"""
User Prompter Service for EU Grant Applications.

This service provides interactive prompts to gather missing critical
information from users during the application process.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from loguru import logger

from .form_prefiller import PrefilledForm, FormField


@dataclass
class UserResponse:
    """User response to a prompt."""
    
    field_name: str
    response: str
    confidence: float = 1.0  # User input has high confidence
    requires_validation: bool = False


class UserPrompter:
    """Interactive prompting system for gathering user input."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the user prompter.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.console = Console()
        logger.info("UserPrompter initialized")
    
    def collect_missing_information(
        self,
        prefilled_forms: List[PrefilledForm],
        grant_title: str
    ) -> Dict[str, UserResponse]:
        """Collect missing critical information from user.
        
        Args:
            prefilled_forms: List of pre-filled forms
            grant_title: Title of the grant for context
            
        Returns:
            Dictionary of user responses
        """
        logger.info("Starting interactive user information collection")
        
        # Show overview
        self._show_collection_overview(prefilled_forms, grant_title)
        
        user_responses = {}
        
        # Collect high-priority fields first
        high_priority_fields = self._get_high_priority_fields(prefilled_forms)
        if high_priority_fields:
            self.console.print("\\n🔴 [bold red]High Priority Fields (Critical for submission)[/bold red]")
            for form_name, field in high_priority_fields:
                response = self._prompt_for_field(field, form_name, "HIGH")
                if response:
                    user_responses[field.field_name] = response
        
        # Ask if user wants to continue with medium priority fields
        medium_priority_fields = self._get_medium_priority_fields(prefilled_forms)
        if medium_priority_fields:
            continue_medium = Confirm.ask(
                "\\n🟡 Would you like to complete medium priority fields to strengthen your application?",
                default=True
            )
            
            if continue_medium:
                self.console.print("\\n🟡 [bold yellow]Medium Priority Fields (Improve application quality)[/bold yellow]")
                for form_name, field in medium_priority_fields:
                    response = self._prompt_for_field(field, form_name, "MEDIUM")
                    if response:
                        user_responses[field.field_name] = response
        
        # Show completion summary
        self._show_completion_summary(user_responses)
        
        return user_responses
    
    def _show_collection_overview(self, prefilled_forms: List[PrefilledForm], grant_title: str):
        """Show overview of what needs to be collected.
        
        Args:
            prefilled_forms: List of pre-filled forms
            grant_title: Grant title
        """
        total_user_input = sum(len(form.user_input_required) for form in prefilled_forms)
        total_critical = sum(len(form.missing_critical_fields) for form in prefilled_forms)
        
        overview_text = f"""
📋 **Grant Application**: {grant_title}
📊 **Fields to Review**: {total_user_input} total
🔴 **Critical Fields**: {total_critical} must be completed
🟡 **Enhancement Fields**: {total_user_input - total_critical} optional but recommended

We'll guide you through the most important information first, then offer to help with additional fields that will strengthen your application.
"""
        
        self.console.print(Panel(
            overview_text,
            title="📝 Information Collection Overview",
            style="blue"
        ))
    
    def _get_high_priority_fields(self, prefilled_forms: List[PrefilledForm]) -> List[tuple]:
        """Get high priority fields that must be completed.
        
        Args:
            prefilled_forms: List of pre-filled forms
            
        Returns:
            List of (form_name, field) tuples for high priority fields
        """
        high_priority_field_names = [
            'project_title', 'project_summary', 'total_budget', 
            'project_coordinator', 'contact_email'
        ]
        
        high_priority = []
        for form in prefilled_forms:
            for field in form.user_input_required:
                if field.field_name in high_priority_field_names:
                    high_priority.append((form.form_name, field))
        
        return high_priority
    
    def _get_medium_priority_fields(self, prefilled_forms: List[PrefilledForm]) -> List[tuple]:
        """Get medium priority fields that improve the application.
        
        Args:
            prefilled_forms: List of pre-filled forms
            
        Returns:
            List of (form_name, field) tuples for medium priority fields
        """
        high_priority_field_names = [
            'project_title', 'project_summary', 'total_budget', 
            'project_coordinator', 'contact_email'
        ]
        
        medium_priority = []
        for form in prefilled_forms:
            for field in form.user_input_required:
                if field.field_name not in high_priority_field_names:
                    medium_priority.append((form.form_name, field))
        
        return medium_priority
    
    def _prompt_for_field(
        self,
        field: FormField,
        form_name: str,
        priority: str
    ) -> Optional[UserResponse]:
        """Prompt user for a specific field.
        
        Args:
            field: Form field to prompt for
            form_name: Name of the form containing the field
            priority: Priority level (HIGH, MEDIUM)
            
        Returns:
            User response if provided
        """
        # Create context panel
        context_text = f"""
📄 **Form**: {form_name}
🏷️  **Field**: {field.field_name.replace('_', ' ').title()}
📝 **Current Value**: {field.prefilled_value or '[Empty]'}
💡 **Guidance**: {field.user_prompt}
"""
        
        self.console.print(Panel(
            context_text,
            title=f"[{priority}] Field Input Required",
            style="yellow" if priority == "MEDIUM" else "red"
        ))
        
        # Handle different field types
        response_value = None
        
        if field.field_type == "textarea":
            response_value = self._prompt_textarea(field)
        elif field.field_type == "number":
            response_value = self._prompt_number(field)
        elif field.field_type == "email":
            response_value = self._prompt_email(field)
        elif field.field_type == "date":
            response_value = self._prompt_date(field)
        elif field.field_type == "select" and field.options:
            response_value = self._prompt_select(field)
        else:
            response_value = self._prompt_text(field)
        
        if response_value:
            return UserResponse(
                field_name=field.field_name,
                response=response_value,
                confidence=1.0
            )
        
        return None
    
    def _prompt_text(self, field: FormField) -> Optional[str]:
        """Prompt for text input.
        
        Args:
            field: Form field
            
        Returns:
            User input or None if skipped
        """
        default_value = field.prefilled_value if field.prefilled_value else ""
        
        prompt_text = f"Enter {field.field_name.replace('_', ' ')}"
        if default_value:
            prompt_text += f" (current: {default_value[:50]}...)" if len(default_value) > 50 else f" (current: {default_value})"
        
        return Prompt.ask(
            prompt_text,
            default=default_value or None,
            show_default=bool(default_value)
        )
    
    def _prompt_textarea(self, field: FormField) -> Optional[str]:
        """Prompt for multi-line text input.
        
        Args:
            field: Form field
            
        Returns:
            User input or None if skipped
        """
        self.console.print(f"[bold]Multi-line input for {field.field_name.replace('_', ' ')}:[/bold]")
        self.console.print("(Press Enter twice when finished, or type 'SKIP' to skip)")
        
        if field.prefilled_value:
            self.console.print(f"[dim]Current value:[/dim]\\n{field.prefilled_value}\\n")
            use_current = Confirm.ask("Use the current value", default=True)
            if use_current:
                return field.prefilled_value
        
        lines = []
        empty_lines = 0
        
        while True:
            try:
                line = input("> ")
                if line.strip().upper() == 'SKIP':
                    return None
                
                if line.strip() == "":
                    empty_lines += 1
                    if empty_lines >= 2:
                        break
                else:
                    empty_lines = 0
                
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        
        result = "\\n".join(lines).strip()
        return result if result else None
    
    def _prompt_number(self, field: FormField) -> Optional[str]:
        """Prompt for numeric input.
        
        Args:
            field: Form field
            
        Returns:
            User input or None if skipped
        """
        default_value = field.prefilled_value
        
        while True:
            response = Prompt.ask(
                f"Enter {field.field_name.replace('_', ' ')} (numbers only)",
                default=default_value
            )
            
            if response is None:
                return None
            
            try:
                # Validate it's a number
                float(response.replace(',', ''))
                return response
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
    
    def _prompt_email(self, field: FormField) -> Optional[str]:
        """Prompt for email input.
        
        Args:
            field: Form field
            
        Returns:
            User input or None if skipped
        """
        while True:
            response = Prompt.ask(
                f"Enter {field.field_name.replace('_', ' ')}",
                default=field.prefilled_value
            )
            
            if response is None:
                return None
            
            # Basic email validation
            if "@" in response and "." in response.split("@")[1]:
                return response
            else:
                self.console.print("[red]Please enter a valid email address[/red]")
    
    def _prompt_date(self, field: FormField) -> Optional[str]:
        """Prompt for date input.
        
        Args:
            field: Form field
            
        Returns:
            User input or None if skipped
        """
        date_format_help = "(format: YYYY-MM-DD)"
        
        while True:
            response = Prompt.ask(
                f"Enter {field.field_name.replace('_', ' ')} {date_format_help}",
                default=field.prefilled_value
            )
            
            if response is None:
                return None
            
            # Basic date validation
            try:
                from datetime import datetime
                datetime.strptime(response, "%Y-%m-%d")
                return response
            except ValueError:
                self.console.print("[red]Please enter a valid date in YYYY-MM-DD format[/red]")
    
    def _prompt_select(self, field: FormField) -> Optional[str]:
        """Prompt for selection from options.
        
        Args:
            field: Form field with options
            
        Returns:
            User input or None if skipped
        """
        # Show options table
        table = Table(title=f"Options for {field.field_name.replace('_', ' ')}")
        table.add_column("Number", style="cyan")
        table.add_column("Option", style="white")
        
        for i, option in enumerate(field.options, 1):
            table.add_row(str(i), option)
        
        self.console.print(table)
        
        while True:
            response = Prompt.ask(
                "Select an option by number",
                choices=[str(i) for i in range(1, len(field.options) + 1)]
            )
            
            if response is None:
                return None
            
            try:
                index = int(response) - 1
                return field.options[index]
            except (ValueError, IndexError):
                self.console.print("[red]Please enter a valid option number[/red]")
    
    def _show_completion_summary(self, user_responses: Dict[str, UserResponse]):
        """Show summary of collected information.
        
        Args:
            user_responses: Dictionary of user responses
        """
        self.console.print("\\n" + "="*60)
        self.console.print("[bold green]✅ Information Collection Complete![/bold green]")
        
        if user_responses:
            self.console.print(f"\\n📋 **Collected {len(user_responses)} field(s):**")
            for field_name, response in user_responses.items():
                field_display = field_name.replace('_', ' ').title()
                value_preview = response.response[:50] + "..." if len(response.response) > 50 else response.response
                self.console.print(f"  ✓ {field_display}: {value_preview}")
        else:
            self.console.print("\\n📋 No additional information was collected.")
        
        self.console.print("\\n🎯 **Next Steps:**")
        self.console.print("  1. Your responses will be integrated into the application forms")
        self.console.print("  2. Complete application documents will be generated")
        self.console.print("  3. Review the generated documents before submission")
        
        self.console.print("\\n" + "="*60)
