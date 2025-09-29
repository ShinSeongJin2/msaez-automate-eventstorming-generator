from typing import Any, Dict, Optional
from .xml_base import XmlBaseGenerator
from ..models import CreateElementNamesByDraftsOutput, ExtractedElementNameDetail
from ..utils import XmlUtil

class CreateElementNamesByDrafts(XmlBaseGenerator):
    def __init__(self, model_name: str, model_kwargs: Optional[Dict[str, Any]] = None, client: Optional[Dict[str, Any]] = None):
        self.inputs_types_to_check = ["previousElementNames", "targetBoundedContextName", "aggregateDraft", "description", "requestedEventNames", "requestedCommandNames", "requestedReadModelNames"]
        super().__init__(model_name, CreateElementNamesByDraftsOutput, model_kwargs, client)

    def _build_persona_info(self) -> Dict[str, str]:
        return {
            "persona": "Senior Domain-Driven Design Architect",
            "goal": "To analyze business requirements and domain context to accurately identify and name key elements such as Commands, Events, and Read Models for each Aggregate within a Bounded Context.",
            "backstory": "With years of experience in designing complex, scalable systems using Domain-Driven Design, I specialize in translating ambiguous business needs into concrete, well-defined domain models. I have a keen eye for identifying the core actions, state changes, and queries that form the backbone of a resilient and maintainable system. My expertise lies in ensuring that the naming of these elements is consistent, intuitive, and perfectly aligned with the ubiquitous language of the domain."
        }

    def _build_task_instruction_prompt(self) -> str:
        return f"""<instruction>
    <core_instructions>
        <title>Task: Generate Element Names for Aggregates</title>
        <task_description>
            Based on the provided Bounded Context information, including user requirements, and aggregate drafts, your task is to comprehensively identify and generate the names for Commands, Events, and Read Models for each aggregate.
            You should not only use explicitly requested names from the requested name lists but also infer additional necessary elements by deeply analyzing the domain description and context.
            The generated names must follow specific conventions and accurately reflect the business logic described.
        </task_description>
        
        <input_sections>
            <title>Input Sections Description</title>
            <section name="previousElementNames">Previously generated element names from other Bounded Contexts. Use this to ensure consistency and avoid duplication.</section>
            <section name="targetBoundedContextName">The name of the Bounded Context you are currently processing.</section>
            <section name="aggregateDraft">A list of draft aggregates within the target Bounded Context. You must generate element names for these aggregates.</section>
            <section name="description">Detailed user requirements, including user stories, DDL, and key events. This is the primary source for identifying necessary elements.</section>
            <section name="requestedEventNames">A list of specific event names that must be generated and assigned to an aggregate.</section>
            <section name="requestedCommandNames">A list of specific command names that must be generated and assigned to an aggregate.</section>
            <section name="requestedReadModelNames">A list of specific read model names that must be generated and assigned to an aggregate.</section>
        </input_sections>

        <naming_conventions>
            <title>Naming and Language Conventions</title>
            <rule id="language">All technical names (Commands, Events, Read Models) MUST be in English.</rule>
            <rule id="command_format">Commands MUST follow the `Verb + Noun` pattern (e.g., `CreateOrder`, `UpdateCustomerDetails`).</rule>
            <rule id="event_format">Events MUST follow the `Noun + PastParticiple` pattern (e.g., `OrderCreated`, `CustomerDetailsUpdated`).</rule>
            <rule id="readmodel_format">Read Models MUST follow the `Noun + Purpose` pattern (e.g., `OrderSummary`, `CustomerDashboard`).</rule>
        </naming_conventions>

        <output_rules>
            <title>Output Format</title>
            <rule id="json_structure">
                The output must be a JSON object with a single key: `extracted_element_names`.
                The `extracted_element_names` value MUST be a list of objects.
                Each object in the list MUST represent an aggregate and contain the following keys: `aggregate_name`, `command_names`, `event_names`, and `read_model_names`.
                The `command_names`, `event_names`, and `read_model_names` values must be arrays of strings.
            </rule>
            <rule id="completeness">You MUST generate names for ALL aggregates listed in the `aggregateDraft`.</rule>
            <rule id="no_comments">Do not add any comments in the output JSON.</rule>
        </output_rules>
        
        <inference_guidelines>
            <title>Inference Guidelines</title>
            <guideline id="direct_reasoning">Your reasoning should directly explain how you derived the element names from the provided inputs, referencing specific parts of the description or site map.</guideline>
            <guideline id="command_event_correlation">
                For every Command that modifies the state of an aggregate, there MUST be a corresponding Event. This is a fundamental principle of Event-Sourcing.
                - `Create...` command should have a `...Created` or `...Registered` event.
                - `Update...` command should have a `...Updated` event.
                - `Delete...` or `Dispose...` command should have a `...Deleted` or `...Disposed` event.
                - `Cancel...` command should have a `...Cancelled` event.
                Ensure this one-to-one correspondence is maintained for all state-changing commands you identify or infer.
            </guideline>
            <guideline id="policy_and_command_chaining">
                Consider how events might trigger subsequent actions via policies, creating a chain of commands. This is crucial for modeling complete business workflows.
                - When an event occurs (e.g., `OrderPlaced`), think about what happens next. Does it trigger another process?
                - This next process is often initiated by a new command on the same or a different aggregate (e.g., `ProcessPayment`).
                - Analyze the `description` for cause-and-effect relationships. If a user story says, "When an order is confirmed, an invoice should be generated," this implies an `OrderConfirmed` event triggers a `GenerateInvoice` command.
                - Infer these chained commands even if they are not explicitly requested. This ensures that the interactions between different parts of the domain are captured.
            </guideline>
            <guideline id="analysis_process">
                1.  Thoroughly analyze the `description` (user stories, DDL, events) to understand the underlying business processes and identify key actions, state changes, and data requirements.
                2.  For each aggregate in `aggregateDraft`, compile a list of associated commands, events, and read models.
                3.  Crucially, you must also infer and add element names that are logically necessary based on the domain description, even if they are not explicitly mentioned in the `requested` lists. For instance, if a process described implies a status change, you should infer a corresponding `Update...Status` command and `...StatusChanged` event.
                4.  Ensure all `requestedEventNames`, `requestedCommandNames`, and `requestedReadModelNames` are included for the appropriate aggregates.
                5.  Apply the naming conventions strictly.
            </guideline>
        </inference_guidelines>
    </core_instructions>
</instruction>"""
    
    def _build_json_example_input_format(self) -> Optional[Dict[str, Any]]:
        return {
            "previousElementNames": self._get_xml_from_previousElementNames({}),
            "targetBoundedContextName": "BookManagement",
            "aggregateDraft": XmlUtil.from_dict([
                {
                    "alias": "Book",
                    "name": "Book"
                },
                {
                    "alias": "Author",
                    "name": "Author"
                }
            ]),
            "description": "# Bounded Context Overview: BookManagement\n\n## Role\nManages the lifecycle of books, including registration, status updates, and disposal. It also handles author information and their relationship with books.\n\n## Key Events\n- BookRegistered\n- BookStatusChanged\n- BookDisposed\n- AuthorRegistered\n- AuthorProfileUpdated",
            "requestedEventNames": XmlUtil.from_dict([
                "BookRegistered",
                "BookStatusChanged",
                "BookDisposed",
                "AuthorRegistered",
                "AuthorProfileUpdated"
            ]),
            "requestedCommandNames": XmlUtil.from_dict([
                "CreateBook", 
                "DisposeBook",
                "CreateAuthor"
            ]),
            "requestedReadModelNames": XmlUtil.from_dict([
                "BookList",
                "AuthorDetail"
            ])
        }

    def _build_json_example_output_format(self) -> Dict[str, Any]:
        return {
            "extracted_element_names": [
                {
                    "aggregate_name": "Book",
                    "command_names": [
                        "CreateBook",
                        "UpdateBookStatus",
                        "DisposeBook"
                    ],
                    "event_names": [
                        "BookRegistered",
                        "BookStatusChanged",
                        "BookDisposed"
                    ],
                    "read_model_names": [
                        "BookList"
                    ]
                },
                {
                    "aggregate_name": "Author",
                    "command_names": [
                        "CreateAuthor",
                        "UpdateAuthorProfile"
                    ],
                    "event_names": [
                        "AuthorRegistered",
                        "AuthorProfileUpdated"
                    ],
                    "read_model_names": [
                        "AuthorDetail"
                    ]
                }
            ]
        }
    
    def _build_json_user_query_input_format(self) -> Dict[str, Any]:
        inputs = self.client.get("inputs")
        return {
            "previousElementNames": self._get_xml_from_previousElementNames(inputs.get("previousElementNames")),
            "targetBoundedContextName": inputs.get("targetBoundedContextName"),
            "aggregateDraft": XmlUtil.from_dict(inputs.get("aggregateDraft")),
            "description": inputs.get("description"),
            "requestedEventNames": XmlUtil.from_dict(inputs.get("requestedEventNames")),
            "requestedCommandNames": XmlUtil.from_dict(inputs.get("requestedCommandNames")),
            "requestedReadModelNames": XmlUtil.from_dict(inputs.get("requestedReadModelNames")),
        }
    
    def _get_xml_from_previousElementNames(self, previousElementNames: Dict[str, Dict[str, ExtractedElementNameDetail]]) -> Dict[str, Any]:
        if not previousElementNames:
            return XmlUtil.from_dict([])
        
        base_json = {}
        for bounded_context_name, aggregate_name_dict in previousElementNames.items():
            for aggregate_name, extracted_element_name_detail in aggregate_name_dict.items():
                if bounded_context_name not in base_json:
                    base_json[bounded_context_name] = {}
                dumped_extracted_element_name_detail = extracted_element_name_detail.model_dump()
                base_json[bounded_context_name][aggregate_name] = {
                    "command_names": "[" + ",".join(dumped_extracted_element_name_detail["command_names"]) + "]",
                    "event_names": "[" + ",".join(dumped_extracted_element_name_detail["event_names"]) + "]",
                    "read_model_names": "[" + ",".join(dumped_extracted_element_name_detail["read_model_names"]) + "]"
                }
        
        return XmlUtil.from_dict(base_json)