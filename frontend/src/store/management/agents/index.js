import mutations from './mutations.js'
import actions from './actions.js'
import getters from './getters.js'

export default {
    namespaced: true,
    state(){
        return {
            csdAgents:[],
            collectionAgents:[],
            salesAgents:[],
            salesTeamLeaders:[
                'BRY',
                'ARLENE',
                'DON',
                'IVAN',
                'JOMAN',
                'JHUN',
                'KEN',
                'MHEL',
                'PAULA',
                'RUSTAN',
                'ZARWIN',
                'SALLY'
            ],
            agentBelongsTo: null
        }
    },
    getters,
    mutations,
    actions

}