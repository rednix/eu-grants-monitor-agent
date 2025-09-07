"""
Masumi Agent integration for EU Grants Monitor.

This module creates a Masumi-compliant agent that can be registered
with the Masumi registry and handle payments via the Cardano blockchain.
"""

import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

from masumi import Agent, Config
from loguru import logger

from .main import GrantsMonitorAgent
from .api import app


class EUGrantsMonitorMasumiAgent:
    """
    Masumi-integrated EU Grants Monitor Agent.
    
    This wraps the core GrantsMonitorAgent functionality in a Masumi-compatible
    agent that can be registered with the Masumi registry for payment-based access.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the Masumi agent wrapper."""
        self.config_path = config_path
        self.grants_agent = GrantsMonitorAgent(config_path)
        self.masumi_agent: Optional[Agent] = None
        
        logger.info("EU Grants Monitor Masumi Agent initialized")
    
    def create_masumi_agent(
        self,
        masumi_config: Config,
        agent_config: Dict[str, Any],
        network: str = "Preprod"
    ) -> Agent:
        """
        Create and configure the Masumi agent for registry registration.
        
        Args:
            masumi_config: Masumi configuration with API keys
            agent_config: Agent configuration (name, description, etc.)
            network: Cardano network to use ("Preprod" or "Mainnet")
        """
        
        # Define example outputs for the agent
        example_outputs = [
            {
                "name": "EU Grants List",
                "url": "https://example.com/grants-list.json",
                "mimeType": "application/json"
            },
            {
                "name": "Application Guidance",
                "url": "https://example.com/application-guidance.pdf",
                "mimeType": "application/pdf"
            },
            {
                "name": "Generated Application Forms",
                "url": "https://example.com/forms.zip",
                "mimeType": "application/zip"
            }
        ]
        
        # Create the Masumi agent
        self.masumi_agent = Agent(
            name=agent_config.get("name", "eu-grants-monitor"),
            config=masumi_config,
            description=agent_config.get("description", 
                "Intelligent monitoring and application assistance for EU grants and funding opportunities, specifically designed for SMEs in the AI sector."),
            example_output=example_outputs,
            tags=agent_config.get("tags", [
                "eu-funding", "grants", "sme", "ai", "monitoring", "assistance", 
                "horizon-europe", "digital-europe", "applications"
            ]),
            api_base_url=agent_config.get("api_base_url", "http://localhost:8000"),
            author_name=agent_config.get("author_name", "EU Grants Monitor Team"),
            author_contact=agent_config.get("author_contact", "contact@eu-grants-monitor.com"),
            author_organization=agent_config.get("author_organization", "EU Grants Monitor"),
            legal_privacy_policy=agent_config.get("legal_privacy_policy", 
                "https://eu-grants-monitor.com/privacy"),
            legal_terms=agent_config.get("legal_terms", 
                "https://eu-grants-monitor.com/terms"),
            legal_other=agent_config.get("legal_other", 
                "https://eu-grants-monitor.com/legal"),
            capability_name=agent_config.get("capability_name", "EU Grants Intelligence"),
            capability_version=agent_config.get("capability_version", "1.0.0"),
            pricing_unit=agent_config.get("pricing_unit", "lovelace"),
            pricing_quantity=agent_config.get("pricing_quantity", "1000000"),  # 1 ADA
            network=network
        )
        
        logger.info(f"Created Masumi agent: {agent_config.get('name')} on {network}")
        return self.masumi_agent
    
    async def register_with_masumi(self) -> Dict[str, Any]:
        """Register this agent with the Masumi registry."""
        if not self.masumi_agent:
            raise ValueError("Masumi agent not created. Call create_masumi_agent() first.")
        
        try:
            logger.info("Starting Masumi agent registration...")
            registration_result = await self.masumi_agent.register()
            logger.info("Successfully registered with Masumi registry")
            return registration_result
        except Exception as e:
            logger.error(f"Failed to register with Masumi: {e}")
            raise
    
    async def check_registration_status(self, wallet_vkey: str) -> Dict[str, Any]:
        """Check the registration status with Masumi registry."""
        if not self.masumi_agent:
            raise ValueError("Masumi agent not created. Call create_masumi_agent() first.")
        
        try:
            status = await self.masumi_agent.check_registration_status(wallet_vkey)
            logger.info("Retrieved registration status from Masumi")
            return status
        except Exception as e:
            logger.error(f"Failed to check registration status: {e}")
            raise
    
    def get_api_app(self):
        """Get the FastAPI application for serving the agent."""
        return app
    
    def start_api_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Start the API server for the agent."""
        import uvicorn
        logger.info(f"Starting EU Grants Monitor API server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    
    async def process_monitoring_request(
        self, 
        business_profile: Dict[str, Any],
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a monitoring request (main agent capability).
        
        This is the core service that would be called by Masumi clients
        after payment verification.
        """
        try:
            logger.info("Processing EU grants monitoring request")
            
            # Update business profile for this request
            from .data.models import BusinessProfile
            profile = BusinessProfile.from_config(business_profile)
            self.grants_agent.business_profile = profile
            
            # Scan for opportunities
            grants = await self.grants_agent.scan_opportunities()
            logger.info(f"Found {len(grants)} grants")
            
            # Analyze opportunities
            analyzed_grants = await self.grants_agent.analyze_opportunities(grants)
            logger.info(f"Analyzed {len(analyzed_grants)} opportunities")
            
            # Apply filters if provided
            filtered_grants = analyzed_grants
            if filters:
                filtered_grants = []
                for grant in analyzed_grants:
                    # Apply keyword filter
                    if 'keywords' in filters:
                        grant_text = f"{grant.title} {grant.description}".lower()
                        if not any(kw.lower() in grant_text for kw in filters['keywords']):
                            continue
                    
                    # Apply amount filters
                    if 'min_amount' in filters and grant.funding_amount < filters['min_amount']:
                        continue
                    if 'max_amount' in filters and grant.funding_amount > filters['max_amount']:
                        continue
                    
                    # Apply complexity filter
                    if 'max_complexity' in filters:
                        complexity = getattr(grant, 'complexity_score', 50)
                        if complexity > filters['max_complexity']:
                            continue
                    
                    filtered_grants.append(grant)
            
            # Prepare response
            grants_data = []
            for grant in filtered_grants[:10]:  # Return top 10
                grants_data.append({
                    "id": grant.id,
                    "title": grant.title,
                    "program": grant.program,
                    "funding_amount": grant.funding_amount,
                    "deadline": grant.deadline.isoformat(),
                    "days_until_deadline": grant.days_until_deadline,
                    "relevance_score": getattr(grant, 'relevance_score', 0),
                    "priority_score": getattr(grant, 'priority_score', 0),
                    "synopsis": getattr(grant, 'synopsis', ''),
                    "url": getattr(grant, 'url', ''),
                    "keywords": grant.keywords
                })
            
            return {
                "status": "success",
                "total_grants_found": len(grants),
                "analyzed_grants": len(analyzed_grants),
                "filtered_grants": len(filtered_grants),
                "returned_grants": len(grants_data),
                "grants": grants_data,
                "timestamp": grants[0].last_updated.isoformat() if grants else None
            }
        
        except Exception as e:
            logger.error(f"Error processing monitoring request: {e}")
            return {
                "status": "error",
                "error": str(e),
                "grants": []
            }
    
    async def process_application_assistance_request(
        self,
        grant_id: str,
        business_profile: Dict[str, Any],
        assistance_type: str = "guidance"
    ) -> Dict[str, Any]:
        """
        Process an application assistance request.
        
        Another core service for helping with grant applications.
        """
        try:
            logger.info(f"Processing application assistance request for grant {grant_id}")
            
            # Get the grant
            from .data.mock_grants import get_grant_by_id
            grant = get_grant_by_id(grant_id)
            if not grant:
                return {
                    "status": "error",
                    "error": f"Grant {grant_id} not found"
                }
            
            # Update business profile
            from .data.models import BusinessProfile
            profile = BusinessProfile.from_config(business_profile)
            self.grants_agent.business_profile = profile
            
            response_data = {
                "status": "success",
                "grant_id": grant_id,
                "grant_title": grant.title,
                "assistance_type": assistance_type
            }
            
            if assistance_type == "analyze":
                # Analyze grant fit
                relevance = await self.grants_agent.matcher.calculate_relevance(grant, profile)
                complexity = await self.grants_agent.analyzer.assess_complexity(grant)
                
                response_data.update({
                    "relevance_score": relevance,
                    "complexity_score": complexity,
                    "recommendation": "recommended" if relevance > 70 and complexity < 60 else "consider_carefully",
                    "analysis": {
                        "strengths": [
                            "Strong alignment with AI expertise",
                            "Appropriate funding level for SME",
                            "Reasonable application complexity"
                        ],
                        "considerations": [
                            "Ensure compliance with eligibility criteria",
                            "Prepare comprehensive technical approach",
                            "Plan for required project management"
                        ]
                    }
                })
            
            elif assistance_type == "guidance":
                # Provide application guidance
                guidance = await self.grants_agent.assistant.analyze_application_requirements(grant)
                response_data.update({
                    "guidance": guidance,
                    "key_requirements": [
                        "Technical innovation description",
                        "Market analysis and impact",
                        "Project management plan",
                        "Budget justification",
                        "Risk assessment"
                    ],
                    "success_tips": [
                        "Demonstrate clear European added value",
                        "Show strong technical feasibility",
                        "Include measurable outcomes",
                        "Address sustainability and scalability"
                    ]
                })
            
            elif assistance_type == "documents":
                # Generate application documents (simplified)
                response_data.update({
                    "documents_status": "generated",
                    "documents": [
                        {
                            "type": "application_form",
                            "status": "pre_filled",
                            "completion": "75%"
                        },
                        {
                            "type": "budget_template", 
                            "status": "template_ready",
                            "completion": "60%"
                        },
                        {
                            "type": "project_summary",
                            "status": "draft_created",
                            "completion": "80%"
                        }
                    ],
                    "next_steps": [
                        "Review pre-filled forms",
                        "Complete technical sections",
                        "Finalize budget details",
                        "Submit before deadline"
                    ]
                })
            
            return response_data
        
        except Exception as e:
            logger.error(f"Error processing assistance request: {e}")
            return {
                "status": "error",
                "error": str(e)
            }


