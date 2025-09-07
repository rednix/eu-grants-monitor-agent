"""
Form Pre-filler Service for EU Grant Applications.

This service intelligently pre-fills grant application forms
using researched company data and intelligent field mapping.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from loguru import logger

from ..data.models import Grant, BusinessProfile
from .web_researcher import CompanyInfo
from .document_analyzer import GrantDocumentPackage, DocumentInfo


@dataclass
class FormField:
    """Represents a form field with pre-filled data."""
    
    field_name: str
    field_type: str = "text"
    prefilled_value: Optional[str] = None
    confidence: float = 0.0
    needs_user_input: bool = False
    user_prompt: Optional[str] = None
    options: List[str] = None


@dataclass
class PrefilledForm:
    """A complete pre-filled application form."""
    
    form_name: str
    document_info: DocumentInfo
    fields: List[FormField]
    completion_percentage: float
    missing_critical_fields: List[str]
    user_input_required: List[FormField]


class FormPrefiller:
    """Intelligently pre-fills grant application forms."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the form prefiller."""
        self.config = config
        logger.info("FormPrefiller initialized")
    
    def prefill_all_forms(
        self,
        document_package: GrantDocumentPackage,
        company_info: CompanyInfo,
        business_profile: BusinessProfile,
        grant: Grant
    ) -> List[PrefilledForm]:
        """Pre-fill all application forms for a grant."""
        logger.info(f"Pre-filling forms for grant {grant.id}")
        
        prefilled_forms = []
        
        for form_doc in document_package.application_forms:
            try:
                prefilled_form = self._prefill_single_form(
                    form_doc, company_info, business_profile, grant, document_package
                )
                prefilled_forms.append(prefilled_form)
                logger.info(f"Pre-filled form: {form_doc.filename} ({prefilled_form.completion_percentage:.1f}% complete)")
            except Exception as e:
                logger.error(f"Error pre-filling form {form_doc.filename}: {e}")
        
        return prefilled_forms
    
    def _prefill_single_form(
        self,
        form_doc: DocumentInfo,
        company_info: CompanyInfo,
        business_profile: BusinessProfile,
        grant: Grant,
        document_package: GrantDocumentPackage
    ) -> PrefilledForm:
        """Pre-fill a single application form."""
        prefilled_fields = []
        
        for field_name in form_doc.form_fields:
            field = self._prefill_field(field_name, company_info, business_profile, grant)
            prefilled_fields.append(field)
        
        # Calculate completion percentage
        completed_fields = sum(1 for f in prefilled_fields if f.prefilled_value and f.confidence > 0.7)
        completion_percentage = (completed_fields / len(prefilled_fields)) * 100 if prefilled_fields else 0
        
        # Identify missing critical fields
        critical_fields = ['organization_name', 'project_title', 'total_budget', 'contact_email']
        missing_critical = []
        for field in prefilled_fields:
            if field.field_name in critical_fields and (not field.prefilled_value or field.confidence < 0.5):
                missing_critical.append(field.field_name)
        
        # Identify fields needing user input
        user_input_needed = [f for f in prefilled_fields if f.needs_user_input]
        
        return PrefilledForm(
            form_name=form_doc.filename,
            document_info=form_doc,
            fields=prefilled_fields,
            completion_percentage=completion_percentage,
            missing_critical_fields=missing_critical,
            user_input_required=user_input_needed
        )
    
    def _prefill_field(
        self,
        field_name: str,
        company_info: CompanyInfo,
        business_profile: BusinessProfile,
        grant: Grant
    ) -> FormField:
        """Pre-fill a single form field."""
        field = FormField(field_name=field_name)
        
        # Simple field mapping
        if field_name == 'organization_name':
            field.prefilled_value = company_info.name
            field.confidence = 0.95
        
        elif field_name == 'country':
            field.prefilled_value = business_profile.country
            field.confidence = 0.95
        
        elif field_name == 'organization_type':
            field.field_type = "select"
            field.options = ['Micro Enterprise (1-9 employees)', 'Small Enterprise (10-49 employees)', 'Medium Enterprise (50-249 employees)']
            size_mapping = {
                'micro': 'Micro Enterprise (1-9 employees)',
                'small': 'Small Enterprise (10-49 employees)',
                'medium': 'Medium Enterprise (50-249 employees)'
            }
            field.prefilled_value = size_mapping.get(business_profile.company_size, 'Small Enterprise (10-49 employees)')
            field.confidence = 0.9
        
        elif field_name == 'contact_email':
            field.field_type = "email"
            if company_info.contact_info and 'email' in company_info.contact_info:
                field.prefilled_value = company_info.contact_info['email']
                field.confidence = 0.9
            else:
                field.needs_user_input = True
                field.user_prompt = "Please provide the project contact email address"
        
        elif field_name == 'project_title':
            # Generate intelligent project title
            expertise = business_profile.ai_expertise[0] if business_profile.ai_expertise else "AI"
            domain = self._extract_domain_from_grant(grant)
            field.prefilled_value = f"Advanced {expertise.replace('_', ' ').title()} Solutions for {domain}"
            field.confidence = 0.7
            field.needs_user_input = True
            field.user_prompt = "Please review and customize the project title"
        
        elif field_name == 'project_summary':
            field.field_type = "textarea"
            expertise_str = ", ".join(business_profile.ai_expertise[:3])
            industry = business_profile.target_industries[0] if business_profile.target_industries else "technology"
            
            field.prefilled_value = f"This project leverages {company_info.name}'s expertise in {expertise_str} to develop innovative solutions for the {industry} sector. Our approach combines cutting-edge AI technologies with practical applications, ensuring scalable and sustainable outcomes."
            field.confidence = 0.6
            field.needs_user_input = True
            field.user_prompt = "Please customize this summary with your specific technical approach"
        
        elif field_name == 'total_budget':
            field.field_type = "number"
            suggested_budget = min(grant.funding_amount * 0.8, business_profile.preferred_funding_range["max"])
            field.prefilled_value = str(int(suggested_budget))
            field.confidence = 0.7
            field.needs_user_input = True
            field.user_prompt = "Please adjust based on actual project scope"
        
        elif field_name == 'start_date':
            field.field_type = "date"
            suggested_start = grant.deadline + timedelta(days=90)
            field.prefilled_value = suggested_start.strftime("%Y-%m-%d")
            field.confidence = 0.8
        
        elif field_name == 'duration_months':
            field.field_type = "number"
            if grant.funding_amount > 500000:
                duration = min(36, business_profile.max_project_duration_months)
            else:
                duration = min(24, business_profile.max_project_duration_months)
            field.prefilled_value = str(duration)
            field.confidence = 0.7
        
        elif field_name in ['personnel_costs', 'equipment_costs', 'travel_costs', 'other_costs', 'indirect_costs', 'total_costs']:
            field.field_type = "number"
            budget = min(grant.funding_amount * 0.8, business_profile.preferred_funding_range["max"])
            
            if field_name == 'personnel_costs':
                field.prefilled_value = str(int(budget * 0.65))
            elif field_name == 'equipment_costs':
                field.prefilled_value = str(int(budget * 0.12))
            elif field_name == 'travel_costs':
                field.prefilled_value = str(int(budget * 0.04))
            elif field_name == 'other_costs':
                field.prefilled_value = str(int(budget * 0.06))
            elif field_name == 'indirect_costs':
                field.prefilled_value = str(int(budget * 0.8 * 0.25))  # 25% of direct costs
            else:  # total_costs
                field.prefilled_value = str(int(budget))
            
            field.confidence = 0.7
        
        return field
    
    def _extract_domain_from_grant(self, grant: Grant) -> str:
        """Extract domain from grant information."""
        if 'healthcare' in grant.description.lower():
            return "Healthcare"
        elif 'manufacturing' in grant.description.lower():
            return "Manufacturing"
        elif 'education' in grant.description.lower():
            return "Education"
        elif 'environment' in grant.description.lower():
            return "Environmental"
        else:
            return "Technology"
