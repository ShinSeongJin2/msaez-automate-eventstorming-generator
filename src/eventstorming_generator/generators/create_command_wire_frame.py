from typing import Any, Dict, Optional
import json

from .xml_base import XmlBaseGenerator
from ..models import CreateCommandWireFrameOutput
from ..utils import XmlUtil

class CreateCommandWireFrame(XmlBaseGenerator):
    COMMON_STYLE_DIC = {
        "root-div": ".rootdiv { max-width:600px; margin:0 auto; padding:24px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; }",
        "form-group": ".form-group { margin-bottom: 1rem; }",
        "form-label": ".form-label { display: block; margin-bottom: .5rem; font-weight: 500; }",
        "form-control": ".form-control { display: block; width: 100%; padding: .375rem .75rem; font-size: 1rem; line-height: 1.5; color: #495057; background-color: #fff; background-clip: padding-box; border: 1px solid #ced4da; border-radius: .25rem; transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out; box-sizing: border-box; }",
        "form-control:focus": ".form-control:focus { color: #495057; background-color: #fff; border-color: #80bdff; outline: 0; box-shadow: 0 0 0 .2rem rgba(0,123,255,.25); }",
        "btn": ".btn { display: inline-block; font-weight: 400; text-align: center; vertical-align: middle; user-select: none; background-color: transparent; border: 1px solid transparent; padding: .375rem .75rem; font-size: 1rem; line-height: 1.5; border-radius: .25rem; cursor: pointer; transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out; }",
        "btn-primary": ".btn-primary { color: #fff; background-color: #007bff; border-color: #007bff; }",
        "btn-primary:hover": ".btn-primary:hover { color: #fff; background-color: #0069d9; border-color: #0062cc; }",
        "btn-secondary": ".btn-secondary { color: #fff; background-color: #6c757d; border-color: #6c757d; }",
        "btn-secondary:hover": ".btn-secondary:hover { color: #fff; background-color: #5a6268; border-color: #545b62; }",
        "text-danger": ".text-danger { color: #dc3545; }",
        "mt-2": ".mt-2 { margin-top: .5rem; }",
        "w-100": ".w-100 { width: 100%; }",
    }

    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["commandName", "commandDisplayName", "fields", "api"]
        super().__init__(model_name, CreateCommandWireFrameOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Senior UI/UX Designer and Frontend Architect",
            "goal": "To create intuitive, user-friendly HTML wireframes for command interfaces that translate business requirements into well-structured, accessible, and visually appealing user interfaces following modern UI/UX best practices.",
            "backstory": "With extensive experience in designing enterprise command interfaces and form-based applications, I've mastered the practical application of user experience design principles across diverse business domains. My approach combines visual design excellence with functional usability, ensuring interfaces remain intuitive while addressing complex business operations. I excel at creating wireframes that properly represent command structures, form layouts, and user interaction patterns."
        }

    def _build_task_instruction_prompt(self) -> str:
        return f"""<instruction>
    <core_instructions>
        <title>Wireframe Generation Task</title>
        <task_description>You need to create an HTML wireframe for a command interface based on the provided command information and additional requirements.</task_description>

        <output_rules>
            <title>Output Format</title>
            <rule id="json_structure">The output must be a JSON object with a single key: "html".</rule>
            <rule id="html_value">The "html" value will be the complete HTML wireframe code.</rule>
        </output_rules>
        
        <wireframe_rules>
            <title>HTML Wireframe Requirements</title>
            <rule id="purpose">This is a PREVIEW COMPONENT, not a complete webpage. It will be embedded inside a container, so it must fit within it and not take over the entire screen. Think of it as a UI component, not a standalone page.</rule>
            <rule id="no_full_page_tags">DO NOT use `<html>`, `<head>`, or `<body>` tags.</rule>
            <rule id="structure">Start with a `<style>` tag for custom CSS, followed by `<div>` container elements.</rule>
            <rule id="no_viewport_units">DO NOT use `height: 100vh` or `width: 100vw`. Use relative sizing (`%`, `auto`).</rule>
            <rule id="static_only">DO NOT include JavaScript code. Wireframes must be static HTML with CSS only.</rule>
            <rule id="accessibility">Ensure accessibility with proper ARIA labels and semantic markup.</rule>
            <rule id="sample_data">Include sample data to demonstrate functionality.</rule>
        </wireframe_rules>

        <styling_rules>
            <title>CSS Styling Guidelines</title>
            <common_styles>
                <title>Common CSS Classes</title>
                <description>A set of predefined CSS classes is available. Prioritize using these for consistency. The style block for these classes will be added automatically if you use them, so you don't need to include it in your output.</description>
                <classes>
{XmlUtil.from_dict(self.COMMON_STYLE_DIC)}
                </classes>
            </common_styles>
            <custom_styles>
                <title>Custom Styling Strategy</title>
                <rule id="embedded_css">Use an embedded `<style>` tag for styles that are reused 2 or more times (e.g., custom form controls, buttons).</rule>
                <rule id="inline_css">Use inline CSS for unique, one-time styles or specific layout positioning.</rule>
                <rule id="minimize_html">Prefer embedded CSS for common patterns to reduce code repetition and HTML size.</rule>
            </custom_styles>
            <default_styles>
                <title>Default Style Guidelines</title>
                <rule id="buttons">Primary: #007bff, Secondary: #6c757d</rule>
                <rule id="forms">16px margins, 4px border-radius</rule>
                <rule id="colors">Success: #28a745, Error: #dc3545</rule>
                <rule id="layout">Center-aligned, max-width 600px</rule>
                <rule id="typography">Clean, readable fonts with proper contrast</rule>
            </default_styles>
        </styling_rules>

        <design_process>
            <title>Command Interface Design Process</title>
            <step id="1" name="Default Structure">
                <description>If no specific structural requirements are given, create a simple form with all provided fields. Use appropriate input types based on field data types (String -> text/textarea, Date -> date picker, Boolean -> checkbox/toggle, Number -> number input, Selection -> dropdown/radio).</description>
            </step>
            <step id="2" name="Handling Additional Requirements">
                <description>Process ALL additional requirements together.</description>
                <scenario name="Simple Changes (colors, fonts)">Keep the basic structure and apply only the requested style changes.</scenario>
                <scenario name="Component Changes (add screens, buttons)">Keep the basic structure and add the requested components.</scenario>
                <scenario name="Structural Changes (dashboard, charts)">Ignore the basic structure and create a new one as requested.</scenario>
            </step>
            <step id="3" name="Layout and UX">
                <description>Group related fields logically. Use proper spacing, alignment, and label-input associations for a clear visual hierarchy. Include validation indicators and error states. Minimize cognitive load and focus on task completion.</description>
            </step>
        </design_process>
        
        <language_and_naming>
            <title>Language and Naming Conventions</title>
            <rule id="language">All user-facing text must be in user's preferred language.</rule>
            <rule id="labels">Use clear, descriptive labels that reflect business concepts.</rule>
            <rule id="naming">Follow consistent naming patterns for UI elements.</rule>
        </language_and_naming>
    </core_instructions>
</instruction>"""
        
    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "command_name": "RegisterUser",
            "command_display_name": "User Registration", 
            "fields": XmlUtil.from_dict([
                {
                    "name": "email",
                    "type": "String", 
                    "required": True
                },
                {
                    "name": "password",
                    "type": "String",
                    "required": True
                },
                {
                    "name": "confirmPassword", 
                    "type": "String",
                    "required": True
                },
                {
                    "name": "acceptTerms",
                    "type": "Boolean", 
                    "required": True
                }
            ]),
            "api": "POST /users/register",
            "additional_requirements": "Add password strength indicator and terms of service link",
            "user_preferred_language": "English"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "html": """<style>
    .field-feedback {
        font-size: 12px;
        display: block;
        margin-top: 4px;
    }
</style>
<div class="root-div">
    <div style="background:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);padding:32px;">
        <h2 style="text-align:center;margin-bottom:24px;color:#333;font-size:24px;">User Registration</h2>
        
        <form style="display:flex;flex-direction:column;gap:20px;">
            <div class="form-group">
                <label for="email" class="form-label">Email Address *</label>
                <input type="email" id="email" name="email" required class="form-control" placeholder="Enter your email address">
            </div>
            
            <div class="form-group">
                <label for="password" class="form-label">Password *</label>
                <input type="password" id="password" name="password" required class="form-control" placeholder="Enter your password">
                <div style="height: 4px; background: #eee; border-radius: 2px; margin-top: 6px;">
                    <div style="height: 100%; background: #ffc107; width: 50%; border-radius: 2px;"></div>
                </div>
                <small class="field-feedback" style="color:#ffc107;">Password Strength: Fair</small>
            </div>
            
            <div class="form-group">
                <label for="confirmPassword" class="form-label">Confirm Password *</label>
                <input type="password" id="confirmPassword" name="confirmPassword" required class="form-control" placeholder="Confirm your password">
                <small class="field-feedback text-danger">Passwords do not match.</small>
            </div>
            
            <div style="display:flex;align-items:flex-start;gap:12px;">
                <input type="checkbox" id="acceptTerms" name="acceptTerms" required style="margin-top:4px;width:16px;height:16px;">
                <label for="acceptTerms" style="font-size:14px;color:#555;line-height:1.4;">
                    I accept the <a href="#" style="color:#007bff;text-decoration:none;">Terms of Service</a> and Privacy Policy *
                </label>
            </div>
            
            <button type="submit" class="btn btn-primary w-100" style="margin-top:8px;">
                Register Account
            </button>
        </form>
    </div>
</div>"""
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "command_name": inputs.get("commandName"),
            "command_display_name": inputs.get("commandDisplayName"), 
            "fields": XmlUtil.from_dict(inputs.get("fields")),
            "api": inputs.get("api"),
            "additional_requirements": inputs.get("additionalRequirements", ""),
            "user_preferred_language": self.client.get("preferredLanguage")
        }

    def _post_process_to_structured_output(self, output: CreateCommandWireFrameOutput) -> CreateCommandWireFrameOutput:
        try:
            used_common_classes = []
            for class_name in self.COMMON_STYLE_DIC.keys():
                if class_name in output.html:
                    used_common_classes.append(class_name)               
            
            if used_common_classes:
                style_content = "<style>\n"
                for class_name in used_common_classes:
                    style_content += self.COMMON_STYLE_DIC[class_name] + "\n"
                style_content += "</style>\n"
                output.html = style_content + output.html
            
            return output
        except (json.JSONDecodeError, AttributeError):
            raise ValueError("Invalid JSON format")
    