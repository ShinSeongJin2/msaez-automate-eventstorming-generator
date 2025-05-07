let thinkingUpdateInterval = undefined
const createThinkingUpdateInterval = (elapsedSeconds=0, subjectText) => {
    clearThinkingUpdateInterval()

    const updateMessage = (elapsedSeconds, subjectText) => {
        this.generatorProgressDto.displayMessage = `Thinking for ${elapsedSeconds} second${elapsedSeconds > 1 ? 's' : ''}... (Subject: ${subjectText})`
    }

    updateMessage(elapsedSeconds, subjectText)
    thinkingUpdateInterval = setInterval(() => {
        elapsedSeconds += 1
        updateMessage(elapsedSeconds, subjectText)
    }, 1000)
}
const clearThinkingUpdateInterval = () => {
    if(thinkingUpdateInterval) {
        clearInterval(thinkingUpdateInterval)
        thinkingUpdateInterval = undefined
    }
}
const addGlobalProgressCount = () => {
    this.generatorProgressDto.currentGlobalProgressCount += 1
    this.generatorProgressDto.globalProgress = Math.min(100, Math.round(this.generatorProgressDto.currentGlobalProgressCount / this.generatorProgressDto.totalGlobalProgressCount * 100))
}

const byFunctionCallbacks = {
    onSend: (input, stopCallback) => {
        this.AggregateDraftDialogDto = {
            ...this.AggregateDraftDialogDto,
            isShow: false
        }

        this.generatorProgressDto.generateDone = false
        this.generatorProgressDto.displayMessage = ""
        this.generatorProgressDto.progress = null
        this.generatorProgressDto.actions.stopGeneration = stopCallback

        createThinkingUpdateInterval(0, input.subjectText)
    },

    onFirstResponse: (returnObj) => {
        clearThinkingUpdateInterval()
        this.AggregateDraftDialogDto = {
            ...this.AggregateDraftDialogDto,
            isShow: false
        }

        this.generatorProgressDto.generateDone = false
        this.generatorProgressDto.displayMessage = returnObj.directMessage
        this.generatorProgressDto.progress = 0
        this.generatorProgressDto.actions.stopGeneration = returnObj.actions.stopGeneration
    },

    onThink: (returnObj, thinkText) => {
        clearThinkingUpdateInterval()
        this.generatorProgressDto.displayMessage = returnObj.directMessage
        this.generatorProgressDto.thinkMessage = this.generatorProgressDto.previousThinkingMessage + "\n" + thinkText
        this.generatorProgressDto.progress = 0
    },

    onModelCreatedWithThinking: (returnObj) => {
        clearThinkingUpdateInterval()
        this.generatorProgressDto.displayMessage = returnObj.directMessage
        this.generatorProgressDto.progress = returnObj.progress

        if(returnObj.modelValue && returnObj.modelValue.createdESValue) {
            this.changedByMe = true
            this.$set(this.value, "elements", returnObj.modelValue.createdESValue.elements)
            this.$set(this.value, "relations", returnObj.modelValue.createdESValue.relations)
        }
    },

    onGenerationSucceeded: (returnObj) => {
        clearThinkingUpdateInterval()
        this.generatorProgressDto.previousThinkingMessage = this.generatorProgressDto.thinkMessage

        if(returnObj.modelValue.removedElements && returnObj.modelValue.removedElements.length > 0) {
            returnObj.modelValue.removedElements.forEach(element => {
                if(this.value.elements[element.id])
                    this.removeElementAction(this.value.elements[element.id])
            })
        }

        addGlobalProgressCount()
        if(returnObj.modelValue && returnObj.modelValue.createdESValue) {
            this.changedByMe = true
            this.$set(this.value, "elements", returnObj.modelValue.createdESValue.elements)
            this.$set(this.value, "relations", returnObj.modelValue.createdESValue.relations)
        }
    },

    onRetry: (returnObj) => {
        clearThinkingUpdateInterval()
        console.warn(`[!] An error occurred during creation, please try again.\n* Error log \n${returnObj.errorMessage}`)
        this.AggregateDraftDialogDto = {
            ...this.AggregateDraftDialogDto,
            isShow: true,
            draftUIInfos: {
                leftBoundedContextCount: 0
            },
            isGeneratorButtonEnabled: true
        }
        this.generatorProgressDto.generateDone = true
        this.isEditable = true
    },

    onStopped: () => {
        clearThinkingUpdateInterval()
        this.generatorProgressDto.generateDone = true
        this.isEditable = true
    },

    onGenerationDone: () => {
        clearThinkingUpdateInterval()
        this.generatorProgressDto.generateDone = true
    }
}

