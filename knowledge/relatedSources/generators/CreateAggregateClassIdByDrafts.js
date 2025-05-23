const FormattedJSONAIGenerator = require("../../FormattedJSONAIGenerator")
const { ESValueSummaryGenerator } = require("..")
const ESActionsUtil = require("../../es-ddl-generators/modules/ESActionsUtil")
const { ESValueSummarizeWithFilter } = require("../helpers")
const ActionsProcessorUtils = require("../../es-ddl-generators/modules/ESActionsUtilProcessors/ActionsProcessorUtils")
const ESAliasTransManager = require("../../es-ddl-generators/modules/ESAliasTransManager")
const changeCase = require('change-case');
const { z } = require("zod")
const { zodResponseFormat } = require("../../utils")

class CreateAggregateClassIdByDrafts extends FormattedJSONAIGenerator{
    constructor(client){
        super(client);

        this.generatorName = "CreateAggregateClassIdByDrafts"
        this.checkInputParamsKeys = ["draftOption", "targetReferences", "esValue", "userInfo", "information"]
        this.progressCheckStrings = ["inference", "actions"]

        this.initialResponseFormat = zodResponseFormat(
            z.object({
                inference: z.string(),
                result: z.object({
                    actions: z.array(
                        z.object({
                            objectType: z.literal("ValueObject"),
                            ids: z.object({
                                boundedContextId: z.string(),
                                aggregateId: z.string(),
                                valueObjectId: z.string()
                            }).strict(),
                            args: z.object({
                                valueObjectName: z.string(),
                                referenceClass: z.string(),
                                properties: z.array(
                                    z.object({
                                        name: z.string(),
                                        type: z.string(),
                                        isKey: z.boolean()
                                    }).strict()
                                )
                            }).strict()
                        }).strict()
                    )
                }).strict()
            }).strict(),
            "instruction"
        )
    }

