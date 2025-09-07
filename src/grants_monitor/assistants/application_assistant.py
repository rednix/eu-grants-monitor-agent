"""
Application Assistant for EU Grant Applications.

This module provides intelligent assistance for preparing EU grant applications,
including requirement analysis, template generation, and strategic guidance.
"""

import asyncio
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from loguru import logger

from ..data.models import Grant, BusinessProfile, ComplexityLevel
from ..services.document_analyzer import DocumentAnalyzer, GrantDocumentPackage
from ..services.web_researcher import WebResearcher, CompanyInfo
from ..services.form_prefiller import FormPrefiller, PrefilledForm
from ..services.document_generator import DocumentGenerator, GeneratedDocument
from ..services.user_prompter import UserPrompter, UserResponse


@dataclass
class ApplicationGuidance:
    """Structured guidance for a grant application."""
    
    grant_id: str
    match_score: float
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]
    timeline: List[Dict[str, Any]]
    required_documents: List[str]
    estimated_effort: str
    success_probability: str
    strategic_advice: str


@dataclass
class RequirementAnalysis:
    """Analysis of grant requirements."""
    
    technical_requirements: List[str]
    eligibility_criteria: List[str]
    consortium_requirements: Optional[Dict[str, Any]]
    funding_details: Dict[str, Any]
    deliverables: List[str]
    evaluation_criteria: Dict[str, float]


