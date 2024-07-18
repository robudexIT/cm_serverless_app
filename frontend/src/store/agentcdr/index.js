import getters from './getters.js'
import mutations from './mutations.js'
import actions from './actions.js'

const agentcdr = {
    namespaced: true,
    state(){
        return {
            csdInBoundSummaries:[],
            csdInBoundAgentDetails:[],
            csdOutBoundSummaries:[],
            csdOutBoundAgentDetails:[],
            collectionOutBoundSummaries:[],
            collectionOutBoundAgentDetails:[],
            salesOutBoundSummaries:[],
            salesOutBoundAgentDetails:[],
            missedCallsSummaries:[],
            missedCallsDetails:[],
            parkedCalls:[],
            voiceMails:[],
            summariesExportData: {},
            detailsExportData: {},
            missedCallsDetailsExport:{},
            mpvTotalCounts: [],
            tagComment :[],
            resultSearchNUmber: []
        }
    },
    getters,
    mutations,
    actions
}

export default agentcdr