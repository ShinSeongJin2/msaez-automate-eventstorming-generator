from typing import List

from eventstorming_generator.models.action_model import ActionModel


class MockActionBuilder:
    def __init__(self):
        self.actions: List[ActionModel] = []
        self.current_bc_id: str = ""
        self.current_agg_id: str = ""
        self.current_bc_name: str = ""
        self.current_agg_name: str = ""

    def with_bounded_context(self, bc_index: int):
        bc_name = f"TestBC{bc_index}"
        self.current_bc_name = bc_name
        self.current_bc_id = f"bc-{bc_name.lower()}"
        action = ActionModel(
            objectType="BoundedContext",
            type="create",
            ids={"boundedContextId": self.current_bc_id},
            args={
                "boundedContextName": bc_name,
                "boundedContextAlias": bc_name,
                "description": f"Test Bounded Context {bc_index}",
            },
        )
        self.actions.append(action)
        return self

    def with_aggregate(self, agg_index: int):
        if not self.current_bc_id:
            raise ValueError(
                "BoundedContext must be set before adding Aggregate."
            )

        agg_name = f"{self.current_bc_name}Agg{agg_index}"
        self.current_agg_name = agg_name
        self.current_agg_id = f"agg-{agg_name.lower()}"
        action = ActionModel(
            objectType="Aggregate",
            type="create",
            ids={
                "boundedContextId": self.current_bc_id,
                "aggregateId": self.current_agg_id,
            },
            args={
                "aggregateName": agg_name,
                "aggregateAlias": agg_name,
                "properties": [],
            },
        )
        self.actions.append(action)
        return self

    def with_command_event_pairs(self, count: int):
        if not self.current_bc_id or not self.current_agg_id:
            raise ValueError(
                "BoundedContext and Aggregate must be set before adding command/event pairs."
            )

        for i in range(1, count + 1):
            base_name = f"{self.current_agg_name}Pair{i}"
            cmd_name = f"Do{base_name}"
            evt_name = f"{base_name}Done"

            cmd_id = f"cmd-{cmd_name.lower()}"
            evt_id = f"evt-{evt_name.lower()}"

            # Command
            cmd_action = ActionModel(
                objectType="Command",
                type="create",
                ids={
                    "boundedContextId": self.current_bc_id,
                    "aggregateId": self.current_agg_id,
                    "commandId": cmd_id,
                },
                args={
                    "commandName": cmd_name,
                    "commandAlias": cmd_name,
                    "outputEventIds": [evt_id],
                },
            )
            self.actions.append(cmd_action)

            # Event
            evt_action = ActionModel(
                objectType="Event",
                type="create",
                ids={
                    "boundedContextId": self.current_bc_id,
                    "aggregateId": self.current_agg_id,
                    "eventId": evt_id,
                },
                args={
                    "eventName": evt_name,
                    "eventAlias": evt_name,
                    "properties": [],
                },
            )
            self.actions.append(evt_action)
        return self

    def build(self) -> List[ActionModel]:
        return self.actions