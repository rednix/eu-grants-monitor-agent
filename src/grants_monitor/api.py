"""
API endpoints for the EU Grants Monitor Agent (Masumi integration).

This module provides FastAPI endpoints that expose the agent's capabilities
for registration with the Masumi registry.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger

from .main import GrantsMonitorAgent
from .data.models import Grant, BusinessProfile


# Request/Response Models
class MonitoringRequest(BaseModel):
    """Request to start monitoring grants."""
    
    business_profile: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    alert_preferences: Optional[Dict[str, Any]] = None


class GrantListRequest(BaseModel):
    """Request to list grants with filters."""
    
    keywords: Optional[List[str]] = None
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None
    complexity_max: Optional[int] = None
    deadline_days_min: Optional[int] = None


class ApplicationAssistanceRequest(BaseModel):
    """Request for application assistance."""
    
    grant_id: str
    business_profile: Optional[Dict[str, Any]] = None
    assistance_type: str = Field(default="guidance", description="Type: 'guidance', 'generate', or 'analyze'")
    interactive: bool = Field(default=False, description="Whether to include interactive prompts")


class MonitoringResponse(BaseModel):
    """Response from monitoring operation."""
    
    status: str
    grants_found: int
    high_priority_grants: int
    alerts_sent: int
    monitoring_cycle_id: str
    timestamp: datetime


class GrantListResponse(BaseModel):
    """Response with list of grants."""
    
    status: str
    grants: List[Dict[str, Any]]
    total_count: int
    filters_applied: Dict[str, Any]


class ApplicationAssistanceResponse(BaseModel):
    """Response with application assistance."""
    
    status: str
    grant_id: str
    assistance_type: str
    guidance: Optional[Dict[str, Any]] = None
    generated_documents: Optional[List[Dict[str, str]]] = None
    next_steps: Optional[List[str]] = None


# Initialize FastAPI app
app = FastAPI(
    title="EU Grants Monitor Agent",
    description="An intelligent agent that monitors EU grants and tender opportunities for SMEs, built on the Masumi framework",
    version="1.0.0"
)

# Global agent instance (will be initialized on startup)
grants_agent: Optional[GrantsMonitorAgent] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the grants monitor agent on startup."""
    global grants_agent
    try:
        grants_agent = GrantsMonitorAgent()
        logger.info("EU Grants Monitor Agent API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize grants agent: {e}")
        raise


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "EU Grants Monitor Agent"}