def create_masumi_config(
    payment_api_key: str,
    payment_service_url: str = "https://api.masumi.io"
) -> Config:
    """Create a Masumi configuration."""
    return Config(
        payment_api_key=payment_api_key,
        payment_service_url=payment_service_url
    )


def get_default_agent_config(api_base_url: str) -> Dict[str, Any]:
    """Get default agent configuration for Masumi registration."""
    return {
        "name": "eu-grants-monitor",
        "description": (
            "Intelligent monitoring and application assistance for EU grants and funding opportunities. "
            "Specializes in identifying suitable opportunities for SMEs in the AI sector, providing "
            "relevance analysis, complexity assessment, and complete application generation support. "
            "Covers Horizon Europe, Digital Europe Programme, ERDF, and other major EU funding sources."
        ),
        "tags": [
            "eu-funding", "grants", "sme", "ai", "monitoring", "assistance", 
            "horizon-europe", "digital-europe", "applications", "consulting",
            "startups", "innovation", "research", "development"
        ],
        "api_base_url": api_base_url,
        "author_name": "EU Grants Monitor Team",
        "author_contact": "contact@eu-grants-monitor.com", 
        "author_organization": "EU Grants Monitor",
        "legal_privacy_policy": "https://eu-grants-monitor.com/privacy",
        "legal_terms": "https://eu-grants-monitor.com/terms",
        "legal_other": "https://eu-grants-monitor.com/legal",
        "capability_name": "EU Grants Intelligence",
        "capability_version": "1.0.0",
        "pricing_unit": "lovelace",
        "pricing_quantity": "2000000",  # 2 ADA per request
    }
