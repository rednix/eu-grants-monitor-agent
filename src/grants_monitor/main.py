"""
Main entry point for the EU Grants Monitor Agent.

This module contains the main agent class and CLI interface.
"""

import asyncio
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

import click
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .utils.config import ConfigManager
from .utils.logger import setup_logging
from .data.models import Grant, BusinessProfile
from .scrapers.horizon_scraper import HorizonScraper
from .analyzers.opportunity_analyzer import OpportunityAnalyzer
from .matchers.profile_matcher import ProfileMatcher
from .notifiers.email_notifier import EmailNotifier
from .assistants.application_assistant import ApplicationAssistant
from .services.database import DatabaseService
from .data.mock_grants import get_grant_by_id, get_mock_grants

console = Console()


class GrantsMonitorAgent:
    """Main agent class for monitoring EU grants and tenders."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the grants monitor agent.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        
        # Setup logging
        setup_logging(self.config.get('logging', {}))
        
        # Initialize components
        self.scrapers = self._init_scrapers()
        self.analyzer = OpportunityAnalyzer(self.config.get('analysis', {}))
        self.matcher = ProfileMatcher(self.config.get('matching', {}))
        self.notifier = EmailNotifier(self.config.get('notifications', {}))
        self.assistant = ApplicationAssistant(self.config.get('assistance', {}))
        self.database = DatabaseService(self.config)
        
        # Load business profile
        self.business_profile = self._load_business_profile()
        
        logger.info("Grants Monitor Agent initialized")
    
    def _init_scrapers(self) -> Dict[str, object]:
        """Initialize web scrapers for different EU funding portals."""
        scrapers = {}
        scraper_configs = self.config.get('scrapers', {})
        
        if scraper_configs.get('horizon_europe', {}).get('enabled', True):
            scrapers['horizon'] = HorizonScraper(scraper_configs.get('horizon_europe', {}))
        
        # Add more scrapers as needed
        # scrapers['digital_europe'] = DigitalEuropeScraper(...)
        # scrapers['erdf'] = ERDFScraper(...)
        
        return scrapers
    
    def _load_business_profile(self) -> BusinessProfile:
        """Load business profile from configuration."""
        profile_config = self.config_manager.load_business_profile()
        return BusinessProfile.from_config(profile_config)
    
    async def scan_opportunities(self) -> List[Grant]:
        """Scan all configured sources for new grant opportunities."""
        logger.info("Starting opportunity scan...")
        
        all_grants = []
        for name, scraper in self.scrapers.items():
            try:
                logger.info(f"Scanning {name}...")
                grants = await scraper.scrape_grants()
                all_grants.extend(grants)
                logger.info(f"Found {len(grants)} grants from {name}")
            except Exception as e:
                logger.error(f"Error scanning {name}: {e}")
        
        logger.info(f"Total grants found: {len(all_grants)}")
        return all_grants
    
    async def analyze_opportunities(self, grants: List[Grant]) -> List[Grant]:
        """Analyze grants for relevance and complexity."""
        logger.info("Analyzing opportunities...")
        
        analyzed_grants = []
        for grant in grants:
            try:
                # Analyze relevance to business profile
                relevance_score = await self.matcher.calculate_relevance(
                    grant, self.business_profile
                )
                grant.relevance_score = relevance_score
                
                # Analyze application complexity
                complexity_score = await self.analyzer.assess_complexity(grant)
                grant.complexity_score = complexity_score
                
                # Calculate overall priority
                grant.priority_score = self._calculate_priority(grant)
                
                analyzed_grants.append(grant)
                
            except Exception as e:
                logger.error(f"Error analyzing grant {grant.id}: {e}")
        
        # Sort by priority score
        analyzed_grants.sort(key=lambda g: g.priority_score, reverse=True)
        
        logger.info(f"Analyzed {len(analyzed_grants)} opportunities")
        return analyzed_grants
    
    def _calculate_priority(self, grant: Grant) -> float:
        """Calculate overall priority score for a grant."""
        weights = self.config.get('scoring', {}).get('weights', {})
        
        relevance_weight = weights.get('relevance', 0.4)
        complexity_weight = weights.get('complexity', 0.3)  # Lower complexity = higher score
        amount_weight = weights.get('amount', 0.2)
        deadline_weight = weights.get('deadline', 0.1)
        
        # Normalize scores to 0-1 range
        relevance_norm = grant.relevance_score / 100.0
        complexity_norm = (100 - grant.complexity_score) / 100.0  # Invert complexity
        amount_norm = min(grant.funding_amount / 1000000, 1.0)  # Cap at 1M euros
        deadline_norm = min(grant.days_until_deadline / 365, 1.0)  # Cap at 1 year
        
        priority = (
            relevance_norm * relevance_weight +
            complexity_norm * complexity_weight +
            amount_norm * amount_weight +
            deadline_norm * deadline_weight
        )
        
        return priority * 100  # Convert back to 0-100 scale
    
    async def send_alerts(self, grants: List[Grant]) -> None:
        """Send alerts for high-priority opportunities."""
        alert_threshold = self.config.get('alerts', {}).get('priority_threshold', 70)
        high_priority_grants = [g for g in grants if g.priority_score >= alert_threshold]
        
        if high_priority_grants:
            logger.info(f"Sending alerts for {len(high_priority_grants)} high-priority grants")
            await self.notifier.send_opportunity_alert(high_priority_grants)
        else:
            logger.info("No high-priority grants found for alerts")
    
    async def store_results(self, grants: List[Grant]) -> None:
        """Store monitoring results in the database.
        
        Args:
            grants: List of analyzed grants to store
        """
        if not grants:
            logger.info("No grants to store")
            return
        
        try:
            logger.info(f"Storing {len(grants)} grants to database...")
            self.database.store_grants(grants)
            
            # Store monitoring session data
            session_data = {
                'grants_processed': len(grants),
                'high_priority_count': len([g for g in grants if g.priority_score >= 70]),
                'avg_relevance_score': sum(g.relevance_score for g in grants) / len(grants),
                'avg_complexity_score': sum(g.complexity_score for g in grants) / len(grants),
                'timestamp': datetime.now().isoformat()
            }
            session_id = self.database.store_monitoring_session(session_data)
            logger.info(f"Stored monitoring session: {session_id}")
            
        except Exception as e:
            logger.error(f"Error storing results: {e}")
            # Don't raise the exception to avoid breaking the monitoring cycle
            # but log it for debugging
    
    async def run_monitoring_cycle(self) -> None:
        """Execute a complete monitoring cycle."""
        try:
            # Scan for opportunities
            grants = await self.scan_opportunities()
            
            # Analyze opportunities
            analyzed_grants = await self.analyze_opportunities(grants)
            
            # Send alerts for high-priority items
            await self.send_alerts(analyzed_grants)
            
            # Store results in database
            await self.store_results(analyzed_grants)
            
            logger.info("Monitoring cycle completed successfully")
            
        except Exception as e:
            logger.error(f"Error in monitoring cycle: {e}")
            raise


# CLI Interface
@click.group()
@click.option('--config', '-c', type=click.Path(exists=True), help='Path to config file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx: click.Context, config: Optional[str], verbose: bool) -> None:
    """EU Grants Monitor Agent CLI."""
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = Path(config) if config else None
    ctx.obj['verbose'] = verbose


@cli.command()
@click.pass_context
def setup(ctx: click.Context) -> None:
    """Initialize the agent configuration."""
    console.print("🚀 Setting up EU Grants Monitor Agent...", style="bold blue")
    
    # Create configuration files if they don't exist
    config_manager = ConfigManager(ctx.obj['config_path'])
    config_manager.create_default_configs()
    
    console.print("✅ Configuration files created", style="bold green")
    console.print("\n📝 Next steps:")
    console.print("1. Edit config/config.yaml with your preferences")
    console.print("2. Edit config/business_profile.yaml with your business details")
    console.print("3. Run 'grants-monitor run' to start monitoring")


@cli.command()
@click.option('--continuous', '-c', is_flag=True, help='Run continuously')
@click.pass_context
def run(ctx: click.Context, continuous: bool) -> None:
    """Start monitoring for grant opportunities."""
    console.print("🔍 Starting EU Grants Monitor Agent...", style="bold blue")
    
    agent = GrantsMonitorAgent(ctx.obj['config_path'])
    
    async def main():
        if continuous:
            # Run continuously with scheduled intervals
            console.print("Running in continuous mode...")
            # Implement scheduler here
            while True:
                await agent.run_monitoring_cycle()
                await asyncio.sleep(3600)  # Wait 1 hour
        else:
            # Run once
            await agent.run_monitoring_cycle()
    
    asyncio.run(main())


@cli.command()
@click.option('--port', '-p', default=8000, help='Port to run the API server on')
@click.option('--host', default='0.0.0.0', help='Host to bind the API server to')
@click.pass_context
def serve_api(ctx: click.Context, port: int, host: str) -> None:
    """Start the agent API server for Masumi integration."""
    console.print("🌐 Starting EU Grants Monitor API server...", style="bold blue")
    console.print(f"Server will be available at: http://{host}:{port}")
    
    from .api import app
    import uvicorn
    
    uvicorn.run(app, host=host, port=port)


@cli.command()
@click.option('--api-key', required=True, help='Masumi payment API key')
@click.option('--api-url', required=True, help='Base URL where the agent API is hosted')
@click.option('--network', type=click.Choice(['Preprod', 'Mainnet']), default='Preprod', help='Cardano network')
@click.option('--environment', type=click.Choice(['development', 'staging', 'production']), default='development', help='Environment')
@click.option('--dry-run', is_flag=True, help='Show configuration without registering')
@click.pass_context
def register_masumi(ctx: click.Context, api_key: str, api_url: str, network: str, environment: str, dry_run: bool) -> None:
    """Register this agent with the Masumi registry."""
    console.print("🔗 Registering EU Grants Monitor with Masumi...", style="bold blue")
    
    from .masumi_agent import EUGrantsMonitorMasumiAgent, create_masumi_config, get_default_agent_config
    
    async def register():
        try:
            # Get configuration
            example_configs = {
                "development": {
                    "name": "eu-grants-monitor-dev",
                    "pricing_quantity": "1000000",  # 1 ADA
                    "capability_version": "1.0.0-dev"
                },
                "staging": {
                    "name": "eu-grants-monitor-staging", 
                    "pricing_quantity": "1500000",  # 1.5 ADA
                    "capability_version": "1.0.0-beta"
                },
                "production": {
                    "name": "eu-grants-monitor",
                    "pricing_quantity": "2000000",  # 2 ADA
                    "capability_version": "1.0.0"
                }
            }
            
            custom_config = example_configs.get(environment, {})
            custom_config["api_base_url"] = api_url
            
            if dry_run:
                base_config = get_default_agent_config(api_url)
                base_config.update(custom_config)
                
                console.print("\n🔍 Agent Configuration:", style="bold")
                for key, value in base_config.items():
                    console.print(f"  {key}: {value}")
                console.print(f"\n  Network: {network}")
                console.print(f"  Environment: {environment}")
                return
            
            # Create Masumi configuration
            masumi_config = create_masumi_config(
                payment_api_key=api_key,
                payment_service_url="https://api.masumi.io"
            )
            
            # Get agent configuration
            agent_config = get_default_agent_config(api_url)
            agent_config.update(custom_config)
            
            # Create and register agent
            masumi_agent = EUGrantsMonitorMasumiAgent()
            masumi_agent.create_masumi_agent(
                masumi_config=masumi_config,
                agent_config=agent_config,
                network=network
            )
            
            result = await masumi_agent.register_with_masumi()
            
            console.print("\n✅ Registration Complete!", style="bold green")
            console.print(f"Agent Name: {agent_config['name']}")
            console.print(f"Network: {network}")
            console.print(f"API URL: {api_url}")
            console.print(f"Environment: {environment}")
            
        except Exception as e:
            console.print(f"\n❌ Registration failed: {e}", style="bold red")
            raise
    
    asyncio.run(register())


@cli.command()
@click.option('--api-key', required=True, help='Masumi payment API key')
@click.option('--wallet-vkey', required=True, help='Wallet verification key')
@click.option('--network', type=click.Choice(['Preprod', 'Mainnet']), default='Preprod', help='Cardano network')
@click.pass_context
def check_masumi_status(ctx: click.Context, api_key: str, wallet_vkey: str, network: str) -> None:
    """Check registration status with Masumi registry."""
    console.print("📊 Checking Masumi registration status...", style="bold blue")
    
    from .masumi_agent import EUGrantsMonitorMasumiAgent, create_masumi_config, get_default_agent_config
    
    async def check_status():
        try:
            masumi_config = create_masumi_config(
                payment_api_key=api_key,
                payment_service_url="https://api.masumi.io"
            )
            
            masumi_agent = EUGrantsMonitorMasumiAgent()
            agent_config = get_default_agent_config("http://localhost:8000")
            masumi_agent.create_masumi_agent(
                masumi_config=masumi_config,
                agent_config=agent_config,
                network=network
            )
            
            status = await masumi_agent.check_registration_status(wallet_vkey)
            
            console.print("\n📊 Registration Status:", style="bold")
            if 'data' in status and 'Assets' in status['data']:
                assets = status['data']['Assets']
                if assets:
                    for asset in assets:
                        console.print(f"  Agent: {asset.get('name', 'Unknown')}")
                        console.print(f"  Status: {asset.get('status', 'Unknown')}")
                        console.print(f"  Network: {network}")
                else:
                    console.print("  No registered agents found", style="yellow")
            else:
                console.print(f"  Raw status: {status}")
                
        except Exception as e:
            console.print(f"\n❌ Status check failed: {e}", style="bold red")
            raise
    
    asyncio.run(check_status())


@cli.command()
@click.option('--filter', '-f', help='Filter by keywords')
@click.option('--complexity', help='Filter by complexity (simple, medium, complex)')
@click.option('--amount', help='Filter by funding amount range (e.g., 50000-500000)')
@click.pass_context
def list(ctx: click.Context, filter: Optional[str], complexity: Optional[str], 
         amount: Optional[str]) -> None:
    """List available grant opportunities."""
    console.print("📋 Listing grant opportunities...", style="bold blue")
    
    # Get mock grants
    grants = get_mock_grants()
    
    # Apply filters
    if filter:
        from .data.mock_grants import get_grants_by_keyword
        grants = get_grants_by_keyword(filter)
        console.print(f"Filtering by keyword: {filter}")
    
    if complexity:
        # This would be implemented with actual complexity scoring
        console.print(f"Complexity filter: {complexity} (not yet implemented)")
    
    if amount:
        # Parse amount range and filter
        try:
            if '-' in amount:
                min_amt, max_amt = map(int, amount.split('-'))
                grants = [g for g in grants if min_amt <= g.funding_amount <= max_amt]
                console.print(f"Filtering by amount: €{min_amt:,} - €{max_amt:,}")
        except ValueError:
            console.print(f"Invalid amount format: {amount}", style="red")
    
    # Create and populate table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", no_wrap=True, width=18)
    table.add_column("Title", style="cyan", width=25)
    table.add_column("Synopsis", style="white", width=35)
    table.add_column("Program", style="yellow", width=15)
    table.add_column("Amount", justify="right", style="green", width=12)
    table.add_column("Deadline", style="red", width=12)
    table.add_column("Days", justify="right", style="white", width=5)
    
    for grant in grants:
        days_left = (grant.deadline - date.today()).days
        days_color = "red" if days_left < 30 else "yellow" if days_left < 60 else "green"
        
        table.add_row(
            grant.id,
            grant.title[:23] + ("..." if len(grant.title) > 23 else ""),
            grant.synopsis[:33] + ("..." if len(grant.synopsis) > 33 else ""),
            grant.program.value.replace('_', ' ').title(),
            f"€{grant.funding_amount:,.0f}",
            grant.deadline.strftime("%Y-%m-%d"),
            f"[{days_color}]{days_left}[/]"
        )
    
    console.print(table)
    console.print(f"\nFound {len(grants)} grant opportunities")
    
    if grants:
        console.print("\n💡 Tips:")
        console.print("  • Use 'grants-monitor show <GRANT_ID>' to see full details and URL")
        console.print("  • Use 'grants-monitor assist <GRANT_ID>' to get application guidance!")


@cli.command()
@click.argument('grant_id')
@click.pass_context
def show(ctx: click.Context, grant_id: str) -> None:
    """Show detailed information about a specific grant."""
    try:
        grant = get_grant_by_id(grant_id)
    except ValueError as e:
        console.print(f"❌ Error: {e}", style="bold red")
        console.print("\n📋 Available grants:")
        for g in get_mock_grants():
            console.print(f"  • {g.id}: {g.title}")
        return
    
    # Display detailed grant information
    console.print(Panel(
        f"📜 Grant Details: {grant.id}",
        style="bold blue"
    ))
    
    # Basic information
    info_text = f"**Title:** {grant.title}\n"
    info_text += f"**Program:** {grant.program.value.replace('_', ' ').title()}\n"
    info_text += f"**Synopsis:** {grant.synopsis}\n"
    info_text += f"**Funding Amount:** €{grant.funding_amount:,.0f}\n"
    if grant.min_funding and grant.max_funding:
        info_text += f"**Funding Range:** €{grant.min_funding:,.0f} - €{grant.max_funding:,.0f}\n"
    info_text += f"**Deadline:** {grant.deadline.strftime('%Y-%m-%d')} ({(grant.deadline - date.today()).days} days left)\n"
    info_text += f"**Project Duration:** {grant.start_date.strftime('%Y-%m-%d')} to {grant.end_date.strftime('%Y-%m-%d')}\n"
    info_text += f"**Official URL:** {grant.url}\n"
    if grant.documents_url:
        info_text += f"**Documents URL:** {grant.documents_url}\n"
    
    console.print(Panel(info_text, title="Basic Information"))
    
    # Description
    console.print(Panel(grant.description, title="Description"))
    
    # Eligibility and targets
    if grant.eligible_countries:
        countries_text = ", ".join(grant.eligible_countries)
        console.print(Panel(f"**Eligible Countries:** {countries_text}", title="Eligibility"))
    
    if grant.target_organizations:
        orgs_text = ", ".join(grant.target_organizations)
        console.print(Panel(f"**Target Organizations:** {orgs_text}", title="Target Audience"))
    
    # Keywords
    if grant.keywords:
        keywords_text = ", ".join(grant.keywords)
        console.print(Panel(keywords_text, title="Keywords & Topics"))
    
    console.print("\n💡 Use 'grants-monitor assist {}' for application guidance!".format(grant.id))


@cli.command()
@click.argument('grant_id')
@click.option('--interactive/--no-interactive', default=True, help='Enable/disable interactive prompts')
@click.pass_context
def generate(ctx: click.Context, grant_id: str, interactive: bool) -> None:
    """Generate complete, ready-to-submit application documents."""
    console.print(f"🚀 Generating complete application for grant {grant_id}...", style="bold blue")
    
    try:
        # Initialize the agent
        agent = GrantsMonitorAgent(ctx.obj['config_path'])
        
        # Get the grant data
        try:
            grant = get_grant_by_id(grant_id)
        except ValueError as e:
            console.print(f"❌ Error: {e}", style="bold red")
            console.print("\n📋 Available grants:")
            for g in get_mock_grants():
                console.print(f"  • {g.id}: {g.title}")
            return
        
        # Generate complete application
        async def generate_application():
            return await agent.assistant.generate_complete_application(
                grant, agent.business_profile, interactive=interactive
            )
        
        result = asyncio.run(generate_application())
        
        console.print("\n✅ [bold green]Application generation completed successfully![/bold green]")
        
    except Exception as e:
        logger.error(f"Error generating application: {e}")
        console.print(f"❌ Error generating application: {e}", style="bold red")


@cli.command()
@click.argument('grant_id')
@click.option('--save', '-s', help='Save guidance to file', type=click.Path())
@click.pass_context
def assist(ctx: click.Context, grant_id: str, save: Optional[str]) -> None:
    """Generate application assistance for a specific grant."""
    console.print(f"🤖 Generating assistance for grant {grant_id}...", style="bold blue")
    
    try:
        # Initialize the agent to load configuration
        agent = GrantsMonitorAgent(ctx.obj['config_path'])
        
        # Get the grant data
        try:
            grant = get_grant_by_id(grant_id)
        except ValueError as e:
            console.print(f"❌ Error: {e}", style="bold red")
            console.print("\n📋 Available grants:")
            for g in get_mock_grants():
                console.print(f"  • {g.id}: {g.title}")
            return
        
        # Generate assistance
        async def generate_guidance():
            return await agent.assistant.generate_assistance(grant, agent.business_profile)
        
        guidance = asyncio.run(generate_guidance())
        
        # Display the guidance
        agent.assistant.display_guidance(guidance)
        
        # Save to file if requested
        if save:
            import json
            from dataclasses import asdict
            
            guidance_data = {
                'grant_id': guidance.grant_id,
                'match_score': guidance.match_score,
                'strengths': guidance.strengths,
                'gaps': guidance.gaps,
                'recommendations': guidance.recommendations,
                'timeline': guidance.timeline,
                'required_documents': guidance.required_documents,
                'estimated_effort': guidance.estimated_effort,
                'success_probability': guidance.success_probability,
                'strategic_advice': guidance.strategic_advice,
                'generated_at': datetime.now().isoformat()
            }
            
            with open(save, 'w') as f:
                json.dump(guidance_data, f, indent=2)
            
            console.print(f"\n💾 Guidance saved to: {save}", style="bold green")
        
    except Exception as e:
        logger.error(f"Error generating assistance: {e}")
        console.print(f"❌ Error generating assistance: {e}", style="bold red")


if __name__ == "__main__":
    cli()
