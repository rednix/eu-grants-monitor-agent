"""
Document Analyzer Service for EU Grant Applications.

This service downloads, analyzes, and extracts information from grant
application documents, forms, and requirements.
"""

import asyncio
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re

import aiohttp
import PyPDF2
from bs4 import BeautifulSoup
from loguru import logger

from ..data.models import Grant


@dataclass
class DocumentInfo:
    """Information about a downloaded document."""
    
    filename: str
    file_type: str
    size_bytes: int
    local_path: str
    url: str
    is_form: bool = False
    form_fields: List[str] = None
    requirements: List[str] = None


@dataclass
class GrantDocumentPackage:
    """Complete package of grant documents."""
    
    grant_id: str
    documents: List[DocumentInfo]
    call_text: str
    eligibility_requirements: List[str]
    application_forms: List[DocumentInfo]
    supporting_documents: List[str]
    deadlines: Dict[str, str]
    budget_requirements: Dict[str, Any]


class DocumentAnalyzer:
    """Analyzes and processes grant application documents."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the document analyzer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.temp_dir = Path(tempfile.mkdtemp(prefix="grants_docs_"))
        self.session = None
        logger.info(f"DocumentAnalyzer initialized with temp dir: {self.temp_dir}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'EU-Grants-Monitor-Agent/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def analyze_grant_documents(self, grant: Grant) -> GrantDocumentPackage:
        """Download and analyze all documents for a grant.
        
        Args:
            grant: Grant object to analyze
            
        Returns:
            GrantDocumentPackage with analyzed documents
        """
        logger.info(f"Analyzing documents for grant {grant.id}")
        
        # Download main call documentation
        call_text = await self._fetch_call_text(grant.url)
        
        # Download application documents
        documents = await self._download_application_documents(grant)
        
        # Analyze documents for requirements and forms
        eligibility_reqs = self._extract_eligibility_requirements(call_text, documents)
        forms = self._identify_application_forms(documents)
        supporting_docs = self._identify_supporting_documents(call_text, documents)
        deadlines = self._extract_deadlines(call_text)
        budget_reqs = self._extract_budget_requirements(call_text, documents)
        
        return GrantDocumentPackage(
            grant_id=grant.id,
            documents=documents,
            call_text=call_text,
            eligibility_requirements=eligibility_reqs,
            application_forms=forms,
            supporting_documents=supporting_docs,
            deadlines=deadlines,
            budget_requirements=budget_reqs
        )
    
    async def _fetch_call_text(self, url: str) -> str:
        """Fetch and extract text from grant call webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            Extracted text content
        """
        # For demonstration, return mock call text
        return f"""
HORIZON EUROPE GRANT CALL

This call supports Small and Medium Enterprises (SMEs) in developing innovative solutions.

ELIGIBILITY CRITERIA:
- Must be a legally established SME
- Located in EU member state or associated country
- Demonstrate technical and financial capacity
- Minimum 2 years of operational experience

FUNDING DETAILS:
- Maximum funding: €500,000 per project
- Funding rate: 70% for SMEs
- Project duration: 18-36 months

REQUIREMENTS:
- Technical feasibility assessment required
- Ethics self-assessment mandatory
- Data management plan required for data-intensive projects
- Consortium with minimum 3 partners required for grants >€1M

EVALUATION CRITERIA:
- Excellence (30%)
- Impact (30%)
- Implementation (40%)