    /**
     * @description 
     * Aggregate 간의 참조 관계를 기반으로 클래스 ID를 생성하는 제너레이터를 생성합니다.
     * 이벤트 스토밍 모델에서 Aggregate 간의 양방향 참조를 단방향으로 최적화하고,
     * 적절한 ID 클래스를 자동으로 생성하는 기능을 제공합니다.
     * 
     * @example 기본적인 Aggregate 클래스 ID 생성
     * const generator = CreateAggregateClassIdByDrafts.createGeneratorByDraftOptions({
     *   onGenerationSucceeded: (returnObj) => {
     *     // 생성된 클래스 ID 정보로 이벤트 스토밍 모델 업데이트
     *     esValue.elements = returnObj.modelValue.createdESValue.elements
     *     esValue.relations = returnObj.modelValue.createdESValue.relations
     *   },
     *   onGenerationDone: () => {
     *     console.log("클래스 ID 생성 완료")
     *   }
     * })
     * 
     * // 제너레이터 초기화 및 실행
     * generator.initInputs(
     *   mocks.getEsDraft("libraryService"),
     *   mocks.getEsValue("libraryService", ["remainOnlyAggregate", "classId"]),
     *   mocks.esConfigs.userInfo,
     *   mocks.esConfigs.information
     * )
     * generator.generateIfInputsExist()
     * 
     * @example 진행 상태 모니터링을 포함한 고급 사용
     * const generator = CreateAggregateClassIdByDrafts.createGeneratorByDraftOptions({
     *   onFirstResponse: (returnObj) => {
     *     console.log("초기 응답 수신")
     *   },
     *   onModelCreated: (returnObj) => {
     *     console.log("모델 생성됨")
     *   },
     *   onGenerationSucceeded: (returnObj) => {
     *     // 생성 성공 처리
     *   },
     *   onGenerationDone: () => {
     *     // 모든 Class ID 생성 완료시 처리
     *     console.log("모든 Class ID 생성 완료")
     *   },
     *   onRetry: (returnObj) => {
     *     console.log(`오류 발생: ${returnObj.errorMessage}`)
     *   },
     *   onStopped: () => {
     *     console.log("생성 중단됨")
     *   }
     * })
     *
     * @note
     * - callbacks.onFirstResponse: 첫 번째 응답 수신 시 호출
     * - callbacks.onModelCreated: 모델 생성 완료 시 호출
     * - callbacks.onGenerationSucceeded: 각 생성 단계 성공 시 호출
     * - callbacks.onRetry: 오류 발생으로 재시도 필요 시 호출
     * - callbacks.onStopped: 생성 프로세스 중단 시 호출
     * - callbacks.onGenerationDone: 모든 생성 작업 완료 시 호출
     * - initInputs 메서드를 통해 필요한 입력값을 설정한 후 generateIfInputsExist를 호출하여 생성 시작
     * - 양방향 참조가 있는 경우 자동으로 단방향으로 최적화됨
     */
    static createGeneratorByDraftOptions(callbacks){
        const generator = new CreateAggregateClassIdByDrafts({
            input: null,

            onSend: (input, stopCallback) => {
                if(callbacks.onSend)
                    callbacks.onSend(input, stopCallback)
            },

            onFirstResponse: (returnObj) => {
                if(callbacks.onFirstResponse)
                    callbacks.onFirstResponse(returnObj)
            },

            onThink: (returnObj, thinkText) => {
                if(callbacks.onThink)
                    callbacks.onThink(returnObj, thinkText)
            },

            onModelCreatedWithThinking: (returnObj) => {
                if(callbacks.onModelCreatedWithThinking)
                    callbacks.onModelCreatedWithThinking(returnObj)
            },

            onModelCreated: (returnObj) => {
                if(callbacks.onModelCreated)
                    callbacks.onModelCreated(returnObj)
            },

            onGenerationSucceeded: (returnObj) => {
                if(callbacks.onGenerationSucceeded)
                    callbacks.onGenerationSucceeded(returnObj)

                if(generator.generateIfInputsExist())
                    return


                if(callbacks.onGenerationDone)
                    callbacks.onGenerationDone()
            },

            onRetry: (returnObj) => {
                console.warn(`[!] An error occurred during aggregate class id creation, please try again.\n* Error log \n${returnObj.errorMessage}`)

                if(callbacks.onRetry)
                    callbacks.onRetry(returnObj)
            },

            onStopped: () => {
                if(callbacks.onStopped)
                    callbacks.onStopped()
            }
        })

        generator.initInputs = (draftOptions, esValue, userInfo, information) => {
            let draftOptionStructure = {}
            for(const boundedContextId of Object.keys(draftOptions)) {
                draftOptionStructure[boundedContextId] = draftOptions[boundedContextId].structure
            }

            const references = []
            for(const boundedContextId of Object.keys(draftOptionStructure)) {
                for(const structure of draftOptionStructure[boundedContextId]) {
                    for(const vo of structure.valueObjects) {
                        if('referencedAggregate' in vo) {
                            references.push({
                                fromAggregate: structure.aggregate.name,
                                toAggregate: vo.referencedAggregate.name,
                                referenceName: vo.name
                            })
                        }
                    }
                }
            }

            if(references.length > 0) {
                const processedPairs = new Set()
                const inputs = []

                references.forEach(ref => {
                    const pairKey = [ref.fromAggregate, ref.toAggregate].sort().join('-')
                    
                    if(!processedPairs.has(pairKey)) {
                        processedPairs.add(pairKey)

                        const bidirectionalRefs = references.filter(r => 
                            (r.fromAggregate === ref.fromAggregate && r.toAggregate === ref.toAggregate) ||
                            (r.fromAggregate === ref.toAggregate && r.toAggregate === ref.fromAggregate)
                        )

                        const targetReferences = bidirectionalRefs.map(r => r.referenceName)

                        inputs.push({
                            draftOption: draftOptionStructure,
                            esValue: esValue,
                            userInfo: userInfo,
                            information: information,
                            targetReferences: targetReferences
                        })
                    }
                })

                generator.inputs = inputs
            }
            else
                generator.inputs = []
        }

        generator.generateIfInputsExist = () => {
            if(generator.inputs.length > 0) {
                generator.client.input = generator.inputs.shift()
                generator.generate()
                return true
            }
            return false
        }

        return generator
    }

