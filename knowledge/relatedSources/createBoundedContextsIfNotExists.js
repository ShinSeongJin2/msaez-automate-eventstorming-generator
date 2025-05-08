_createBoundedContextsIfNotExists(draftOptions) {
    for(const context of Object.values(draftOptions)) {
            const bcNameToCheck = context.boundedContext.name
            const isBoundedContextExists = Object.values(this.value.elements).some((element) => 
                element && element._type === "org.uengine.modeling.model.BoundedContext" && element.name.toLowerCase() === bcNameToCheck.toLowerCase()
            )
            if(isBoundedContextExists) continue

            const appliedESValue = ESActionsUtil.getActionAppliedESValue([
                {
                    "objectType": "BoundedContext",
                    "type": "create",
                    "ids": {
                        "boundedContextId": `bc-${context.boundedContext.name}`
                    },
                    "args": {
                        "boundedContextName": context.boundedContext.name,
                        "boundedContextAlias": context.boundedContext.displayName,
                        "description": context.boundedContext.description
                    }
                }
            ], this.userInfo, this.information, this.value)
    }
},