APPLICATION DOCUMENTS:
- Application form (mandatory)
- Budget template (mandatory)  
- Technical annexes
- CVs of key personnel
- Company registration documents
"""
    
    async def _download_application_documents(self, grant: Grant) -> List[DocumentInfo]:
        """Download application documents and forms.
        
        Args:
            grant: Grant object
            
        Returns:
            List of downloaded document information
        """
        documents = []
        
        if grant.documents_url:
            # Simulate downloading common EU grant documents
            mock_documents = [
                {
                    "filename": f"{grant.id}_application_form.pdf",
                    "file_type": "pdf",
                    "size_bytes": 245760,
                    "url": f"{grant.documents_url}/application_form.pdf",
                    "is_form": True,
                    "form_fields": [
                        "organization_name", "organization_type", "country",
                        "project_title", "project_summary", "total_budget",
                        "project_coordinator", "contact_email", "start_date",
                        "duration_months", "consortium_members", "work_packages"
                    ]
                },
                {
                    "filename": f"{grant.id}_budget_template.xlsx",
                    "file_type": "xlsx",
                    "size_bytes": 45120,
                    "url": f"{grant.documents_url}/budget_template.xlsx",
                    "is_form": True,
                    "form_fields": [
                        "personnel_costs", "equipment_costs", "travel_costs",
                        "other_costs", "indirect_costs", "total_costs"
                    ]
                },
                {
                    "filename": f"{grant.id}_guidelines.pdf",
                    "file_type": "pdf",
                    "size_bytes": 1024000,
                    "url": f"{grant.documents_url}/guidelines.pdf",
                    "is_form": False,
                    "requirements": [
                        "Technical feasibility assessment",
                        "Market analysis and commercialization plan",
                        "Risk assessment and mitigation strategies",
                        "Consortium agreement (if applicable)",
                        "Ethics self-assessment",
                        "Data management plan"
                    ]
                }
            ]
            
            for doc_info in mock_documents:
                # Simulate local file path
                local_path = self.temp_dir / doc_info["filename"]
                
                doc = DocumentInfo(
                    filename=doc_info["filename"],
                    file_type=doc_info["file_type"],
                    size_bytes=doc_info["size_bytes"],
                    local_path=str(local_path),
                    url=doc_info["url"],
                    is_form=doc_info.get("is_form", False),
                    form_fields=doc_info.get("form_fields", []),
                    requirements=doc_info.get("requirements", [])
                )
                documents.append(doc)
                
                logger.info(f"Simulated download: {doc.filename}")
        
        return documents
    
    def _extract_eligibility_requirements(self, call_text: str, documents: List[DocumentInfo]) -> List[str]:
        """Extract eligibility requirements from call text and documents."""
        requirements = []
        
        # Common EU grant eligibility patterns
        eligibility_patterns = [
            r"eligible.{0,50}SME",
            r"Must be.{0,50}legally established",
            r"minimum.{0,20}years.{0,20}experience",
            r"EU member state",
            r"associated country"
        ]
        
        for pattern in eligibility_patterns:
            matches = re.findall(pattern, call_text, re.IGNORECASE)
            for match in matches:
                requirements.append(match.strip())
        
        # Add program-specific requirements
        if "horizon" in call_text.lower():
            requirements.extend([
                "EU legal entity or associated country",
                "Demonstrated technical and financial capacity",
                "Clear European added value"
            ])
        
        # Extract requirements from documents
        for doc in documents:
            if doc.requirements:
                requirements.extend(doc.requirements)
        
        return list(set(requirements))  # Remove duplicates
    
    def _identify_application_forms(self, documents: List[DocumentInfo]) -> List[DocumentInfo]:
        """Identify which documents are application forms."""
        return [doc for doc in documents if doc.is_form]
    
    def _identify_supporting_documents(self, call_text: str, documents: List[DocumentInfo]) -> List[str]:
        """Identify required supporting documents."""
        supporting_docs = []
        
        # Common supporting documents
        if "cv" in call_text.lower() or "personnel" in call_text.lower():
            supporting_docs.append("CV of key personnel")
        
        if "financial" in call_text.lower() or "company registration" in call_text.lower():
            supporting_docs.append("Company registration documents")
        
        if "ethics" in call_text.lower():
            supporting_docs.append("Ethics self-assessment")
        
        if "data management" in call_text.lower():
            supporting_docs.append("Data management plan")
        
        return supporting_docs
    
    def _extract_deadlines(self, call_text: str) -> Dict[str, str]:
        """Extract important deadlines from call text."""
        deadlines = {}
        
        # For demonstration, return a default deadline
        deadlines["submission"] = "Check grant documentation for specific deadline"
        
        return deadlines
    
    def _extract_budget_requirements(self, call_text: str, documents: List[DocumentInfo]) -> Dict[str, Any]:
        """Extract budget requirements and constraints."""
        budget_reqs = {
            "min_amount": None,
            "max_amount": None,
            "funding_rate": "70% for SMEs",
            "eligible_costs": [
                "Personnel costs",
                "Equipment and infrastructure",
                "Travel and accommodation",
                "External services and consultancy",
                "Other direct costs",
                "Indirect costs (25% of direct costs)"
            ],
            "cost_categories": [
                "Personnel costs",
                "Equipment and infrastructure", 
                "Travel and accommodation",
                "External services and consultancy",
                "Other direct costs",
                "Indirect costs"
            ]
        }
        
        return budget_reqs
    
    def cleanup(self):
        """Clean up temporary files."""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logger.info("Cleaned up temporary document files")
        except Exception as e:
            logger.warning(f"Error cleaning up temp files: {e}")