    async onGenerateBefore(inputParams){
        inputParams.esValue = JSON.parse(JSON.stringify(inputParams.esValue))
        inputParams.esAliasTransManager = new ESAliasTransManager(inputParams.esValue)
        inputParams.summarizedESValue = ESValueSummarizeWithFilter.getSummarizedESValue(
            inputParams.esValue, ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES.aggregateOuterStickers, 
            inputParams.esAliasTransManager
        )

        inputParams.subjectText = `Creating ID Classes for ${inputParams.targetReferences.join(', ')}`
        if(!(await this.isCreatedPromptWithinTokenLimit())) {
            const leftTokenCount = await this.getCreatePromptLeftTokenCount({summarizedESValue: {}})
            if(leftTokenCount <= 100)
                throw new Error("[!] The size of the draft being passed is too large to process.")

            console.log(`[*] 토큰 제한이 초과되어서 이벤트 스토밍 정보를 제한 수치까지 요약해서 전달함`)
            console.log(`[*] 요약 이전 Summary`, inputParams.summarizedESValue)
            const requestContext = this._buildRequestContext(inputParams)
            inputParams.summarizedESValue = await ESValueSummaryGenerator.getSummarizedESValueWithMaxTokenSummarize(
                requestContext,
                inputParams.esValue,
                ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES.aggregateOuterStickers,
                leftTokenCount,
                this.modelInfo.requestModelName,
                inputParams.esAliasTransManager
            )
            console.log(`[*] 요약 이후 Summary`, inputParams.summarizedESValue)
        }
    }

    _buildRequestContext(inputParams) {
    const relationships = [];
    for (const boundedContextId of Object.keys(inputParams.draftOption)) {
        for (const structure of inputParams.draftOption[boundedContextId]) {
            if (structure.valueObjects) {
                for (const vo of structure.valueObjects) {
                    if (vo.referencedAggregate) {
                        relationships.push({
                            from: structure.aggregate.name,
                            to: vo.referencedAggregate.name,
                            reference: vo.name
                        });
                    }
                }
            }
        }
    }

    const relationshipDescriptions = relationships
        .filter(rel => inputParams.targetReferences.includes(rel.reference))
        .map(rel => `${rel.from} -> ${rel.to} (via ${rel.reference})`);

    return `Analyzing aggregate relationships for creating ID Classes:
${relationshipDescriptions.join('\n')}

Focus on elements related to these aggregates and their relationships, particularly for implementing the following references: ${inputParams.targetReferences.join(', ')}.

Key considerations:
1. Aggregate relationships and their boundaries
2. Value objects that implement these relationships
3. Properties and identifiers needed for references
4. Related commands and events that might use these references`;
    }


    __buildAgentRolePrompt(){
        return `You are a senior DDD (Domain-Driven Design) expert with extensive experience in:
1. Domain model design and implementation in complex enterprise systems
2. Precise bounded context definition and strategic context mapping
3. Optimizing aggregate relationships and reference management
4. Implementing clean architecture principles in distributed systems
5. Modeling complex domain relationships with optimal referential integrity

Your specialized knowledge areas include:
- Aggregate identity management and lifecycle control
- Entity-to-ID class transformation patterns 
- Relationship optimization between aggregates
- Foreign key vs. reference object trade-offs
- Strategic domain object coupling/cohesion balancing
- Domain invariant protection across aggregate boundaries
- Efficient query patterns with minimal aggregate traversal
- Performance implications of reference design choices

You excel at creating optimal, unidirectional reference structures that maintain domain integrity while minimizing coupling between aggregates.
`
    }

    __buildTaskGuidelinesPrompt(){
        return `You will need to create the appropriate ValueObject that references other Aggregates as foreign keys, based on the provided EventStorming configuration draft.

Please follow these rules:
1. Foreign Key Value Object Generation:
   * CRITICAL: Only implement ONE DIRECTION of reference between aggregates
   * When choosing direction, consider:
     - Which aggregate is the owner of the relationship
     - Which side is more stable and less likely to change
     - Query patterns and performance requirements
   * Example: In Order-Customer relationship, Order should reference Customer (not vice-versa)

2. Relationship Direction Decision:
   * NEVER create bidirectional references, even if suggested in the draft
   * For each pair of aggregates, choose only ONE direction based on:
     - Lifecycle dependency (dependent aggregate references the independent one)
     - Business invariants (aggregate enforcing rules references required data)
     - Access patterns (optimize for most frequent queries)

3. Property Replication:
   * Only replicate properties that are highly unlikely to change (e.g., birthDate, gender)
   * These near-immutable properties are safe for caching as they remain constant throughout the entity's lifecycle
   * Strictly avoid replicating volatile properties that change frequently
   * Each replicated property must be justified based on its immutability and business value
   * Examples of safe-to-replicate properties:
     - Date of birth (remains constant)
     - Gender (rarely changes)
     - Country of birth (permanent)
   * Examples of properties to avoid replicating:
     - Address (frequently changes)
     - Email (moderately volatile)
     - Phone number (changes occasionally)

4. Technical Considerations:
   * Handle composite keys appropriately when referenced Aggregate uses multiple identifiers
   * Include proper indexing hints for foreign key fields
   * Consider implementing lazy loading for referenced data
   * Maintain referential integrity through proper constraints

5. Edge Cases:
   * Handle null references and optional relationships
   * Consider cascade operations impact
   * Plan for reference cleanup in case of Aggregate deletion
   * Implement proper validation for circular references

6. Output Format:
   * Provide clean JSON without comments
   * Use consistent property naming
   * Include all required metadata
   * Specify proper data types and constraints

7. Output Limit
   * Generate the appropriate ValueObject only for the referceAggregate corresponding to the given targetReferences. However, if the creation of a ValueObject for a given targetReferences also creates bidirectional references, only one of them should be created as a ValueObject.
`
    }