this.generators.CreateAggregateActionsByFunctions.generator = CreateAggregateActionsByFunctions.createGeneratorByDraftOptions(
    {
        ...byFunctionCallbacks,
        onGenerationDone: () => {
            // 이미 기존에 생성한 다른 BC 내용이 있더라도 적절하게 클래스 ID를 생성시키기 위해서 임시 초안 생성
            const draftOptionsByEsValue = {}
            Object.entries(DraftGeneratorByFunctions.esValueToAccumulatedDrafts(
                this.value,
                {name: ""}
            )).forEach(([boundedContextName, draftOptions]) => {
                draftOptionsByEsValue[boundedContextName] = {
                    structure: draftOptions
                }
            })

            Object.keys(this.selectedDraftOptions).forEach(boundedContextName => {
                draftOptionsByEsValue[boundedContextName] = this.selectedDraftOptions[boundedContextName]
            })
            
            this.generators.CreateAggregateClassIdByDrafts.generator.initInputs(
                draftOptionsByEsValue,
                this.value,
                this.userInfo,
                this.information
            )
            if(this.generators.CreateAggregateClassIdByDrafts.generator.generateIfInputsExist())
                return


            // 별도로 추가시킬 클래스 ID가 없을 경우, 바로 커맨드 생성 단계로 이동
            this.generators.CreateCommandActionsByFunctions.generator.initInputs(
                this.selectedDraftOptions,
                this.value,
                this.userInfo,
                this.information
            )
            if(this.generators.CreateCommandActionsByFunctions.generator.generateIfInputsExist())
                return


            byFunctionCallbacks.onGenerationDone()
        }
    }
)

this.generators.CreateAggregateClassIdByDrafts.generator = CreateAggregateClassIdByDrafts.createGeneratorByDraftOptions(
    {
        ...byFunctionCallbacks,
        onGenerationDone: () => {
            this.generators.CreateCommandActionsByFunctions.generator.initInputs(
                this.selectedDraftOptions,
                this.value,
                this.userInfo,
                this.information
            )
            if(this.generators.CreateCommandActionsByFunctions.generator.generateIfInputsExist())
                return
            
            byFunctionCallbacks.onGenerationDone()
        }
    }
)

this.generators.CreateCommandActionsByFunctions.generator = CreateCommandActionsByFunctions.createGeneratorByDraftOptions({
    ...byFunctionCallbacks,
    onGenerationDone: () => {
        this.generators.CreatePolicyActionsByFunctions.generator.initInputs(
            this.selectedDraftOptions,
            this.value,
            this.userInfo,
            this.information
        )
        if(this.generators.CreatePolicyActionsByFunctions.generator.generateIfInputsExist())
            return

        byFunctionCallbacks.onGenerationDone()
    }
})

this.generators.CreatePolicyActionsByFunctions.generator = CreatePolicyActionsByFunctions.createGeneratorByDraftOptions({
    ...byFunctionCallbacks,
    onGenerationDone: () => {
        this.generators.CommandGWTGeneratorByFunctions.generator.initInputs(
            this.selectedDraftOptions,
            this.value
        )
        if(this.generators.CommandGWTGeneratorByFunctions.generator.generateIfInputsExist())
            return

        byFunctionCallbacks.onGenerationDone()
    }
})

