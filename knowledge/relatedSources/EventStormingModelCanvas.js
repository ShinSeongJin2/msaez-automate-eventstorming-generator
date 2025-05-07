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