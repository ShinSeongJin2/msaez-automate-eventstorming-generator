from typing import Any, Dict, Optional
from .base import BaseGenerator
from ..models import CreateReadModelWireFrameOutput

class CreateReadModelWireFrame(BaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["viewName", "viewDisplayName", "aggregateFields", "viewQueryParameters"]
        super().__init__(model_name, model_kwargs, client, structured_output_class=CreateReadModelWireFrameOutput)

    def _build_agent_role_prompt(self) -> str:
        return """Role: Senior UI/UX Designer and Front-end Architect

Goal: To create professional, user-friendly HTML wireframes for View/Query interfaces that effectively present data and provide intuitive user interactions following modern UI/UX design principles.

Backstory: With extensive experience in creating data-driven interfaces and query systems, I've mastered the practical application of modern UI/UX patterns across diverse business domains. My approach combines visual design excellence with functional usability, ensuring interfaces remain accessible while efficiently presenting complex data structures. I excel at creating wireframes that balance aesthetics with functionality, designing responsive layouts that work across different screen sizes.

Operational Guidelines:
* Create HTML wireframes that serve as preview components, not complete webpages
* Design interfaces that fit within containers for embedding purposes
* Apply modern UI/UX principles with consistent spacing, typography, and visual hierarchy
* Implement responsive design patterns that work across different screen sizes
* Create intuitive search forms with appropriate input controls for different data types
* Design effective data presentation using tables, cards, or other appropriate formats
* Include interactive elements with proper JavaScript functionality
* Use semantic HTML markup with proper accessibility considerations
* Apply inline CSS styling for complete self-contained components
* Include sample data to demonstrate functionality and visual appearance"""

    def _build_task_guidelines_prompt(self) -> str:
        return f"""You need to create an HTML wireframe for a View/Query interface based on the provided information about the read model and any additional requirements.

**IMPORTANT: Wireframe Purpose**
- This is a **PREVIEW COMPONENT**, not a complete webpage
- It will be **embedded inside a container** for preview purposes
- It should **fit within its container**, not take over the entire screen
- Think of it as a **UI component** that shows the design, not a standalone page

**View Type**: Regular View (Search form + Results table)

## Requirements Handling

**If NO Additional Requirements:**
- Use the basic structure with search form and results table
- Follow default style guidelines below

**If Additional Requirements exist:**
1. **Simple Changes** (colors, fonts, minor styles):
   - Keep basic structure intact
   - Apply only the requested changes
   
2. **Component Changes** (add fields, filters, pagination):
   - Keep basic structure intact
   - Add requested components
   
3. **Structural Changes** (cards, charts, dashboard):
   - Ignore basic structure completely
   - Create new structure as requested

**CRITICAL: Multiple Requirements Handling**
- **When multiple requirements exist, process ALL of them together**
- **Example**: "Display as cards + Add filters" = Structural + Component changes
- **Do NOT ignore any part of the requirements**
- **Combine different types of changes as needed**

## Technical Guidelines

**HTML Structure Requirements:**
- **DO NOT use <html>, <head>, <body> tags**
- **Start with <div> or other container elements**
- **DO NOT use height: 100vh or width: 100vw**
- **Create a component that fits within a container, not a full page**
- **Use relative sizing (%, auto) instead of viewport units**

**CSS Styling Requirements:**
- Include complete HTML structure with inline CSS styling using style attributes on each element
- Use modern CSS practices (flexbox, grid where appropriate) through inline styles
- Ensure responsive design principles with appropriate inline styling
- Apply consistent spacing and typography through direct style attributes

**JavaScript Requirements:**
- **DO NOT include JavaScript code - wireframes should be static HTML with CSS only**
- Design visual representations of interactive elements without functionality
- Use static styling to show different states (hover, active, selected)
- Focus on visual design rather than interactive behavior

**Data Presentation:**
- Include realistic sample data to demonstrate functionality
- Use appropriate input types for different data types (date, number, text, etc.)
- Implement proper form validation
- Show loading states and empty states where relevant

## Default Style Guidelines
- Primary buttons: #007bff
- Secondary buttons: #6c757d
- Table background: #ffffff with #dee2e6 borders
- Form controls: 8px padding, 4px border-radius
- Layout: Responsive with consistent spacing
- Typography: Clean, readable font stack
- Color scheme: Professional and accessible

## Language Requirements
- All UI text and labels must be in {self.client.get("preferredLanguage")}
- Use appropriate terminology for the business domain
- Ensure proper localization for dates, numbers, and formatting"""

    def _build_inference_guidelines_prompt(self) -> str:
        return """
Inference Guidelines:
1. The reasoning process should be directly related to the wireframe design decisions, not general UI/UX theory.
2. Design Focus: Analyze the provided view information (name, fields, query parameters) and determine the most appropriate UI structure and interactions.
3. Requirements Analysis: Carefully evaluate additional requirements to determine if they require simple changes, component additions, or complete structural modifications.
4. User Experience Consideration: Consider the user journey, data visualization needs, and interaction patterns that best serve the business requirements.
5. Technical Implementation: Plan the HTML structure, CSS styling, and JavaScript functionality needed to create a complete, functional wireframe.
6. Accessibility and Responsiveness: Ensure the design works across devices and meets accessibility standards.
7. Sample Data Strategy: Determine what sample data would best demonstrate the interface functionality and visual design.
"""

    def _build_json_response_format(self) -> str:
        return """
{
    "inference": "<inference>",
    "result": {
        "html": "<complete HTML wireframe code starting with <div> container, including inline CSS only (NO JavaScript)>"
    }
}
"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "View Name": "ProductSearch",
            "View Display Name": "Product Search",
            "Aggregate Fields": [
                {
                    "name": "productId",
                    "type": "Long"
                },
                {
                    "name": "productName",
                    "type": "String"
                },
                {
                    "name": "category",
                    "type": "String"
                },
                {
                    "name": "price",
                    "type": "Double"
                },
                {
                    "name": "stockQuantity",
                    "type": "Integer"
                },
                {
                    "name": "createdDate",
                    "type": "Date"
                }
            ],
            "View Query Parameters": [
                {
                    "name": "productName",
                    "type": "String"
                },
                {
                    "name": "category",
                    "type": "String"
                },
                {
                    "name": "minPrice",
                    "type": "Double"
                },
                {
                    "name": "maxPrice",
                    "type": "Double"
                }
            ],
            "Additional Requirements": "Add sorting by price and creation date, include pagination with 10 items per page"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Based on the Product Search view requirements, I designed a comprehensive search interface with a search form at the top containing fields for product name, category, and price range filtering. The results are displayed in a responsive table format with visual indicators for sortable columns for price and creation date. Pagination is shown with 10 items per page as requested. The interface includes modern styling with Bootstrap-like components, visual elements representing interactivity, and proper data visualization with sample product data to demonstrate the complete user experience.",
            "result": {
                "html": """<div style="max-width: 1200px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 20px 0; color: #333;">Product Search</h2>
        <div style="display: flex; gap: 15px; margin-bottom: 15px; align-items: end;">
            <div style="flex: 1;">
                <label for="productName" style="display: block; margin-bottom: 5px; font-weight: 500; color: #333;">Product Name</label>
                <input type="text" id="productName" style="width: 100%; padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 14px;" placeholder="Enter product name">
            </div>
            <div style="flex: 1;">
                <label for="category" style="display: block; margin-bottom: 5px; font-weight: 500; color: #333;">Category</label>
                <select id="category" style="width: 100%; padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 14px;">
                    <option value="">All Categories</option>
                    <option value="Electronics">Electronics</option>
                    <option value="Clothing">Clothing</option>
                    <option value="Books">Books</option>
                </select>
            </div>
            <div style="flex: 1;">
                <label for="minPrice" style="display: block; margin-bottom: 5px; font-weight: 500; color: #333;">Min Price</label>
                <input type="number" id="minPrice" style="width: 100%; padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 14px;" placeholder="0.00" step="0.01">
            </div>
            <div style="flex: 1;">
                <label for="maxPrice" style="display: block; margin-bottom: 5px; font-weight: 500; color: #333;">Max Price</label>
                <input type="number" id="maxPrice" style="width: 100%; padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 14px;" placeholder="999.99" step="0.01">
            </div>
        </div>
        <div style="text-align: right;">
            <button style="padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; background-color: #6c757d; color: white; margin-right: 10px;">Clear</button>
            <button style="padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500; background-color: #007bff; color: white;">Search</button>
        </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <thead>
            <tr>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057;">Product ID</th>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057;">Product Name</th>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057;">Category</th>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057; cursor: pointer;">Price ↕️</th>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057;">Stock Quantity</th>
                <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; background-color: #f8f9fa; font-weight: 600; color: #495057; cursor: pointer;">Created Date ↕️</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: white;"><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">1001</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Wireless Headphones</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Electronics</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">$79.99</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">45</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">2024-01-15</td></tr>
            <tr style="background-color: white;"><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">1002</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Cotton T-Shirt</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Clothing</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">$24.99</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">120</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">2024-01-10</td></tr>
            <tr style="background-color: white;"><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">1003</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Programming Guide</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Books</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">$39.99</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">30</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">2024-01-08</td></tr>
            <tr style="background-color: white;"><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">1004</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Smart Watch</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Electronics</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">$199.99</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">25</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">2024-01-20</td></tr>
            <tr style="background-color: white;"><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">1005</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Denim Jeans</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Clothing</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">$59.99</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">80</td><td style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">2024-01-12</td></tr>
        </tbody>
    </table>

    <div style="display: flex; justify-content: center; margin-top: 20px; gap: 5px;">
        <a href="#" style="padding: 8px 12px; border: 1px solid #dee2e6; color: #007bff; text-decoration: none; border-radius: 4px;">Previous</a>
        <a href="#" style="padding: 8px 12px; border: 1px solid #007bff; color: white; text-decoration: none; border-radius: 4px; background-color: #007bff;">1</a>
        <a href="#" style="padding: 8px 12px; border: 1px solid #dee2e6; color: #007bff; text-decoration: none; border-radius: 4px;">2</a>
        <a href="#" style="padding: 8px 12px; border: 1px solid #dee2e6; color: #007bff; text-decoration: none; border-radius: 4px;">3</a>
        <a href="#" style="padding: 8px 12px; border: 1px solid #dee2e6; color: #007bff; text-decoration: none; border-radius: 4px;">Next</a>
    </div>
</div>"""
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "View Name": inputs.get("viewName", ""),
            "View Display Name": inputs.get("viewDisplayName", ""),
            "Aggregate Fields": inputs.get("aggregateFields", []),
            "View Query Parameters": inputs.get("viewQueryParameters", []),
            "Additional Requirements": inputs.get("additionalRequirements", "")
        }