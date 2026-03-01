"""
Semantic Bridge v2.0: Form Ingest, ATS Parsing, Guided Field Queue
Parses HTML forms and manages sequential clipboard loop for high-friction ATS forms.
"""

import re
import json
from html.parser import HTMLParser
from pathlib import Path


class FormFieldParser(HTMLParser):
    """Parse HTML forms to extract field structure."""

    def __init__(self):
        super().__init__()
        self.fields = []
        self.current_field = {}
        self.in_form = False
        self.in_label = False
        self.label_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == "form":
            self.in_form = True
        elif tag == "label":
            self.in_label = True
        elif tag in ("input", "textarea", "select") and self.in_form:
            field_type = attrs_dict.get("type", "text")
            field_name = attrs_dict.get("name", "")
            field_id = attrs_dict.get("id", "")
            self.current_field = {
                "tag": tag,
                "type": field_type,
                "name": field_name,
                "id": field_id,
                "required": "required" in attrs_dict,
                "placeholder": attrs_dict.get("placeholder", "")
            }

    def handle_endtag(self, tag):
        if tag == "form":
            self.in_form = False
        elif tag == "label":
            self.in_label = False
            if self.current_field:
                self.current_field["label"] = self.label_text
                self.label_text = ""
        elif tag in ("input", "textarea", "select"):
            if self.current_field:
                self.fields.append(self.current_field)
                self.current_field = {}

    def handle_data(self, data):
        if self.in_label:
            self.label_text += data.strip()

    def get_fields(self):
        return self.fields


class SemanticBridge:
    """Manages form parsing and guided field queue for ATS systems."""

    # Common ATS field mappings
    ATS_FIELD_MAPPINGS = {
        "workday": {
            "phone": "Mobile Phone",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "years_experience": "Years of Experience",
            "current_title": "Current Job Title"
        },
        "greenhouse": {
            "phone": "Phone Number",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name"
        },
        "taleo": {
            "phone": "Phone",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name"
        }
    }

    def __init__(self, db=None):
        self.db = db
        self.field_queue = []

    def ingest_html_form(self, html_file_path):
        """Parse a saved HTML form from DevTools."""
        html_path = Path(html_file_path)
        if not html_path.exists():
            return {"status": "error", "message": "HTML file not found."}
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = FormFieldParser()
        parser.feed(html_content)
        fields = parser.get_fields()
        
        return {
            "status": "success",
            "fields_extracted": len(fields),
            "fields": fields
        }

    def detect_ats_system(self, html_file_path):
        """Detect which ATS system this form belongs to."""
        html_path = Path(html_file_path)
        if not html_path.exists():
            return "unknown"
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read().lower()
        
        if "workday" in html_content:
            return "workday"
        elif "greenhouse" in html_content:
            return "greenhouse"
        elif "taleo" in html_content:
            return "taleo"
        
        return "generic"

    def create_field_queue(self, fields, user_data):
        """Create sequential guided field queue for user to fill."""
        queue = []
        
        for i, field in enumerate(fields):
            field_name = field.get("name", "").lower()
            field_type = field.get("type", "text")
            label = field.get("label", field_name)
            
            suggested_value = self._suggest_value(field_name, user_data)
            
            queue_item = {
                "sequence": i + 1,
                "field_name": field_name,
                "field_type": field_type,
                "label": label,
                "placeholder": field.get("placeholder", ""),
                "required": field.get("required", False),
                "suggested_value": suggested_value,
                "instruction": self._get_instruction(field_type, label)
            }
            queue.append(queue_item)
        
        self.field_queue = queue
        return queue

    def _suggest_value(self, field_name, user_data):
        """Suggest value based on field name and user data."""
        field_lower = field_name.lower()
        
        suggestions = {
            "email": user_data.get("email", ""),
            "phone": user_data.get("phone", ""),
            "first_name": user_data.get("first_name", ""),
            "last_name": user_data.get("last_name", ""),
            "title": user_data.get("current_title", ""),
            "years": user_data.get("experience_years", ""),
            "linkedin": user_data.get("linkedin_url", ""),
        }
        
        for key, value in suggestions.items():
            if key in field_lower:
                return value
        
        return ""

    def _get_instruction(self, field_type, label):
        """Provide contextual instruction for field."""
        instructions = {
            "email": "Enter your professional email address.",
            "tel": "Enter your phone number in format +1-XXX-XXX-XXXX.",
            "textarea": "Provide detailed response. Tailor to job description.",
            "date": "Select date in MM/DD/YYYY format.",
            "checkbox": "Check if applicable to you.",
            "file": "Upload your resume / cover letter."
        }
        
        return instructions.get(field_type, f"Fill in: {label}")

    def guided_paste_loop(self, field_sequence_num):
        """Guide user through copying/pasting for a specific field."""
        if field_sequence_num > len(self.field_queue):
            return {"status": "error", "message": "Invalid field sequence."}
        
        field = self.field_queue[field_sequence_num - 1]
        
        return {
            "current_field": field_sequence_num,
            "total_fields": len(self.field_queue),
            "field_info": field,
            "action": f"Copy the suggested value and paste into field: {field['label']}",
            "progress": f"{field_sequence_num}/{len(self.field_queue)} completed"
        }

    def validate_form_completion(self, field_values):
        """Validate that all required fields are filled."""
        missing = []
        for field in self.field_queue:
            if field["required"] and not field_values.get(field["field_name"]):
                missing.append(field["label"])
        
        return {
            "is_complete": len(missing) == 0,
            "missing_fields": missing
        }

    def export_form_data(self, field_values, format="json"):
        """Export filled form data in specified format."""
        if format == "json":
            return json.dumps(field_values, indent=2)
        elif format == "csv":
            return ",".join([f"{k}:{v}" for k, v in field_values.items()])
        
        return field_values
