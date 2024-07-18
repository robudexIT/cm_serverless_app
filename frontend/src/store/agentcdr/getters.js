export default {
    getCsdInBoundSummaries(state){
        return state.csdInBoundSummaries
    },
    getCsdInBoundAgentDetails(state){
        return state.csdInBoundAgentDetails
    },
    getCsdOutBoundSummaries(state){
        return state.csdOutBoundSummaries
    },
    getCsdOutBoundAgentDetails(state){
        return state.csdOutBoundAgentDetails
    },
    getCollectionOutBoundSummaries(state){
        return state.collectionOutBoundSummaries
    },
    getCollectionOutBoundAgentDetails(state){
        return state.collectionOutBoundAgentDetails
    },
    getSalesOutBoundSummaries(state){
        return state.salesOutBoundSummaries
    },
    getSalesOutBoundAgentDetails(state){
        return state.salesOutBoundAgentDetails
    },
    getMissedCallsSummaries(state){
        return state.missedCallsSummaries
    },
    getMissedCallsDetails(state){
        return state.missedCallsDetails
    },
    getParkedCalls(state){
        return state.parkedCalls
    },
    getVoiceMails(state){
        return state.voiceMails
    },
    getMpvTotalCounts(state){
        return state.mpvTotalCounts
    },

    getTagComment(state){
        return state.tagComment 
    }, 
    getSummariesExportData(state){
        return  state.summariesExportData
    },
    getDetailsExportData(state){
        return state.detailsExportData
    },
    getMissedCallsDetailsExport(state){
        return state.missedCallsDetailsExport
    },
    getResultSearchNUmber(state){
        return state.resultSearchNUmber 
    } 
}