    __buildInferenceGuidelinesPrompt() {
        return `
Inference Guidelines:
1. The process of reasoning should be directly related to the output result, not a reference to a general strategy.
2. Begin by comprehensively analyzing the provided aggregate relationships and domain context.
3. Focus on key aspects:
   - **Domain Alignment:** Assess how the value object and its references integrate into the broader business domain.
   - **Unidirectional Relationship:** Ensure that references are implemented in a strictly unidirectional manner; choose the direction based on aggregate dependency, lifecycle, and stability.
   - **Property Considerations:** Identify and replicate only those properties that are immutable and critical for maintaining referential integrity.
`;
    }

    __buildRequestFormatPrompt(){
        return ESValueSummarizeWithFilter.getGuidePrompt()
    }

    __buildJsonResponseFormat() {
        return `
{
    "inference": "<inference>",
    "result": {
        "actions": [
            {
                "objectType": "ValueObject",
                "ids": {
                    "boundedContextId": "<boundedContextId>",
                    "aggregateId": "<aggregateId>",
                    "valueObjectId": "<valueObjectId>"
                },
                "args": {
                    "valueObjectName": "<valueObjectName>",
                    "referenceClass": "<referenceClassName>",
                    "properties": [
                        {
                            "name": "<propertyName>",
                            ["type": "<propertyType>"], // If the type is String, do not specify the type.
                            ["isKey": true] // Write only if there is a primary key.
                        }
                    ]
                }
            }
        ]
    }
}`
    }