class ApplicationAssistant:
    """Provides intelligent assistance for EU grant applications."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the application assistant.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.console = Console()
        logger.info("Application Assistant initialized")
    
    async def generate_assistance(
        self, 
        grant: Grant, 
        business_profile: BusinessProfile
    ) -> ApplicationGuidance:
        """Generate comprehensive application assistance for a grant.
        
        Args:
            grant: Grant opportunity to analyze
            business_profile: Business profile for matching
            
        Returns:
            ApplicationGuidance object with detailed recommendations
        """
        logger.info(f"Generating assistance for grant {grant.id}")
        
        # Analyze requirements
        requirements = self._analyze_requirements(grant)
        
        # Calculate match score and identify gaps
        match_score, strengths, gaps = self._analyze_business_fit(
            grant, business_profile, requirements
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            grant, business_profile, requirements, gaps
        )
        
        # Create application timeline
        timeline = self._create_application_timeline(grant)
        
        # Estimate effort and success probability
        effort = self._estimate_application_effort(grant, requirements)
        success_prob = self._estimate_success_probability(
            match_score, grant.complexity_level, business_profile
        )
        
        # Generate strategic advice
        strategic_advice = self._generate_strategic_advice(
            grant, business_profile, match_score
        )
        
        # Required documents
        required_docs = self._get_required_documents(grant, requirements)
        
        return ApplicationGuidance(
            grant_id=grant.id,
            match_score=match_score,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            timeline=timeline,
            required_documents=required_docs,
            estimated_effort=effort,
            success_probability=success_prob,
            strategic_advice=strategic_advice
        )
    
    def _analyze_requirements(self, grant: Grant) -> RequirementAnalysis:
        """Analyze grant requirements and extract key information."""
        
        # In a real implementation, this would parse actual grant documents
        # For now, we'll generate realistic requirements based on grant type
        
        technical_reqs = []
        eligibility = []
        consortium = None
        deliverables = []
        evaluation_criteria = {}
        
        # Extract requirements based on keywords and program
        if "artificial intelligence" in grant.description.lower() or "ai" in grant.keywords:
            technical_reqs.extend([
                "Demonstrated AI/ML expertise",
                "Experience with production AI systems",
                "Data handling and privacy compliance",
                "Scalable AI architecture design"
            ])
            deliverables.extend([
                "AI model development and validation",
                "Technical documentation and specifications",
                "User training materials",
                "Performance benchmarking report"
            ])
            evaluation_criteria = {
                "Technical Excellence": 0.3,
                "Innovation": 0.25,
                "Impact": 0.2,
                "Implementation Quality": 0.15,
                "Sustainability": 0.1
            }
        
        if "healthcare" in grant.description.lower() or "health" in grant.keywords:
            technical_reqs.extend([
                "Healthcare industry experience",
                "Medical data handling compliance (GDPR, HIPAA)",
                "Clinical workflow understanding"
            ])
            eligibility.extend([
                "Healthcare technology experience required",
                "Must demonstrate understanding of medical regulations"
            ])
        
        if "sme" in grant.description.lower() or grant.target_organizations:
            eligibility.extend([
                "Small to Medium Enterprise (SME) status required",
                "EU-based organization",
                f"Maximum {grant.max_funding or grant.funding_amount} EUR funding request"
            ])
        
        # Consortium requirements for larger grants
        if grant.funding_amount > 500000:
            consortium = {
                "required": True,
                "min_partners": 3,
                "partner_types": ["SME", "Research Institution", "Large Enterprise"],
                "geographic_distribution": "At least 2 EU countries"
            }
        
        funding_details = {
            "total_budget": grant.funding_amount,
            "max_funding_rate": "70% for SMEs, 50% for large enterprises",
            "eligible_costs": [
                "Personnel costs",
                "Equipment and infrastructure",
                "Travel and accommodation",
                "External services",
                "Dissemination and exploitation"
            ]
        }
        
        return RequirementAnalysis(
            technical_requirements=technical_reqs,
            eligibility_criteria=eligibility,
            consortium_requirements=consortium,
            funding_details=funding_details,
            deliverables=deliverables,
            evaluation_criteria=evaluation_criteria
        )
    
    def _analyze_business_fit(
        self, 
        grant: Grant, 
        profile: BusinessProfile, 
        requirements: RequirementAnalysis
    ) -> Tuple[float, List[str], List[str]]:
        """Analyze how well the business profile fits the grant requirements."""
        
        strengths = []
        gaps = []
        score_components = []
        
        # Check technical expertise match
        tech_match = 0
        profile_expertise = set(profile.ai_expertise + profile.technology_focus)
        
        for req in requirements.technical_requirements:
            if any(tech.lower() in req.lower() for tech in profile_expertise):
                tech_match += 1
                strengths.append(f"Strong match: {req}")
            else:
                gaps.append(f"Technical gap: {req}")
        
        if requirements.technical_requirements:
            tech_score = tech_match / len(requirements.technical_requirements)
            score_components.append(("technical", tech_score, 0.4))
        
        # Check industry experience
        industry_match = 0
        for industry in profile.target_industries:
            if industry.lower() in grant.description.lower():
                industry_match += 1
                strengths.append(f"Industry experience: {industry}")
        
        if profile.target_industries:
            industry_score = min(industry_match / len(profile.target_industries), 1.0)
            score_components.append(("industry", industry_score, 0.2))
        
        # Check funding range fit
        funding_fit = 0
        if (profile.preferred_funding_range["min"] <= grant.funding_amount <= 
            profile.preferred_funding_range["max"]):
            funding_fit = 1.0
            strengths.append("Funding amount within preferred range")
        elif grant.funding_amount < profile.preferred_funding_range["min"]:
            funding_fit = 0.5
            gaps.append("Grant amount below preferred minimum")
        else:
            funding_fit = 0.3
            gaps.append("Grant amount above preferred maximum")
        
        score_components.append(("funding", funding_fit, 0.2))
        
        # Check complexity preference
        complexity_fit = 0
        if grant.complexity_level == profile.complexity_preference:
            complexity_fit = 1.0
            strengths.append("Complexity level matches preference")
        elif (grant.complexity_level == ComplexityLevel.MEDIUM and 
              profile.complexity_preference == ComplexityLevel.SIMPLE):
            complexity_fit = 0.6
            gaps.append("Higher complexity than preferred")
        else:
            complexity_fit = 0.3
            gaps.append("Complexity mismatch")
        
        score_components.append(("complexity", complexity_fit, 0.2))
        
        # Calculate overall match score
        match_score = sum(score * weight for _, score, weight in score_components)
        match_score = min(max(match_score * 100, 0), 100)  # Scale to 0-100
        
        return match_score, strengths, gaps
    
    def _generate_recommendations(
        self,
        grant: Grant,
        profile: BusinessProfile,
        requirements: RequirementAnalysis,
        gaps: List[str]
    ) -> List[str]:
        """Generate actionable recommendations for the application."""
        
        recommendations = []
        
        # Address technical gaps
        tech_gaps = [gap for gap in gaps if "Technical gap" in gap]
        if tech_gaps:
            recommendations.append(
                "Consider partnering with organizations that have the missing technical expertise, "
                "or highlight transferable skills from your current technology stack."
            )
        
        # Consortium recommendations
        if requirements.consortium_requirements and requirements.consortium_requirements.get("required"):
            recommendations.append(
                f"Form a consortium with {requirements.consortium_requirements['min_partners']} partners. "
                f"Target partner types: {', '.join(requirements.consortium_requirements['partner_types'])}"
            )
        
        # Budget recommendations
        if grant.funding_amount > profile.preferred_funding_range["max"]:
            recommendations.append(
                "Consider scaling down the project scope to match your preferred funding range, "
                "or partner with larger organizations to handle the increased project size."
            )
        
        # Industry-specific recommendations
        if "healthcare" in grant.description.lower():
            recommendations.append(
                "Emphasize any healthcare-related projects or partnerships. "
                "Consider collaborating with medical institutions to strengthen your application."
            )
        
        if "ai" in grant.description.lower() or "artificial intelligence" in grant.description.lower():
            recommendations.append(
                "Highlight specific AI use cases and demonstrate measurable impact. "
                "Include technical architecture diagrams and proof-of-concept results if available."
            )
        
        # Timeline recommendations
        days_until_deadline = (grant.deadline - date.today()).days
        if days_until_deadline < 30:
            recommendations.append(
                "⚠️ Tight deadline! Prioritize completing mandatory sections first. "
                "Consider requesting deadline extension if available."
            )
        elif days_until_deadline < 60:
            recommendations.append(
                "Moderate timeline available. Start with proposal outline and consortium formation."
            )
        
        return recommendations
    
    def _create_application_timeline(self, grant: Grant) -> List[Dict[str, Any]]:
        """Create a detailed timeline for the application process."""
        
        days_until_deadline = (grant.deadline - date.today()).days
        timeline = []
        
        if days_until_deadline > 60:
            timeline.extend([
                {
                    "phase": "Preparation (Weeks 1-2)",
                    "tasks": [
                        "Analyze grant requirements in detail",
                        "Assess internal capabilities and identify gaps",
                        "Research potential partners and competitors"
                    ],
                    "priority": "High"
                },
                {
                    "phase": "Consortium Building (Weeks 3-4)",
                    "tasks": [
                        "Identify and contact potential partners",
                        "Define roles and responsibilities",
                        "Draft consortium agreement"
                    ],
                    "priority": "High"
                },
                {
                    "phase": "Proposal Development (Weeks 5-7)",
                    "tasks": [
                        "Develop technical approach and methodology",
                        "Create detailed work packages and timeline",
                        "Prepare budget and resource allocation"
                    ],
                    "priority": "Critical"
                },
                {
                    "phase": "Review and Submission (Week 8)",
                    "tasks": [
                        "Internal review and quality check",
                        "Partner review and approval",
                        "Final submission and documentation"
                    ],
                    "priority": "Critical"
                }
            ])
        else:
            # Accelerated timeline for tight deadlines
            timeline.extend([
                {
                    "phase": "Immediate Actions (Days 1-3)",
                    "tasks": [
                        "Complete eligibility check",
                        "Gather required documents",
                        "Contact key partners if consortium needed"
                    ],
                    "priority": "Critical"
                },
                {
                    "phase": "Core Development (Days 4-10)",
                    "tasks": [
                        "Draft technical sections",
                        "Prepare budget outline",
                        "Complete mandatory forms"
                    ],
                    "priority": "Critical"
                },
                {
                    "phase": "Finalization (Final 3 days)",
                    "tasks": [
                        "Review and polish application",
                        "Submit before deadline",
                        "Prepare for potential follow-up questions"
                    ],
                    "priority": "Critical"
                }
            ])
        
        return timeline
    
    def _estimate_application_effort(
        self, 
        grant: Grant, 
        requirements: RequirementAnalysis
    ) -> str:
        """Estimate the effort required for the application."""
        
        base_effort = 40  # Base hours for simple applications
        
        # Adjust based on grant size
        if grant.funding_amount > 1000000:
            base_effort += 80
        elif grant.funding_amount > 500000:
            base_effort += 40
        elif grant.funding_amount > 100000:
            base_effort += 20
        
        # Adjust based on consortium requirements
        if (requirements.consortium_requirements and 
            requirements.consortium_requirements.get("required")):
            base_effort += 30
        
        # Adjust based on technical complexity
        if len(requirements.technical_requirements) > 5:
            base_effort += 20
        
        if base_effort < 60:
            return f"{base_effort} hours (1-2 weeks with 1 person)"
        elif base_effort < 120:
            return f"{base_effort} hours (2-3 weeks with 1 person, or 1-2 weeks with 2 people)"
        else:
            return f"{base_effort} hours (1+ months, requires team effort)"
    
    def _estimate_success_probability(
        self, 
        match_score: float, 
        complexity: ComplexityLevel, 
        profile: BusinessProfile
    ) -> str:
        """Estimate the probability of application success."""
        
        base_prob = match_score / 100  # Start with match score as probability
        
        # Adjust based on complexity vs preference
        if complexity == profile.complexity_preference:
            base_prob += 0.1
        elif complexity == ComplexityLevel.COMPLEX:
            base_prob -= 0.2
        
        # Adjust based on company size (SMEs often preferred)
        if profile.company_size == "small":
            base_prob += 0.1
        
        base_prob = min(max(base_prob, 0.1), 0.9)  # Keep between 10-90%
        
        if base_prob > 0.7:
            return f"High ({base_prob:.0%}) - Strong alignment with requirements"
        elif base_prob > 0.4:
            return f"Medium ({base_prob:.0%}) - Good potential with some gaps to address"
        else:
            return f"Low ({base_prob:.0%}) - Significant gaps, consider partnership or skip"
    
    def _generate_strategic_advice(
        self, 
        grant: Grant, 
        profile: BusinessProfile, 
        match_score: float
    ) -> str:
        """Generate high-level strategic advice for the application."""
        
        advice_parts = []
        
        if match_score > 70:
            advice_parts.append(
                "🎯 **Strong Fit**: This grant aligns well with your capabilities. "
                "Focus on highlighting your unique value proposition and past successes."
            )
        elif match_score > 50:
            advice_parts.append(
                "⚖️ **Moderate Fit**: Consider strengthening your application through partnerships "
                "or by emphasizing transferable skills from related projects."
            )
        else:
            advice_parts.append(
                "⚠️ **Challenging Fit**: This grant has significant gaps. "
                "Consider whether the effort is justified or focus on better-matched opportunities."
            )
        
        # Program-specific advice
        if grant.program.value == "horizon_europe":
            advice_parts.append(
                "📊 **Horizon Europe Focus**: Emphasize innovation, impact, and European added value. "
                "Strong consortium and clear commercialization path are crucial."
            )
        
        # Funding amount advice
        if grant.funding_amount > profile.preferred_funding_range["max"]:
            advice_parts.append(
                "💰 **Large Grant Strategy**: Consider this as an opportunity to scale up operations. "
                "Ensure you have the capacity to manage increased project complexity."
            )
        
        return "\n\n".join(advice_parts)
    
    def _get_required_documents(
        self, 
        grant: Grant, 
        requirements: RequirementAnalysis
    ) -> List[str]:
        """Get list of required documents for the application."""
        
        documents = [
            "Grant application form (mandatory sections completed)",
            "Technical proposal with detailed methodology",
            "Budget breakdown and justification",
            "Company profile and capability statement"
        ]
        
        # Add consortium-specific documents
        if (requirements.consortium_requirements and 
            requirements.consortium_requirements.get("required")):
            documents.extend([
                "Consortium agreement draft",
                "Partner commitment letters",
                "Partner capability statements"
            ])
        
        # Add program-specific documents
        if grant.program.value == "horizon_europe":
            documents.extend([
                "Ethics self-assessment",
                "Data management plan",
                "Dissemination and exploitation plan"
            ])
        
        # Add compliance documents for healthcare/regulated industries
        if "healthcare" in grant.description.lower():
            documents.extend([
                "Regulatory compliance statement",
                "Data privacy impact assessment"
            ])
        
        return documents
    
    def display_guidance(self, guidance: ApplicationGuidance) -> None:
        """Display the application guidance in a formatted, readable way."""
        
        # Main header
        self.console.print(Panel(
            f"📋 Application Assistance for Grant: {guidance.grant_id}",
            style="bold blue"
        ))
        
        # Match score and probability
        match_color = "green" if guidance.match_score >= 70 else "yellow" if guidance.match_score >= 50 else "red"
        self.console.print(Panel(
            f"🎯 **Match Score**: [{match_color}]{guidance.match_score:.1f}%[/]\n"
            f"📈 **Success Probability**: {guidance.success_probability}\n"
            f"⏱️  **Estimated Effort**: {guidance.estimated_effort}",
            title="Quick Assessment"
        ))
        
        # Strengths and Gaps
        strengths_text = "\n".join([f"✅ {strength}" for strength in guidance.strengths])
        gaps_text = "\n".join([f"❌ {gap}" for gap in guidance.gaps])
        
        self.console.print(Panel(
            f"**Strengths:**\n{strengths_text}\n\n**Areas to Address:**\n{gaps_text}",
            title="Capability Analysis"
        ))
        
        # Recommendations
        recommendations_text = "\n".join([f"• {rec}" for rec in guidance.recommendations])
        self.console.print(Panel(
            recommendations_text,
            title="💡 Recommendations"
        ))
        
        # Timeline
        timeline_table = Table(show_header=True, header_style="bold magenta")
        timeline_table.add_column("Phase", style="cyan", no_wrap=True)
        timeline_table.add_column("Tasks", style="white")
        timeline_table.add_column("Priority", justify="center")
        
        for phase in guidance.timeline:
            tasks = "\n".join([f"• {task}" for task in phase["tasks"]])
            priority_style = "red" if phase["priority"] == "Critical" else "yellow"
            timeline_table.add_row(
                phase["phase"],
                tasks,
                f"[{priority_style}]{phase['priority']}[/]"
            )
        
        self.console.print(Panel(timeline_table, title="📅 Application Timeline"))
        
        # Required documents
        docs_text = "\n".join([f"📄 {doc}" for doc in guidance.required_documents])
        self.console.print(Panel(
            docs_text,
            title="📋 Required Documents"
        ))
        
        # Strategic advice
        self.console.print(Panel(
            Markdown(guidance.strategic_advice),
            title="🎯 Strategic Advice"
        ))
        
        self.console.print("\n" + "="*80 + "\n")
        self.console.print(
            "[bold green]💡 Tip:[/] Save this guidance and refer to it throughout your application process!"
        )
    
    async def generate_complete_application(
        self, 
        grant: Grant, 
        business_profile: BusinessProfile,
        interactive: bool = True
    ) -> Dict[str, Any]:
        """Generate a complete, ready-to-submit grant application.
        
        Args:
            grant: Grant opportunity to apply for
            business_profile: Business profile for the application
            interactive: Whether to prompt user for input
            
        Returns:
            Dictionary containing all generated application materials
        """
        logger.info(f"Starting complete application generation for grant {grant.id}")
        
        self.console.print(Panel(
            f"🚀 Generating Complete Application Package for {grant.id}",
            style="bold blue"
        ))
        
        try:
            # Step 1: Document Analysis
            self.console.print("📄 Step 1: Analyzing grant documents...")
            async with DocumentAnalyzer(self.config) as doc_analyzer:
                document_package = await doc_analyzer.analyze_grant_documents(grant)
            
            logger.info(f"Analyzed {len(document_package.documents)} documents")
            
            # Step 2: Company Research
            self.console.print("🔍 Step 2: Researching company information...")
            async with WebResearcher(self.config) as web_researcher:
                company_info = await web_researcher.research_company(business_profile)
            
            logger.info(f"Researched company: {company_info.name}")
            
            # Step 3: Form Pre-filling
            self.console.print("📝 Step 3: Pre-filling application forms...")
            form_prefiller = FormPrefiller(self.config)
            prefilled_forms = form_prefiller.prefill_all_forms(
                document_package, company_info, business_profile, grant
            )
            
            total_completion = sum(f.completion_percentage for f in prefilled_forms) / len(prefilled_forms) if prefilled_forms else 0
            logger.info(f"Pre-filled {len(prefilled_forms)} forms with {total_completion:.1f}% completion")
            
            # Step 4: Interactive User Input (if enabled)
            user_responses = {}
            if interactive:
                self.console.print("👤 Step 4: Collecting additional information...")
                user_prompter = UserPrompter(self.config)
                user_responses = user_prompter.collect_missing_information(
                    prefilled_forms, grant.title
                )
                logger.info(f"Collected {len(user_responses)} user responses")
                
                # Apply user responses to forms
                self._apply_user_responses(prefilled_forms, user_responses)
            else:
                self.console.print("⚠️ Skipping interactive input (non-interactive mode)")
            
            # Step 5: Document Generation
            self.console.print("📋 Step 5: Generating final application documents...")
            document_generator = DocumentGenerator(self.config)
            generated_documents = document_generator.generate_all_documents(
                prefilled_forms, grant
            )
            
            logger.info(f"Generated {len(generated_documents)} application documents")
            
            # Step 6: Final Summary
            self._display_generation_summary(
                grant, prefilled_forms, generated_documents, user_responses
            )
            
            return {
                "grant": grant,
                "document_package": document_package,
                "company_info": company_info,
                "prefilled_forms": prefilled_forms,
                "user_responses": user_responses,
                "generated_documents": generated_documents,
                "completion_summary": {
                    "overall_completion": total_completion,
                    "forms_count": len(prefilled_forms),
                    "documents_count": len(generated_documents),
                    "user_inputs_count": len(user_responses)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating complete application: {e}")
            self.console.print(f"❌ Error generating application: {e}", style="bold red")
            raise
    
    def _apply_user_responses(
        self, 
        prefilled_forms: List[PrefilledForm], 
        user_responses: Dict[str, UserResponse]
    ):
        """Apply user responses to pre-filled forms.
        
        Args:
            prefilled_forms: List of pre-filled forms to update
            user_responses: User responses to apply
        """
        for form in prefilled_forms:
            for field in form.fields:
                if field.field_name in user_responses:
                    user_response = user_responses[field.field_name]
                    field.prefilled_value = user_response.response
                    field.confidence = user_response.confidence
                    field.needs_user_input = False
                    field.user_prompt = None
            
            # Recalculate completion percentage
            completed_fields = sum(1 for f in form.fields if f.prefilled_value and f.confidence > 0.7)
            form.completion_percentage = (completed_fields / len(form.fields)) * 100 if form.fields else 0
            
            # Update user input required list
            form.user_input_required = [f for f in form.fields if f.needs_user_input]
    
    def _display_generation_summary(
        self,
        grant: Grant,
        prefilled_forms: List[PrefilledForm],
        generated_documents: List[GeneratedDocument],
        user_responses: Dict[str, UserResponse]
    ):
        """Display comprehensive summary of application generation.
        
        Args:
            grant: Grant information
            prefilled_forms: Pre-filled forms
            generated_documents: Generated documents
            user_responses: User responses
        """
        self.console.print("\n" + "=" * 80)
        self.console.print("[bold green]🎉 APPLICATION GENERATION COMPLETE![/bold green]")
        self.console.print("=" * 80)
        
        # Overall statistics
        total_fields = sum(len(form.fields) for form in prefilled_forms)
        completed_fields = sum(
            len([f for f in form.fields if f.prefilled_value and f.confidence > 0.7])
            for form in prefilled_forms
        )
        overall_completion = (completed_fields / total_fields * 100) if total_fields > 0 else 0
        
        stats_table = Table(title="Application Statistics", show_header=True)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Grant", grant.title)
        stats_table.add_row("Grant ID", grant.id)
        stats_table.add_row("Overall Completion", f"{overall_completion:.1f}%")
        stats_table.add_row("Forms Generated", str(len(prefilled_forms)))
        stats_table.add_row("Documents Created", str(len(generated_documents)))
        stats_table.add_row("User Inputs Collected", str(len(user_responses)))
        stats_table.add_row("Total Fields Processed", str(total_fields))
        
        self.console.print(stats_table)
        
        # Document details
        docs_table = Table(title="Generated Documents", show_header=True)
        docs_table.add_column("Document", style="white")
        docs_table.add_column("Type", style="yellow")
        docs_table.add_column("Status", style="white")
        docs_table.add_column("Size", justify="right", style="cyan")
        
        for doc in generated_documents:
            status_style = {
                "complete": "[green]Complete[/]",
                "needs_review": "[yellow]Needs Review[/]",
                "missing_data": "[red]Missing Data[/]"
            }.get(doc.completion_status, doc.completion_status)
            
            size_kb = doc.size_bytes / 1024
            size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
            
            docs_table.add_row(
                doc.document_name,
                doc.file_type.upper(),
                status_style,
                size_str
            )
        
        self.console.print(docs_table)
        
        # Output location
        if generated_documents:
            output_dir = Path(generated_documents[0].file_path).parent
            self.console.print(Panel(
                f"📁 **Application files saved to:**\n{output_dir}",
                title="Output Location",
                style="blue"
            ))
        
        # Next steps
        next_steps = """🎯 **Next Steps:**

1. **Review Generated Documents**: Open the application files and verify all information
2. **Complete Missing Fields**: Address any fields marked as "needs review"
3. **Gather Supporting Documents**: Collect required certificates, CVs, and statements
4. **Quality Check**: Have a colleague review the application for accuracy
5. **Submit Application**: Upload to the official EU portal before the deadline

💡 **Pro Tips:**
• All forms are pre-filled with researched company data
• Yellow highlighted fields need your attention
• Keep copies of everything you submit
• Submit at least 24 hours before the deadline"""
        
        self.console.print(Panel(
            next_steps,
            title="Final Instructions",
            style="green"
        ))
        
        deadline_days = (grant.deadline - date.today()).days
        deadline_color = "red" if deadline_days < 30 else "yellow" if deadline_days < 60 else "green"
        
        self.console.print(f"\n⏰ **Deadline**: [{deadline_color}]{grant.deadline.strftime('%Y-%m-%d')} ({deadline_days} days remaining)[/]")
        self.console.print(f"🔗 **Grant URL**: {grant.url}")
        
        self.console.print("\n" + "=" * 80)
        self.console.print("[bold blue]Good luck with your EU grant application! 🚀[/bold blue]")
        self.console.print("=" * 80)
