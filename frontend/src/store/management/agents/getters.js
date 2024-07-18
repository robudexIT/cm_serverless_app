export default {
    getCsdAgents(state){
        return state.csdAgents
    },
    getCsdUpdateAgents(state){
        return state.csdUpdated
    }, 
    getCollectionAgents(state){
        return state.collectionAgents
    },
    getSalesAgents(state){
        return state.salesAgents
    },
    getSalesTeamLeaders(state){
        return state.salesTeamLeaders
    },
    getAgentBelongsTo(state){
        return state.agentBelongsTo
    }
}