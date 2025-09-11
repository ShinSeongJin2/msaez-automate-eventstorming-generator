from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import CreateCommandWireFrameOutput

class CreateCommandWireFrame(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["commandName", "commandDisplayName", "fields", "api"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateCommandWireFrameOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior UI/UX Designer and Frontend Architect

Goal: To create intuitive, user-friendly HTML wireframes for command interfaces that translate business requirements into well-structured, accessible, and visually appealing user interfaces following modern UI/UX best practices.

Backstory: With extensive experience in designing enterprise command interfaces and form-based applications, I've mastered the practical application of user experience design principles across diverse business domains. My approach combines visual design excellence with functional usability, ensuring interfaces remain intuitive while addressing complex business operations. I excel at creating wireframes that properly represent command structures, form layouts, and user interaction patterns.

Operational Guidelines:
* Design clean, intuitive command interfaces that reflect business operations and user workflows  
* Create responsive, accessible wireframes following modern UI/UX standards and design systems
* Implement proper form validation patterns and user feedback mechanisms
* Apply consistent styling and component patterns for maintainable interface design
* Balance visual hierarchy with functional requirements to guide user attention effectively
* Ensure wireframes are componentized and embeddable within larger application contexts
* Design for multiple device sizes and interaction patterns while maintaining usability
* Incorporate appropriate visual cues and affordances that communicate functionality clearly
* Create interfaces that minimize cognitive load while maximizing task completion efficiency"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to create an HTML wireframe for a command interface based on the provided command information and additional requirements.

Please follow these rules:

**IMPORTANT: Wireframe Purpose**
- This is a **PREVIEW COMPONENT**, not a complete webpage
- It will be **embedded inside a container** for preview purposes  
- It should **fit within its container**, not take over the entire screen
- Think of it as a **UI component** that shows the design, not a standalone page

Command Interface Design Guidelines:
1. Basic Structure (Default):
   - Create a simple form with all provided fields
   - Include appropriate input types based on field data types
   - Add submit/action button with proper labeling
   - No additional screens by default

2. Field Type Mapping:
   - String fields: Use text input or textarea for longer content
   - Date fields: Use date picker input
   - Boolean fields: Use checkbox or toggle
   - Number fields: Use number input with appropriate constraints
   - Selection fields: Use dropdown or radio buttons

3. Form Layout:
   - Use proper spacing and alignment for visual hierarchy
   - Group related fields logically
   - Ensure proper label-input associations
   - Include validation indicators and error states

**How to Handle Additional Requirements:**

**If NO Additional Requirements:**
- Use the basic structure above
- Follow default style guidelines below

**If Additional Requirements exist:**
1. **Simple Changes** (colors, fonts, minor styles):
   - Keep basic structure
   - Apply only the requested changes
   
2. **Component Changes** (add screens, buttons, fields):
   - Keep basic structure  
   - Add requested components
   
3. **Structural Changes** (dashboard, charts, different layout):
   - Ignore basic structure completely
   - Create new structure as requested

**CRITICAL: Multiple Requirements Handling**
- **When multiple requirements exist, process ALL of them together**
- **Example**: "Card layout + Success/failure screens" = Structural + Component changes
- **Do NOT ignore any part of the requirements**
- **Combine different types of changes as needed**

**Default Style Guidelines:**
- Buttons: Primary #007bff, Secondary #6c757d  
- Forms: 16px margins, 4px border-radius
- Colors: Success #28a745, Error #dc3545
- Layout: Center-aligned, max-width 600px
- Typography: Clean, readable fonts with proper contrast
- Spacing: Consistent padding and margins for visual rhythm

**Technical Requirements:**
- **DO NOT use <html>, <head>, <body> tags**
- **Start with <div> or other container elements**
- **DO NOT use height: 100vh or width: 100vw**  
- **Create a component that fits within a container, not a full page**
- **Use relative sizing (%, auto) instead of viewport units**
- Include complete HTML structure with inline CSS styling
- **DO NOT include JavaScript code - wireframes should be static HTML with CSS only**
- Include sample data to demonstrate functionality
- Ensure accessibility with proper ARIA labels and semantic markup

Naming and Language Conventions:
1. All user-facing text must be in {self.client.get("preferredLanguage")}
2. Use clear, descriptive labels that reflect business concepts  
3. Follow consistent naming patterns for UI elements
4. Ensure proper semantic HTML structure for screen readers

Best Practices:
1. Focus on user experience and task completion efficiency
2. Minimize cognitive load through clear visual hierarchy
3. Provide immediate feedback for user actions
4. Design for error prevention and graceful error handling
5. Ensure responsive behavior within container constraints
6. Use progressive disclosure for complex forms
7. Implement proper loading and success states"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The reasoning process should be directly related to the wireframe design decisions, not a reference to general UI/UX strategies.
2. Design Focus: Prioritize user experience objectives and ensure that the generated wireframe aligns with modern UI/UX principles, accessibility standards, and responsive design patterns.
3. Requirement Analysis: Carefully evaluate the command structure, field types, business context, and additional requirements to create appropriate interface layouts.
4. Component Selection: Determine the most suitable UI components and interaction patterns based on the command's purpose and user workflow.
5. Visual Hierarchy: Establish clear information architecture and visual hierarchy that guides users through the command execution process effectively.
6. Responsive Considerations: Ensure the wireframe works well within container constraints while maintaining usability across different screen sizes.
7. Accessibility and Usability: Consider accessibility requirements, keyboard navigation, and inclusive design principles in component selection and layout decisions.
"""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<detailed reasoning about wireframe design decisions>",
    "result": {
        "html": "<complete HTML wireframe code starting with <div> container, including inline CSS only (NO JavaScript)>"
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "Command Name": "RegisterUser",
            "Command Display Name": "User Registration", 
            "Fields": [
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
            ],
            "API": "POST /users/register",
            "Additional Requirements": "Add password strength indicator and terms of service link"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Based on the RegisterUser command, I need to create a user registration form with email, password, confirm password, and terms acceptance fields. The additional requirements specify a password strength indicator and terms of service link, so I'll add these visual elements using static CSS styling. The form uses a clean, centered layout with proper validation styling and responsive design that works within a container.",
            "result": {
                "html": """<div style="max-width: 600px; margin: 0 auto; padding: 24px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <div style="background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 32px;">
    <h2 style="text-align: center; margin-bottom: 24px; color: #333; font-size: 24px;">User Registration</h2>
    
    <form id="registerForm" style="display: flex; flex-direction: column; gap: 20px;">
      <div>
        <label for="email" style="display: block; margin-bottom: 6px; font-weight: 500; color: #555;">Email Address *</label>
        <input type="email" id="email" name="email" required 
               style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 4px; font-size: 16px; box-sizing: border-box;"
               placeholder="Enter your email address">
      </div>
      
      <div>
        <label for="password" style="display: block; margin-bottom: 6px; font-weight: 500; color: #555;">Password *</label>
        <input type="password" id="password" name="password" required
               style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 4px; font-size: 16px; box-sizing: border-box;"
               placeholder="Enter your password">
        <div style="height: 4px; background: #eee; border-radius: 2px; margin-top: 6px;">
          <div style="height: 100%; background: #ffc107; width: 50%; border-radius: 2px;"></div>
        </div>
        <small style="color: #ffc107; font-size: 12px;">Password Strength: Fair</small>
      </div>
      
      <div>
        <label for="confirmPassword" style="display: block; margin-bottom: 6px; font-weight: 500; color: #555;">Confirm Password *</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required
               style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 4px; font-size: 16px; box-sizing: border-box;"
               placeholder="Confirm your password">
      </div>
      
      <div style="display: flex; align-items: flex-start; gap: 12px;">
        <input type="checkbox" id="acceptTerms" name="acceptTerms" required
               style="margin-top: 4px; width: 16px; height: 16px;">
        <label for="acceptTerms" style="font-size: 14px; color: #555; line-height: 1.4;">
          I accept the <a href="#" style="color: #007bff; text-decoration: none;">Terms of Service</a> and Privacy Policy *
        </label>
      </div>
      
      <button type="submit" 
              style="background: #007bff; color: white; border: none; padding: 14px 24px; border-radius: 4px; font-size: 16px; font-weight: 500; cursor: pointer; margin-top: 8px;">
        Register Account
      </button>
    </form>
  </div>
</div>"""
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "Command Name": inputs.get("commandName"),
            "Command Display Name": inputs.get("commandDisplayName"), 
            "Fields": inputs.get("fields"),
            "API": inputs.get("api"),
            "Additional Requirements": inputs.get("additionalRequirements", "")
        }