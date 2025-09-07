"""
Document Generator Service for EU Grant Applications.

This service generates completed, ready-to-sign application documents
from pre-filled form data.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from loguru import logger

from .form_prefiller import PrefilledForm, FormField
from ..data.models import Grant


@dataclass
class GeneratedDocument:
    """Information about a generated document."""
    
    document_name: str
    file_path: str
    file_type: str
    size_bytes: int
    completion_status: str  # "complete", "needs_review", "missing_data"
    missing_fields: List[str]
    generated_at: datetime


class DocumentGenerator:
    """Generates completed application documents."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the document generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.output_dir = Path("generated_applications")
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"DocumentGenerator initialized with output dir: {self.output_dir}")
    
    def generate_all_documents(
        self,
        prefilled_forms: List[PrefilledForm],
        grant: Grant
    ) -> List[GeneratedDocument]:
        """Generate all application documents.
        
        Args:
            prefilled_forms: List of pre-filled forms
            grant: Grant information
            
        Returns:
            List of generated documents
        """
        logger.info(f"Generating application documents for grant {grant.id}")
        
        generated_docs = []
        
        # Create grant-specific directory
        grant_dir = self.output_dir / f"{grant.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        grant_dir.mkdir(exist_ok=True)
        
        for form in prefilled_forms:
            try:
                generated_doc = self._generate_single_document(form, grant, grant_dir)
                generated_docs.append(generated_doc)
                logger.info(f"Generated document: {generated_doc.document_name}")
            except Exception as e:
                logger.error(f"Error generating document for {form.form_name}: {e}")
        
        # Generate summary document
        summary_doc = self._generate_application_summary(prefilled_forms, grant, grant_dir)
        generated_docs.append(summary_doc)
        
        # Generate user instruction document
        instructions_doc = self._generate_user_instructions(prefilled_forms, grant, grant_dir)
        generated_docs.append(instructions_doc)
        
        return generated_docs
    
    def _generate_single_document(
        self,
        form: PrefilledForm,
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate a single application document.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        # Determine file format based on original document
        if form.document_info.file_type == "pdf":
            return self._generate_pdf_form(form, grant, output_dir)
        elif form.document_info.file_type == "xlsx":
            return self._generate_excel_form(form, grant, output_dir)
        else:
            return self._generate_text_form(form, grant, output_dir)
    
    def _generate_pdf_form(
        self,
        form: PrefilledForm,
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate a PDF application form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        # For demonstration, we'll generate an HTML version that can be printed to PDF
        html_content = self._generate_html_form(form, grant)
        
        file_name = f"{form.form_name.replace('.pdf', '')}_completed.html"
        file_path = output_dir / file_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        file_size = file_path.stat().st_size
        
        # Determine completion status
        completion_status = "complete"
        if form.missing_critical_fields:
            completion_status = "missing_data"
        elif form.user_input_required:
            completion_status = "needs_review"
        
        return GeneratedDocument(
            document_name=file_name,
            file_path=str(file_path),
            file_type="html",
            size_bytes=file_size,
            completion_status=completion_status,
            missing_fields=form.missing_critical_fields,
            generated_at=datetime.now()
        )
    
    def _generate_excel_form(
        self,
        form: PrefilledForm,
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate an Excel budget form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        # Generate CSV format for budget data
        csv_content = self._generate_csv_budget(form, grant)
        
        file_name = f"{form.form_name.replace('.xlsx', '')}_completed.csv"
        file_path = output_dir / file_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        file_size = file_path.stat().st_size
        
        completion_status = "complete"
        if form.missing_critical_fields:
            completion_status = "missing_data"
        elif form.user_input_required:
            completion_status = "needs_review"
        
        return GeneratedDocument(
            document_name=file_name,
            file_path=str(file_path),
            file_type="csv",
            size_bytes=file_size,
            completion_status=completion_status,
            missing_fields=form.missing_critical_fields,
            generated_at=datetime.now()
        )
    
    def _generate_text_form(
        self,
        form: PrefilledForm,
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate a text-based form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        text_content = self._generate_text_content(form, grant)
        
        file_name = f"{form.form_name}_completed.txt"
        file_path = output_dir / file_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        file_size = file_path.stat().st_size
        
        completion_status = "complete"
        if form.missing_critical_fields:
            completion_status = "missing_data"
        elif form.user_input_required:
            completion_status = "needs_review"
        
        return GeneratedDocument(
            document_name=file_name,
            file_path=str(file_path),
            file_type="txt",
            size_bytes=file_size,
            completion_status=completion_status,
            missing_fields=form.missing_critical_fields,
            generated_at=datetime.now()
        )
    
    def _generate_html_form(self, form: PrefilledForm, grant: Grant) -> str:
        """Generate HTML content for a form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            
        Returns:
            HTML content string
        """
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{form.form_name} - {grant.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .form-section {{ margin-bottom: 30px; }}
        .field {{ margin-bottom: 15px; }}
        .field-label {{ font-weight: bold; display: inline-block; min-width: 200px; }}
        .field-value {{ display: inline-block; padding: 5px; border-bottom: 1px solid #ccc; min-width: 300px; }}
        .needs-attention {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; }}
        .textarea-field {{ width: 100%; min-height: 100px; }}
        .signature-section {{ margin-top: 50px; }}
        .signature-line {{ border-bottom: 1px solid #000; width: 300px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>EU Grant Application Form</h1>
        <h2>{grant.title}</h2>
        <h3>Grant ID: {grant.id}</h3>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="form-content">
"""
        
        for field in form.fields:
            field_html = self._generate_field_html(field)
            html_template += field_html
        
        # Add user attention section if needed
        if form.user_input_required:
            html_template += """
    <div class="needs-attention">
        <h3>⚠️ Fields Requiring Your Attention:</h3>
        <ul>
"""
            for field in form.user_input_required:
                html_template += f"<li><strong>{field.field_name}:</strong> {field.user_prompt}</li>\\n"
            
            html_template += """
        </ul>
    </div>
"""
        
        html_template += """
    <div class="signature-section">
        <h3>Signatures</h3>
        <p>Project Coordinator:</p>
        <div class="signature-line"></div>
        <p>Date: _______________</p>
        
        <p>Legal Representative:</p>
        <div class="signature-line"></div>
        <p>Date: _______________</p>
    </div>
    
    </div>
</body>
</html>
"""
        
        return html_template
    
    def _generate_field_html(self, field: FormField) -> str:
        """Generate HTML for a single field.
        
        Args:
            field: Form field to generate HTML for
            
        Returns:
            HTML string for the field
        """
        field_class = "field"
        if field.needs_user_input:
            field_class += " needs-attention"
        
        if field.field_type == "textarea":
            return f"""
        <div class="{field_class}">
            <div class="field-label">{field.field_name.replace('_', ' ').title()}:</div>
            <br>
            <textarea class="textarea-field">{field.prefilled_value or '[PLEASE FILL]'}</textarea>
            {f'<p><em>Note: {field.user_prompt}</em></p>' if field.user_prompt else ''}
        </div>
"""
        else:
            return f"""
        <div class="{field_class}">
            <span class="field-label">{field.field_name.replace('_', ' ').title()}:</span>
            <span class="field-value">{field.prefilled_value or '[PLEASE FILL]'}</span>
            {f'<p><em>Note: {field.user_prompt}</em></p>' if field.user_prompt else ''}
        </div>
"""
    
    def _generate_csv_budget(self, form: PrefilledForm, grant: Grant) -> str:
        """Generate CSV content for budget form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            
        Returns:
            CSV content string
        """
        csv_content = f"EU Grant Budget Template - {grant.title}\\n"
        csv_content += f"Grant ID: {grant.id}\\n"
        csv_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
        csv_content += "Category,Amount (EUR),Notes\\n"
        
        for field in form.fields:
            if field.field_type == "number" and field.prefilled_value:
                csv_content += f"{field.field_name.replace('_', ' ').title()},{field.prefilled_value},{field.user_prompt or ''}\\n"
        
        return csv_content
    
    def _generate_text_content(self, form: PrefilledForm, grant: Grant) -> str:
        """Generate text content for form.
        
        Args:
            form: Pre-filled form data
            grant: Grant information
            
        Returns:
            Text content string
        """
        content = f"""
EU GRANT APPLICATION FORM
=========================

Grant: {grant.title}
Grant ID: {grant.id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Completion: {form.completion_percentage:.1f}%

FORM DATA:
----------

"""
        
        for field in form.fields:
            content += f"{field.field_name.replace('_', ' ').title()}:\\n"
            content += f"  Value: {field.prefilled_value or '[PLEASE FILL]'}\\n"
            if field.user_prompt:
                content += f"  Note: {field.user_prompt}\\n"
            content += "\\n"
        
        if form.user_input_required:
            content += "\\nFIELDS REQUIRING ATTENTION:\\n"
            content += "-" * 30 + "\\n"
            for field in form.user_input_required:
                content += f"• {field.field_name}: {field.user_prompt}\\n"
        
        return content
    
    def _generate_application_summary(
        self,
        prefilled_forms: List[PrefilledForm],
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate application summary document.
        
        Args:
            prefilled_forms: List of pre-filled forms
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        total_fields = sum(len(form.fields) for form in prefilled_forms)
        completed_fields = sum(
            len([f for f in form.fields if f.prefilled_value and f.confidence > 0.7])
            for form in prefilled_forms
        )
        overall_completion = (completed_fields / total_fields * 100) if total_fields > 0 else 0
        
        summary_content = f"""
EU GRANT APPLICATION SUMMARY
============================

Grant: {grant.title}
Grant ID: {grant.id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

COMPLETION OVERVIEW:
-------------------
Overall Completion: {overall_completion:.1f}%
Total Fields: {total_fields}
Completed Fields: {completed_fields}
Forms Generated: {len(prefilled_forms)}

FORM DETAILS:
------------
"""
        
        for form in prefilled_forms:
            summary_content += f"""
{form.form_name}:
  - Completion: {form.completion_percentage:.1f}%
  - Missing Critical Fields: {len(form.missing_critical_fields)}
  - User Input Required: {len(form.user_input_required)}
"""
        
        all_missing = []
        all_user_input = []
        
        for form in prefilled_forms:
            all_missing.extend(form.missing_critical_fields)
            all_user_input.extend([f.field_name for f in form.user_input_required])
        
        if all_missing:
            summary_content += f"""
CRITICAL MISSING DATA:
---------------------
{chr(10).join(f"• {field}" for field in set(all_missing))}
"""
        
        if all_user_input:
            summary_content += f"""
FIELDS REQUIRING YOUR INPUT:
---------------------------
{chr(10).join(f"• {field}" for field in set(all_user_input))}
"""
        
        summary_content += f"""

NEXT STEPS:
----------
1. Review all generated forms in this folder
2. Complete any fields marked as requiring attention
3. Print or save forms as PDF for official submission
4. Gather any required supporting documents
5. Submit before deadline: {grant.deadline.strftime('%Y-%m-%d')}

SUPPORTING DOCUMENTS NEEDED:
---------------------------
• Company registration documents
• Financial statements (last 2 years)
• CVs of key personnel
• Letters of intent from partners (if consortium)
• Ethics self-assessment (if applicable)
• Data management plan (if applicable)

Generated by EU Grants Monitor Agent
"""
        
        file_path = output_dir / "APPLICATION_SUMMARY.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        return GeneratedDocument(
            document_name="APPLICATION_SUMMARY.txt",
            file_path=str(file_path),
            file_type="txt",
            size_bytes=file_path.stat().st_size,
            completion_status="complete",
            missing_fields=[],
            generated_at=datetime.now()
        )
    
    def _generate_user_instructions(
        self,
        prefilled_forms: List[PrefilledForm],
        grant: Grant,
        output_dir: Path
    ) -> GeneratedDocument:
        """Generate user instruction document.
        
        Args:
            prefilled_forms: List of pre-filled forms
            grant: Grant information
            output_dir: Output directory
            
        Returns:
            Generated document info
        """
        instructions_content = f"""
INSTRUCTIONS FOR COMPLETING YOUR EU GRANT APPLICATION
====================================================

Grant: {grant.title}
Grant ID: {grant.id}
Deadline: {grant.deadline.strftime('%Y-%m-%d')} ({(grant.deadline - datetime.now().date()).days} days remaining)

WHAT WE'VE DONE FOR YOU:
-----------------------
✅ Downloaded and analyzed all application documents
✅ Researched your company information online
✅ Pre-filled all forms with available data
✅ Generated ready-to-review application documents
✅ Identified fields requiring your attention

YOUR ACTION ITEMS:
-----------------
"""
        
        # Group user input requirements by priority
        high_priority = []
        medium_priority = []
        
        for form in prefilled_forms:
            for field in form.user_input_required:
                if field.field_name in ['project_title', 'project_summary', 'total_budget']:
                    high_priority.append((form.form_name, field))
                else:
                    medium_priority.append((form.form_name, field))
        
        if high_priority:
            instructions_content += "\\n🔴 HIGH PRIORITY (Required for submission):\\n"
            for form_name, field in high_priority:
                instructions_content += f"• {form_name} - {field.field_name}: {field.user_prompt}\\n"
        
        if medium_priority:
            instructions_content += "\\n🟡 MEDIUM PRIORITY (Improve your application):\\n"
            for form_name, field in medium_priority:
                instructions_content += f"• {form_name} - {field.field_name}: {field.user_prompt}\\n"
        
        instructions_content += f"""

STEP-BY-STEP GUIDE:
------------------
1. REVIEW PRE-FILLED DATA
   - Open each generated form file
   - Verify all automatically filled information is correct
   - Pay special attention to company details and contact information

2. COMPLETE HIGH-PRIORITY FIELDS
   - Focus on project title and summary first
   - These are critical for the initial evaluation
   - Make them compelling and specific to your approach

3. REFINE BUDGET INFORMATION  
   - Review the suggested budget breakdown
   - Adjust based on your actual project planning
   - Ensure costs are realistic and justified

4. COMPLETE REMAINING FIELDS
   - Work through medium-priority items
   - These will strengthen your application

5. QUALITY CHECK
   - Spell-check all text fields
   - Verify all numbers add up correctly
   - Ensure consistency across all forms

6. GATHER SUPPORTING DOCUMENTS
   - Company registration certificate
   - Recent financial statements
   - CVs of key team members
   - Any required partner agreements

7. FINAL REVIEW
   - Have a colleague review the application
   - Check against the original grant call requirements
   - Verify all mandatory fields are completed

8. SUBMIT
   - Convert documents to required formats (usually PDF)
   - Submit through the official EU portal
   - Keep copies of everything submitted

TIPS FOR SUCCESS:
----------------
• Be specific and quantitative in your descriptions
• Highlight your unique value proposition
• Demonstrate clear European added value
• Show measurable outcomes and impact
• Provide evidence of technical feasibility
• Address sustainability and scalability

CONTACT SUPPORT:
---------------
If you need help with any of these steps, you can:
• Run 'grants-monitor assist {grant.id}' again for updated guidance
• Review the official grant documentation at: {grant.url}
• Contact the EU funding helpdesk if needed

Good luck with your application! 🚀

Generated by EU Grants Monitor Agent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        file_path = output_dir / "USER_INSTRUCTIONS.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(instructions_content)
        
        return GeneratedDocument(
            document_name="USER_INSTRUCTIONS.txt",
            file_path=str(file_path),
            file_type="txt",
            size_bytes=file_path.stat().st_size,
            completion_status="complete",
            missing_fields=[],
            generated_at=datetime.now()
        )
