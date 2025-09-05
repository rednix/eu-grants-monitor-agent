"""
Main entry point for the EU Grants Monitor Agent.

This module contains the main agent class and CLI interface.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Optional

import click
from loguru import logger
from rich.console import Console
from rich.table import Table

# Masumi imports (placeholder - adjust based on actual Masumi API)
# from masumi import Agent, AgentConfig

from .utils.config import ConfigManager
from .utils.logger import setup_logging
from .data.models import Grant, BusinessProfile
from .scrapers.horizon_scraper import HorizonScraper
from .analyzers.opportunity_analyzer import OpportunityAnalyzer
from .matchers.profile_matcher import ProfileMatcher
from .notifiers.email_notifier import EmailNotifier

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
    
    async def run_monitoring_cycle(self) -> None:
        """Execute a complete monitoring cycle."""
        try:
            # Scan for opportunities
            grants = await self.scan_opportunities()
            
            # Analyze opportunities
            analyzed_grants = await self.analyze_opportunities(grants)
            
            # Send alerts for high-priority items
            await self.send_alerts(analyzed_grants)
            
            # Store results (implement database storage)
            # await self.store_results(analyzed_grants)
            
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
@click.option('--filter', '-f', help='Filter by keywords')
@click.option('--complexity', help='Filter by complexity (simple, medium, complex)')
@click.option('--amount', help='Filter by funding amount range (e.g., 50000-500000)')
@click.pass_context
def list(ctx: click.Context, filter: Optional[str], complexity: Optional[str], 
         amount: Optional[str]) -> None:
    """List available grant opportunities."""
    console.print("📋 Listing grant opportunities...", style="bold blue")
    
    # This would fetch from database in real implementation
    # For now, show a sample table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Title")
    table.add_column("Program")
    table.add_column("Amount", justify="right")
    table.add_column("Deadline")
    table.add_column("Priority", justify="right")
    
    # Sample data
    table.add_row(
        "HE-2024-AI-001",
        "AI for Healthcare SMEs",
        "Horizon Europe",
        "€250,000",
        "2024-03-15",
        "85%"
    )
    
    console.print(table)


@cli.command()
@click.argument('grant_id')
@click.pass_context
def assist(ctx: click.Context, grant_id: str) -> None:
    """Generate application assistance for a specific grant."""
    console.print(f"🤖 Generating assistance for grant {grant_id}...", style="bold blue")
    
    # This would provide detailed application guidance
    console.print("Application assistance feature coming soon!", style="yellow")


if __name__ == "__main__":
    cli()