@app.post("/monitor", response_model=MonitoringResponse)
async def start_monitoring(
    request: MonitoringRequest,
    background_tasks: BackgroundTasks
) -> MonitoringResponse:
    """
    Start monitoring EU grants based on business profile and preferences.
    
    This is the main capability of the agent - intelligent monitoring
    and analysis of EU funding opportunities.
    """
    if not grants_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # Update business profile if provided
        if request.business_profile:
            # Create temporary profile for this request
            profile_data = request.business_profile
            business_profile = BusinessProfile.from_config(profile_data)
            grants_agent.business_profile = business_profile
        
        # Run monitoring cycle in background
        monitoring_cycle_id = f"cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        async def run_monitoring():
            try:
                await grants_agent.run_monitoring_cycle()
                logger.info(f"Monitoring cycle {monitoring_cycle_id} completed")
            except Exception as e:
                logger.error(f"Monitoring cycle {monitoring_cycle_id} failed: {e}")
        
        background_tasks.add_task(run_monitoring)
        
        # Return immediate response
        return MonitoringResponse(
            status="started",
            grants_found=0,  # Will be updated after cycle completes
            high_priority_grants=0,
            alerts_sent=0,
            monitoring_cycle_id=monitoring_cycle_id,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Monitoring failed: {str(e)}")


@app.post("/grants/list", response_model=GrantListResponse)
async def list_grants(request: GrantListRequest) -> GrantListResponse:
    """
    List available grant opportunities with optional filtering.
    
    Returns a curated list of EU funding opportunities that match
    the specified criteria and are suitable for SMEs.
    """
    if not grants_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # For this demo, we'll use mock grants
        # In production, this would scan live sources
        from .data.mock_grants import get_mock_grants
        all_grants = get_mock_grants()
        
        # Apply filters
        filtered_grants = []
        for grant in all_grants:
            # Keyword filter
            if request.keywords:
                grant_text = f"{grant.title} {grant.description} {' '.join(grant.keywords)}"
                if not any(keyword.lower() in grant_text.lower() for keyword in request.keywords):
                    continue
            
            # Amount filters
            if request.min_amount and grant.funding_amount < request.min_amount:
                continue
            if request.max_amount and grant.funding_amount > request.max_amount:
                continue
            
            # Complexity filter (mock complexity score)
            if request.complexity_max and getattr(grant, 'complexity_score', 50) > request.complexity_max:
                continue
            
            # Deadline filter
            if request.deadline_days_min and grant.days_until_deadline < request.deadline_days_min:
                continue
            
            filtered_grants.append(grant)
        
        # Analyze and score grants
        analyzed_grants = await grants_agent.analyze_opportunities(filtered_grants)
        
        # Convert to response format
        grants_data = []
        for grant in analyzed_grants:
            grants_data.append({
                "id": grant.id,
                "title": grant.title,
                "program": grant.program,
                "funding_amount": grant.funding_amount,
                "deadline": grant.deadline.isoformat(),
                "days_until_deadline": grant.days_until_deadline,
                "relevance_score": getattr(grant, 'relevance_score', 0),
                "complexity_score": getattr(grant, 'complexity_score', 0),
                "priority_score": getattr(grant, 'priority_score', 0),
                "synopsis": getattr(grant, 'synopsis', ''),
                "url": getattr(grant, 'url', ''),
                "keywords": grant.keywords
            })
        
        return GrantListResponse(
            status="success",
            grants=grants_data,
            total_count=len(grants_data),
            filters_applied=request.dict(exclude_none=True)
        )
    
    except Exception as e:
        logger.error(f"Error listing grants: {e}")
        raise HTTPException(status_code=500, detail=f"Grant listing failed: {str(e)}")


@app.post("/grants/{grant_id}/assist", response_model=ApplicationAssistanceResponse)
async def get_application_assistance(
    grant_id: str,
    request: ApplicationAssistanceRequest
) -> ApplicationAssistanceResponse:
    """
    Get intelligent application assistance for a specific grant.
    
    Provides guidance, document generation, and strategic advice
    for EU grant applications tailored to SME capabilities.
    """
    if not grants_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # Get the specific grant
        from .data.mock_grants import get_grant_by_id
        grant = get_grant_by_id(grant_id)
        if not grant:
            raise HTTPException(status_code=404, detail=f"Grant {grant_id} not found")
        
        # Update business profile if provided
        if request.business_profile:
            profile_data = request.business_profile
            business_profile = BusinessProfile.from_config(profile_data)
            grants_agent.business_profile = business_profile
        
        response_data = {
            "status": "success",
            "grant_id": grant_id,
            "assistance_type": request.assistance_type
        }
        
        if request.assistance_type == "guidance":
            # Provide strategic guidance
            guidance = await grants_agent.assistant.analyze_application_requirements(grant)
            response_data["guidance"] = {
                "eligibility_assessment": guidance.get("eligibility", {}),
                "success_factors": guidance.get("success_factors", []),
                "application_strategy": guidance.get("strategy", {}),
                "timeline_recommendations": guidance.get("timeline", {}),
                "budget_guidance": guidance.get("budget", {})
            }
            response_data["next_steps"] = [
                "Review eligibility requirements carefully",
                "Prepare required documentation",
                "Develop technical approach",
                "Prepare budget breakdown",
                "Submit application before deadline"
            ]
        
        elif request.assistance_type == "generate":
            # Generate application documents (simplified for API)
            if request.interactive:
                # In a real implementation, this would need WebSocket or polling
                response_data["status"] = "interactive_mode_not_supported_in_api"
                response_data["guidance"] = {
                    "message": "Interactive mode requires CLI. Use non-interactive generation.",
                    "cli_command": f"grants-monitor generate {grant_id} --interactive"
                }
            else:
                # Generate documents without interaction
                docs_info = await grants_agent.assistant.generate_complete_application(
                    grant, interactive=False
                )
                response_data["generated_documents"] = [
                    {
                        "name": "Application Summary",
                        "type": "summary",
                        "description": "Overview of the generated application"
                    },
                    {
                        "name": "Pre-filled Forms",
                        "type": "forms",
                        "description": "Application forms with pre-filled company data"
                    }
                ]
                response_data["next_steps"] = [
                    "Download generated documents",
                    "Review and complete remaining fields",
                    "Gather supporting documents",
                    "Submit to EU portal"
                ]
        
        elif request.assistance_type == "analyze":
            # Analyze grant opportunity
            relevance = await grants_agent.matcher.calculate_relevance(
                grant, grants_agent.business_profile
            )
            complexity = await grants_agent.analyzer.assess_complexity(grant)
            
            response_data["guidance"] = {
                "relevance_analysis": {
                    "score": relevance,
                    "match_factors": [
                        "AI expertise alignment",
                        "Industry focus match",
                        "Company size eligibility"
                    ]
                },
                "complexity_analysis": {
                    "score": complexity,
                    "difficulty_factors": [
                        "Application process complexity",
                        "Documentation requirements",
                        "Competition level"
                    ]
                },
                "recommendation": "High relevance, moderate complexity - recommended for application"
            }
        
        return ApplicationAssistanceResponse(**response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error providing assistance for grant {grant_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Assistance failed: {str(e)}")


@app.get("/grants/{grant_id}")
async def get_grant_details(grant_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific grant."""
    try:
        from .data.mock_grants import get_grant_by_id
        grant = get_grant_by_id(grant_id)
        if not grant:
            raise HTTPException(status_code=404, detail=f"Grant {grant_id} not found")
        
        return {
            "id": grant.id,
            "title": grant.title,
            "program": grant.program,
            "description": grant.description,
            "synopsis": getattr(grant, 'synopsis', ''),
            "funding_amount": grant.funding_amount,
            "funding_range_min": getattr(grant, 'funding_range_min', None),
            "funding_range_max": getattr(grant, 'funding_range_max', None),
            "deadline": grant.deadline.isoformat(),
            "days_until_deadline": grant.days_until_deadline,
            "project_duration_start": grant.project_duration_start.isoformat() if grant.project_duration_start else None,
            "project_duration_end": grant.project_duration_end.isoformat() if grant.project_duration_end else None,
            "url": getattr(grant, 'url', ''),
            "documents_url": getattr(grant, 'documents_url', ''),
            "eligible_countries": getattr(grant, 'eligible_countries', []),
            "target_organizations": getattr(grant, 'target_organizations', []),
            "keywords": grant.keywords
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting grant details for {grant_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get grant details: {str(e)}")


@app.get("/status")
async def get_agent_status() -> Dict[str, Any]:
    """Get current status of the grants monitoring agent."""
    if not grants_agent:
        return {"status": "not_initialized", "error": "Agent not initialized"}
    
    try:
        return {
            "status": "active",
            "agent_name": "EU Grants Monitor Agent",
            "version": "1.0.0",
            "capabilities": [
                "EU grants monitoring",
                "SME-focused opportunity analysis", 
                "Application assistance",
                "Document generation",
                "Real-time alerts"
            ],
            "supported_programs": [
                "Horizon Europe",
                "Digital Europe",
                "ERDF",
                "Life Programme",
                "Erasmus Plus"
            ],
            "business_profile_loaded": grants_agent.business_profile is not None,
            "scrapers_active": len(grants_agent.scrapers),
            "last_scan": None  # Would track last monitoring cycle
        }
    
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        return {"status": "error", "error": str(e)}


# Add CORS middleware for web integration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