    __buildJsonExampleInputFormat() {
        return {
            "Summarized Existing EventStorming Model": {
                "deletedProperties": ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES.aggregateOuterStickers,
                "boundedContexts": [
                    {
                        "id": "bc-order",
                        "name": "orderservice",
                        "aggregates": [
                            {
                                "id": "agg-order",
                                "name": "Order",
                                "properties": [
                                    {
                                        "name": "orderId",
                                        "type": "Long",
                                        "isKey": true
                                    },
                                    {
                                        "name": "orderDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "totalAmount",
                                        "type": "Integer"
                                    }
                                ]
                            },
                            {
                                "id": "agg-customer",
                                "name": "Customer",
                                "properties": [
                                    {
                                        "name": "customerId",
                                        "type": "Long",
                                        "isKey": true
                                    },
                                    {
                                        "name": "name"
                                    },
                                    {
                                        "name": "gender"
                                    },
                                    {
                                        "name": "birthDate",
                                        "type": "Date"
                                    },
                                    {
                                        "name": "email"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },

            "Suggested Structure": {
                "OrderManagement": [
                    {
                        "aggregate": {
                            "name": "Order",
                            "alias": "Order"
                        },
                        "enumerations": [],
                        "valueObjects": [
                            {
                                "name": "CustomerReference",
                                "alias": "Customer Reference",
                                "referencedAggregate": {
                                    "name": "Customer",
                                    "alias": "Customer"
                                }
                            }
                        ]
                    }
                ],
                "CustomerManagement": [
                    {
                        "aggregate": {
                            "name": "Customer",
                            "alias": "Customer"
                        },
                        "enumerations": [],
                        "valueObjects": [
                            {
                                "name": "OrderReference",
                                "alias": "Order Reference",
                                "referencedAggregate": {
                                    "name": "Order",
                                    "alias": "Order"
                                }
                            }
                        ]
                    }
                ]
            },

            "Target References": ["OrderReference", "CustomerReference"]
        }
    }

    __buildJsonExampleOutputFormat() {
        return {
            "inference": `- Unidirectional Reference Selection: Among the aggregates in the model (Order and Customer), the decision was made to establish a one-way reference from the Order aggregate to the Customer aggregate. This aligns with the requirement to avoid bidirectional references, ensuring that only one direction is implemented.
- Domain & Lifecycle Considerations: The Customer aggregate is recognized as the stable, independent entity, making it the ideal candidate for being referenced by the Order. This approach addresses lifecycle dependencies and reflects real-world business invariants.
- Property Replication: Only properties that are immutable and critical for maintaining referential integrity—namely, the primary key (customerId), alongside near-immutable properties such as gender and birthDate—are replicated. This minimizes redundancy and avoids the pitfalls of copying volatile data.
Overall, this inference ensures that the generated ValueObject adheres to the design rules, maintains domain clarity, and promotes referential integrity without creating unwanted bidirectional dependencies.`,
            "result": {
                "actions": [
                    {
                        "objectType": "ValueObject",
                        "ids": {
                            "boundedContextId": "bc-order",
                            "aggregateId": "agg-order",
                            "valueObjectId": "vo-customer-id"
                        },
                        "args": {
                            "valueObjectName": "CustomerReference",
                            "referenceClass": "Customer",
                            "properties": [
                                {
                                    "name": "customerId",
                                    "type": "Long",
                                    "isKey": true
                                },
                                {
                                    "name": "gender"
                                },
                                {
                                    "name": "birthDate",
                                    "type": "Date"
                                }
                            ]
                        }
                    }
                    // Note: Deliberately NOT including reverse reference from Customer to Order
                ]
            }
        }
    }

    __buildJsonUserQueryInputFormat() {
        return {
            "Summarized Existing EventStorming Model": JSON.stringify(this.client.input.summarizedESValue),

            "Suggested Structure": JSON.stringify(this.client.input.draftOption),

            "Target References": this.client.input.targetReferences,

            "Final Check": `
CRITICAL RULES FOR REFERENCE GENERATION:
1. STRICT UNIDIRECTIONAL REFERENCE ONLY:
   - When draft shows two-way relationship, you MUST choose only ONE direction
   - Never generate both directions of references
   - Example: If Order->Customer and Customer->Order are in draft, implement ONLY Order->Customer

2. Direction Selection Criteria:
   - Choose based on dependency (dependent entity references independent one)
   - Consider lifecycle management (e.g., Order depends on Customer)
   - Optimize for most common query patterns

3. Property Guidelines:
   - Avoid adding properties that might change
   - Include only the minimum required reference properties

4. Implementation Check:
   - Verify you're generating only ONE direction of reference
   - Double-check you haven't created any bidirectional references
`,
        }
    }


    onThink(returnObj, thinkText){
        returnObj.directMessage = `Creating ID Classes... (${this.getTotalOutputTextLength(returnObj)} characters generated)`
    }

    onCreateModelGenerating(returnObj){
        returnObj.directMessage = `Creating ID Classes... (${this.getTotalOutputTextLength(returnObj)} characters generated)`
    }

    onCreateModelFinished(returnObj){
        let actions = returnObj.modelValue.aiOutput.result.actions
        this._filterInvalidActions(actions)
        this._filterBidirectionalActions(actions)
        if(actions.length === 0) {
            if(this.leftRetryCount > 0)
                throw new Error("No actions generated")

            console.warn("[*] ClassId 생성에 여러번의 시도에도 불구하고 실패했습니다. 이것 때문에 전체 과정을 중단하는 것보다는 다음 단계로 넘어가는게 좋아보이기 때문에 넘어가겠습니다.")
            returnObj.modelValue = {
                ...returnObj.modelValue,
                actions: [],
                createdESValue: null
            }
            returnObj.directMessage = `Failed to generate ClassId. Skipping this step.`
            return returnObj
        }


        let {actions: appliedActions, createdESValue: createdESValue} = this._getActionAppliedESValue(actions)

        returnObj.modelValue = {
            ...returnObj.modelValue,
            actions: appliedActions,
            createdESValue: createdESValue
        }
        returnObj.directMessage = `Creating ID Classes... (${this.getTotalOutputTextLength(returnObj)} characters generated)`
    }

    _filterInvalidActions(actions){
         for(let i = actions.length - 1; i >= 0; i--) {
            const action = actions[i]
            if(!action.args || !action.args.valueObjectName || 
               !action.ids || !action.ids.valueObjectId) {
                actions.splice(i, 1);
                continue
            }
            
            const isValidReference = this.client.input.targetReferences.some(
                target => action.args.valueObjectName.toLowerCase().includes(target.toLowerCase())
            );
            
            if (!isValidReference) {
                actions.splice(i, 1);
            }
        }
    }

    _filterBidirectionalActions(actions){
        for (let i = 0; i < actions.length; i++) {
            const action1 = actions[i];
            const agg1Name = this.client.input.esValue.elements[this.client.input.esAliasTransManager.getUUIDSafely(action1.ids.aggregateId)].name;
            if(!agg1Name) continue
            
            for (let j = i + 1; j < actions.length; j++) {
                const action2 = actions[j];
                const agg2Name = this.client.input.esValue.elements[this.client.input.esAliasTransManager.getUUIDSafely(action2.ids.aggregateId)].name;
                if(!agg2Name) continue
                
                if (action1.args.referenceClass === agg2Name && 
                    action2.args.referenceClass === agg1Name) {
                    actions.splice(j, 1);
                    j--; 
                }
            }
        }
    }

    _getActionAppliedESValue(actions) {
        actions = this.client.input.esAliasTransManager.transToUUIDInActions(actions)
        this._modifyActionsForReferenceClassValueObject(actions)

        let esValueToModify = JSON.parse(JSON.stringify(this.client.input.esValue))

        let createdESValue = ESActionsUtil.getActionAppliedESValue(actions, this.client.input.userInfo, this.client.input.information, esValueToModify)

        return { actions, createdESValue }
    }

    _modifyActionsForReferenceClassValueObject(actions){
        let actionsToAdd = []
        for (let action of actions) {
            if (!action.args || !action.args.properties) continue;

            const fromAggregate = this.client.input.esValue.elements[action.ids.aggregateId]
            const toAggregate = this.__getAggregateByName(this.client.input.esValue, action.args.referenceClass)
            if(!fromAggregate || !toAggregate) {
                console.warn("[*] 참조 Aggregate를 발견하지 못해서 Aggregate 관계를 형성하지 못함", {action})
                continue
            }
            

            action.args.valueObjectName = `${toAggregate.name}Id`

            const toAggregateKeyProp = toAggregate.aggregateRoot.fieldDescriptors.find(prop => prop.isKey)
            if (!toAggregateKeyProp) continue

            const actionKeyProp = action.args.properties.find(prop => prop.isKey)
            if (actionKeyProp) {
                actionKeyProp.name = toAggregateKeyProp.name
                actionKeyProp.type = toAggregateKeyProp.className
                actionKeyProp.isKey = true
                actionKeyProp.referenceClass = toAggregate.name
                actionKeyProp.isOverrideField = true
            }


            this._addAggregateRelation(fromAggregate, toAggregate, this.client.input.esValue)


            actionsToAdd.push(
                {
                    "objectType": "Aggregate",
                    "type": "update",
                    "ids": {
                        "boundedContextId": action.ids.boundedContextId,
                        "aggregateId": action.ids.aggregateId
                    },
                    "args": {
                        "properties": [
                            {
                                "name": changeCase.camelCase(action.args.valueObjectName),
                                "type": action.args.valueObjectName,
                                "referenceClass": toAggregate.name,
                                "isOverrideField": true
                            }
                        ]
                    }
                },
            )
        }
        actions.push(...actionsToAdd)
    }

    _addAggregateRelation(fromAggregate, toAggregate, esValue){
        for(const relation of Object.values(esValue.relations).filter(relation => relation)) {
            if(relation.sourceElement && relation.targetElement) {
                if(relation.sourceElement.id === fromAggregate.id && relation.targetElement.id === toAggregate.id)
                    return
            }
        }

        const aggregateRelation = ActionsProcessorUtils.getEventStormingRelationObjectBase(fromAggregate, toAggregate)
        console.log("[*] 생성된 관계 추가", {aggregateRelation})
        esValue.relations[aggregateRelation.id] = aggregateRelation   
    }


    __getAggregateByName(esValue, aggregateName){
        for(let element of Object.values(esValue.elements).filter(element => element)) {
            if(element._type === "org.uengine.modeling.model.Aggregate" && element.name === aggregateName && element.id)
                return element
        }
        return null
    }
}

module.exports = CreateAggregateClassIdByDrafts;