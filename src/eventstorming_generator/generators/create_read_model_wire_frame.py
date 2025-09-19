from typing import Any, Dict, Optional
import json

from .xml_base import XmlBaseGenerator
from ..models import CreateReadModelWireFrameOutput
from ..utils import XmlUtil

class CreateReadModelWireFrame(XmlBaseGenerator):
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
        self.inputs_types_to_check = ["viewName", "viewDisplayName", "aggregateFields", "viewQueryParameters"]
        super().__init__(model_name, CreateReadModelWireFrameOutput, model_kwargs, client)

    def _build_persona_info(self) -> str:
        return {
            "persona": "Senior UI/UX Designer and Front-end Architect",
            "goal": "To create professional, user-friendly HTML wireframes for View/Query interfaces that effectively present data and provide intuitive user interactions following modern UI/UX design principles.",
            "backstory": "With extensive experience in creating data-driven interfaces and query systems, I've mastered the practical application of modern UI/UX patterns across diverse business domains. My approach combines visual design excellence with functional usability, ensuring interfaces remain accessible while efficiently presenting complex data structures. I excel at creating wireframes that balance aesthetics with functionality, designing responsive layouts that work across different screen sizes."
        }

    def _build_task_instruction_prompt(self) -> str:
        return f"""<instruction>
    <core_instructions>
        <title>Wireframe Generation Task</title>
        <task_description>You need to create an HTML wireframe for a View/Query interface based on the provided information about the read model and any additional requirements.</task_description>

        <output_rules>
            <title>Output Format</title>
            <rule id="json_structure">The output must be a JSON object with two keys: "inference" and "result".</rule>
            <rule id="inference">The "inference" value should contain detailed reasoning about the wireframe design decisions, focusing on user experience, component selection, and adherence to requirements. It should not be a reference to general UI/UX strategies.</rule>
            <rule id="result">The "result" value must be an object containing an "html" key. The "html" value will be the complete HTML wireframe code.</rule>
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
                <rule id="layout">Responsive, max-width 1200px</rule>
                <rule id="typography">Clean, readable fonts with proper contrast</rule>
            </default_styles>
        </styling_rules>

        <design_process>
            <title>View/Query Interface Design Process</title>
            <step id="1" name="Default Structure">
                <description>If no specific structural requirements are given, create a standard interface with a search form and a results table. Use appropriate input types based on field data types.</description>
            </step>
            <step id="2" name="Handling Additional Requirements">
                <description>Process ALL additional requirements together.</description>
                <scenario name="Simple Changes (colors, fonts)">Keep the basic structure and apply only the requested style changes.</scenario>
                <scenario name="Component Changes (add filters, pagination)">Keep the basic structure and add the requested components.</scenario>
                <scenario name="Structural Changes (cards, charts, dashboard)">Ignore the basic structure and create a new one as requested.</scenario>
            </step>
            <step id="3" name="Layout and UX">
                <description>Group related fields logically. Use proper spacing, alignment, and label-input associations for a clear visual hierarchy. Include validation indicators and error states. Design for data visualization and intuitive interaction patterns.</description>
            </step>
        </design_process>
        
        <language_and_naming>
            <title>Language and Naming Conventions</title>
            <rule id="language">All user-facing text must be in {self.client.get("preferredLanguage")}.</rule>
            <rule id="labels">Use clear, descriptive labels that reflect business concepts.</rule>
            <rule id="naming">Follow consistent naming patterns for UI elements.</rule>
        </language_and_naming>
    </core_instructions>
</instruction>"""

    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "view_name": "ProductSearch",
            "view_display_name": "Product Search",
            "aggregate_fields": XmlUtil.from_dict([
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
            ]),
            "view_query_parameters": XmlUtil.from_dict([
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
            ]),
            "additional_requirements": "Add sorting by price and creation date, include pagination with 10 items per page"
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "inference": "Based on the Product Search view requirements, I will design a comprehensive search interface. I'll use common style classes for forms and buttons. For custom styles, I'll use an embedded `<style>` block for reusable classes like table and pagination link styles, and inline styles for single-use container elements to optimize the HTML structure. The search form at the top will contain fields for product name, category, and price range. Results will be in a responsive table with sortable columns for price and date. Pagination for 10 items per page is included. The design uses sample data to demonstrate the complete user experience.",
            "result": {
                "html": """<style>
    .search-form-field { flex: 1; min-width: 150px; }
    .results-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .results-table th, .results-table td { padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }
    .results-table th { background-color: #f8f9fa; font-weight: 600; color: #495057; }
    .sortable-header { cursor: pointer; }
    .pagination-link { padding: 8px 12px; border: 1px solid #dee2e6; color: #007bff; text-decoration: none; border-radius: 4px; }
    .pagination-link.active { border-color: #007bff; background-color: #007bff; color: white; }
</style>
<div class="root-div">
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin: 0 0 20px 0; color: #333;">Product Search</h2>
        <div style="display: flex; gap: 15px; margin-bottom: 15px; align-items: flex-end; flex-wrap: wrap;">
            <div class="search-form-field form-group">
                <label for="productName" class="form-label">Product Name</label>
                <input type="text" id="productName" class="form-control" placeholder="Enter product name">
            </div>
            <div class="search-form-field form-group">
                <label for="category" class="form-label">Category</label>
                <select id="category" class="form-control">
                    <option value="">All Categories</option>
                    <option value="Electronics">Electronics</option>
                </select>
            </div>
            <div class="search-form-field form-group">
                <label for="minPrice" class="form-label">Min Price</label>
                <input type="number" id="minPrice" class="form-control" placeholder="0.00">
            </div>
            <div class="search-form-field form-group">
                <label for="maxPrice" class="form-label">Max Price</label>
                <input type="number" id="maxPrice" class="form-control" placeholder="999.99">
            </div>
        </div>
        <div style="text-align: right;">
            <button class="btn btn-secondary" style="margin-right: 10px;">Clear</button>
            <button class="btn btn-primary">Search</button>
        </div>
    </div>

    <div style="overflow-x: auto;">
        <table class="results-table">
            <thead>
                <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Category</th>
                    <th class="sortable-header">Price ↕️</th>
                    <th>Stock Quantity</th>
                    <th class="sortable-header">Created Date ↕️</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>1001</td><td>Wireless Headphones</td><td>Electronics</td><td>$79.99</td><td>45</td><td>2024-01-15</td></tr>
                <tr><td>1002</td><td>Cotton T-Shirt</td><td>Clothing</td><td>$24.99</td><td>120</td><td>2024-01-10</td></tr>
            </tbody>
        </table>
    </div>

    <div style="display: flex; justify-content: center; margin-top: 20px; gap: 5px;">
        <a href="#" class="pagination-link">Previous</a>
        <a href="#" class="pagination-link active">1</a>
        <a href="#" class="pagination-link">2</a>
        <a href="#" class="pagination-link">Next</a>
    </div>
</div>"""
            }
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "view_name": inputs.get("viewName", ""),
            "view_display_name": inputs.get("viewDisplayName", ""),
            "aggregate_fields": XmlUtil.from_dict(inputs.get("aggregateFields", [])),
            "view_query_parameters": XmlUtil.from_dict(inputs.get("viewQueryParameters", [])),
            "additional_requirements": inputs.get("additionalRequirements", "")
        }

    def _post_process_to_structured_output(self, output: CreateReadModelWireFrameOutput) -> CreateReadModelWireFrameOutput:
        try:
            used_common_classes = []
            for class_name in self.COMMON_STYLE_DIC.keys():
                if class_name in output.result.html:
                    used_common_classes.append(class_name)               
            
            if used_common_classes:
                style_content = "<style>\n"
                for class_name in used_common_classes:
                    style_content += self.COMMON_STYLE_DIC[class_name] + "\n"
                style_content += "</style>\n"
                output.result.html = style_content + output.result.html
            
            return output
        except (json.JSONDecodeError, AttributeError):
            raise ValueError("Invalid JSON format")