this.generators.CommandGWTGeneratorByFunctions.generator = CommandGWTGeneratorByFunctions.createGeneratorByDraftOptions({
    ...byFunctionCallbacks,
    onGenerationSucceeded: (returnObj) => {
        addGlobalProgressCount()
        if(returnObj.modelValue && returnObj.modelValue.commandsToReplace) {
            this.changedByMe = true
            for(const command of returnObj.modelValue.commandsToReplace)
                this.$set(this.value.elements, command.id, command)
        }
    },

    onGenerationDone: async () => {
        this.generatePBCbyDraftOptions(this.filteredPBCs)
        console.log("[*] 최종 생성 후 PBC 생성 완료", {filteredPBCs: this.filteredPBCs})
        
        this.collectedMockDatas.aggregateDraftScenarios.esValue = structuredClone(
            {
                elements: this.value.elements,
                relations: this.value.relations
            }
        )
        console.log("[*] 시나리오별 테스트를 위한 Mock 데이터 구축 완료", {collectedMockDatas: this.collectedMockDatas.aggregateDraftScenarios})

        this.collectedLogDatas.aggregateDraftScenarios.endTime = new Date().getTime()
        const totalSeconds = (this.collectedLogDatas.aggregateDraftScenarios.endTime - this.collectedLogDatas.aggregateDraftScenarios.startTime) / 1000
        console.log("[*] 최종 생성까지 걸린 총 시간(초)", totalSeconds) 
        
        byFunctionCallbacks.onGenerationDone()

        // AI 생성된 모델을 Project에 저장하기 위해 세팅
        await this.storageDialogReady('save')
        this.storageCondition.projectId = this.projectId
        this.storageCondition.projectName = this.collectedMockDatas.projectName

        if(!localStorage.getItem("blockAutoRefresh"))
            this.$nextTick(() => {
                this.$router.go(0)
            })
    }
})

// 이 Generator의 호출은 ESDialoger.jump()에서 간접적으로 이루어짐
this.generatorsInGeneratorUI.CreateAggregateActionsByFunctions.callbacks = {
    // 공통 처리 루트로 들어가기 위한 작업
    onInputParamsCheckBefore: (inputParams) => {
        console.log("[*] 바로 이벤트 스토밍 생성 실행", {inputParams})

        const newGenerateFromDrafts = () => {
            setTimeout(() => {
                if(this.isModelDefinitionLoaded) {
                    // 이벤트 스토밍 초안으로 부터 '이벤트 스토밍 생성' 버튼을 여러번 눌렀을 경우를 대비
                    // 항상 완전히 초기화된 상태로부터 시작
                    for(const element of Object.values(this.value.elements).filter(element => element))
                        this.removeElementAction(element)

                    this.changedByMe = true
                    this.$set(this.value, "elements", {})
                    this.$set(this.value, "relations", {})
                    this.forceRefreshCanvas()

                    this.generateAggregatesFromDraft(inputParams.draftOptions)
                }
                else {
                    console.log("[*] 모델 정의 로드 대기 중")
                    newGenerateFromDrafts()
                }
            }, 500)
        }
        newGenerateFromDrafts()

        return {stop: true}
    }
}

generateAggregatesFromDraft(draftOptions) {
    console.log("[*] 유저가 선택한 초안 옵션들을 이용해서 모델 생성 로직이 실행됨",
        {prevDraftOptions: JSON.parse(JSON.stringify(draftOptions))}
    )

    // PBC 필터링 & 제거
    let pbc = {}
    let boundedContexts = {}
    
    Object.keys(draftOptions).forEach(key => {
        if(key.includes("PBC")) {
            pbc[key] = draftOptions[key]
        } else {
            boundedContexts[key] = draftOptions[key]
        }
    })

    this.selectedDraftOptions = boundedContexts
    this.filteredPBCs = pbc

    this._removeInvalidReferencedAggregateProperties(boundedContexts)
    this._createBoundedContextsIfNotExists(boundedContexts)
    
    console.log("[*] 초안 전처리 완료", {afterDraftOptions: JSON.parse(JSON.stringify(boundedContexts))})

    this.generatorProgressDto.totalGlobalProgressCount = this._getTotalGlobalProgressCount(boundedContexts)
    this.generatorProgressDto.currentGlobalProgressCount = 0

    this.generatorProgressDto.thinkMessage = ""
    this.generatorProgressDto.previousThinkingMessage = ""
    this.collectedMockDatas.aggregateDraftScenarios.draft = structuredClone(boundedContexts)
    this.collectedLogDatas.aggregateDraftScenarios.startTime = new Date().getTime()
    
    // AI 생성 중에는 수정을 불가능하도록 만듬
    this.isEditable = false

    // 로컬스토리지 데이터가 충분하지 않을 경우, 제대로 저장이 안되는 이슈 해결
    LocalStorageCleanUtil.clean()

    console.log("[*] 생성 데이터 로그", {
        selectedDraftOptions: this.selectedDraftOptions,
        value: this.value,
        userInfo: this.userInfo,
        information: this.information
    })
    this.generators.CreateAggregateActionsByFunctions.generator.initInputs(
        this.selectedDraftOptions,
        this.value,
        this.userInfo,
        this.information
    )
    this.generators.CreateAggregateActionsByFunctions.generator.generateIfInputsExist()
},