const changeCase = require("change-case")
const GlobalPromptUtil = require("./GlobalPromptUtil")

/**
 * 주어진 엘리먼트 이름 정보를 토대로 기존의 UUID 이름을 의미가 있는 별칭으로 변환/역복원시켜서 LLM에게 더 의미있는 엘리먼트 이름을 제공하도록 도와줌
 */
class ESAliasTransManager {
    constructor(esValue){
        this.esValue = esValue
        this.UUIDToAliasDic = {}
        this.aliasToUUIDDic = {}

        this._initUUIDAliasForElements()
        this._initUUIDAliasForRelations()
    }

    _initUUIDAliasForElements() {
        Object.keys(this.esValue.elements).forEach(key => {
            const element = this.esValue.elements[key]
            if(!element) return
            
            const aliasToUse = this.__makeAliasToUse(element)
            this.UUIDToAliasDic[key] = aliasToUse
            this.aliasToUUIDDic[aliasToUse] = key


            if(element._type !== "org.uengine.modeling.model.Aggregate") return
            if(!element.aggregateRoot || !element.aggregateRoot.entities || !element.aggregateRoot.entities.elements) return
            const aggregateElements = element.aggregateRoot.entities.elements

            Object.keys(aggregateElements).forEach(entityKey => {
                const entity = aggregateElements[entityKey]
                if(!entity) return

                const entityAliasToUse = this.__makeAliasToUse(entity)
                this.UUIDToAliasDic[entityKey] = entityAliasToUse
                this.aliasToUUIDDic[entityAliasToUse] = entityKey
            })
        })
    }

    _initUUIDAliasForRelations() {
        const getAliasForRelation = (relation) => {
            const sourceAlias = this.__makeAliasToUse(relation.sourceElement)
            const targetAlias = this.__makeAliasToUse(relation.targetElement)
            return `${sourceAlias}-to-${targetAlias}`
        }

        Object.keys(this.esValue.relations).forEach(relationKey => {
            const relation = this.esValue.relations[relationKey]
            if(!relation) return

            const relationAliasToUse = getAliasForRelation(relation)
            this.UUIDToAliasDic[relationKey] = relationAliasToUse
            this.aliasToUUIDDic[relationAliasToUse] = relationKey
        })
    }

    /**
     * 각 엘리먼트 타입마다 충돌되지 않는 의미있는 별칭을 LLM에게 제공하기 위함
     */
    __makeAliasToUse(element) {
        const getFrontId = (element) => {
            switch(element._type.toLowerCase()) {
                case "org.uengine.modeling.model.boundedcontext": return "bc"
                case "org.uengine.modeling.model.aggregate": return "agg"
                case "org.uengine.modeling.model.command": return "cmd"
                case "org.uengine.modeling.model.event": return "evt"
                case "org.uengine.modeling.model.view": return "rm"
                case "org.uengine.modeling.model.actor": return "act"
                case "org.uengine.uml.model.class": return element.isAggregateRoot ? "agg-root" : "ent"
                case "org.uengine.uml.model.enum": return "enum"
                case "org.uengine.uml.model.vo.class": return "vo"
                case "org.uengine.modeling.model.policy": return "pol"
                default: return "obj"
            }
        }


        if(this.UUIDToAliasDic[element.id]) 
            return this.UUIDToAliasDic[element.id]

        const baseAlias = `${getFrontId(element)}-${changeCase.camelCase(element.name)}`
        let aliasToUse = baseAlias
        let i = 2
        
        while(this.aliasToUUIDDic[aliasToUse]) {
            aliasToUse = `${baseAlias}-${i}`
            i++
        }
        return aliasToUse
    }


    getAliasSafely(uuid){
        if(this.UUIDToAliasDic[uuid]) return this.UUIDToAliasDic[uuid]
        return uuid
    }

    getElementAliasSafely(element) {
        if(element.id) return this.getAliasSafely(element.id)
        if(element.elementView) return this.getAliasSafely(element.elementView.id)
        return element.id
    }

    getUUIDSafely(alias){
        if(this.aliasToUUIDDic[alias]) return this.aliasToUUIDDic[alias]
        return alias
    }

    getUUIDSafelyWithNewUUID(alias){
        if(this.aliasToUUIDDic[alias]) return this.aliasToUUIDDic[alias]

        const newUUID = GlobalPromptUtil.getUUID()
        this.aliasToUUIDDic[alias] = newUUID
        this.UUIDToAliasDic[newUUID] = alias
        return newUUID
    }


    transToAliasInActions(actions){
        return this._transActions(actions, (uuid) => this.getAliasSafely(uuid))
    }

    transToUUIDInActions(actions){
        return this._transActions(actions, (alias) => this.getUUIDSafelyWithNewUUID(alias))
    }

    _transActions(actions, transFunc){
        for(const action of actions){
            for(const idKey of Object.keys(action.ids)){
                action.ids[idKey] = transFunc(action.ids[idKey])
            }

            if(action.objectType === "Command" && action.args && action.args.outputEventIds)
                action.args.outputEventIds = action.args.outputEventIds.map(id => transFunc(id))

            if(action.objectType === "Event" && action.args && action.args.outputCommandIds)
                action.args.outputCommandIds = action.args.outputCommandIds.map(outputCommand => {
                    outputCommand.commandId = transFunc(outputCommand.commandId)
                    return outputCommand
                })
        }
        return actions
    }
}

module.exports = ESAliasTransManager