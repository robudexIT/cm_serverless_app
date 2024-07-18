import getters from './getters.js'
import mutations from './mutation.js'
import actions from './actions.js'

export default {
    namespaced: true,
    state(){
        return {
            tagMetricsGeneratedData: {},
            cdrMetricsGeneratedData:{},
            tagExportData: {},
            cdrExportData: {},
            grandTotalCounts: null,
            grantTotalDurations: null,
            dateTimeRange: null
        }
    },
    getters,
    mutations,
    actions
}