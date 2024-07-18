
const  HTTPADDR = 'http://103.5.6.2/sbtph_api_prod/api' //process.env.VUE_APP_HTTPADDR_OFFFICE
console.log(`this is the api endpoint:${HTTPADDR}`)
const API = {
    phoneLoggedIn: `${HTTPADDR}/active.php`,
    phoneLogggedOut: `${HTTPADDR}/inactive.php`,
    phoneLogsDetails : `${HTTPADDR}/login_logout_details.php`,
    missedCallsSummaries: `${HTTPADDR}/csdinbound/csd_inbound_missed_calls_summary_api.php`,
    missedCallsDetails: `${HTTPADDR}/csdinbound/csd_inbound_missed_calls_details_api.php`,
    voiceMails: `${HTTPADDR}/get_voicemail.php`,
    parkedCalls: `${HTTPADDR}/get_parked_calls.php`,
    mpvTotalCounts: `${HTTPADDR}/get_total_counts.php`,
    getVoiceMails: `${HTTPADDR}/get_voicemail.php`,
    deleteVoiceMails: `${HTTPADDR}/delete_voicemail.php`,
    getParkedCalls: `${HTTPADDR}/get_parked_calls.php`,
    getAgentBelongsTo: `${HTTPADDR}/getCalltype.php`,
    updateAgentBelongsTo: `${HTTPADDR}/collection/updateCallType.php`,

    getCallSummaries: {
        csdinbound:  `${HTTPADDR}/csdinbound/csd_inbound_call_summary_api.php`,
        csdoutbound: `${HTTPADDR}/csdoutbound/csd_outbound_call_summary_api.php`,
        collection: `${HTTPADDR}/collection/collection_call_summary_api.php`,
        sales: `${HTTPADDR}/sales/sales_call_summary_api.php`,
    },
    getCallDetails: {
        csdinbounddetails: `${HTTPADDR}/csdinbound/csd_inbound_call_agent_details_api.php`,
        csdoutbounddetails: `${HTTPADDR}/csdoutbound/csd_outbound_call_agent_details_api.php`,
        collectiondetails: `${HTTPADDR}/collection/collection_call_agent_details_api.php`,
        salesdetails: `${HTTPADDR}/sales/sales_call_agent_details_api.php`,
    },

    // Agent Manamentment Api
    getAllAgents: {
        csd: `${HTTPADDR}/csd_manage.php`,
        collection: `${HTTPADDR}/collection/collection_get_all_collection_agent_api.php`,
        sales:`${HTTPADDR}/sales/sales_manage.php`
    },
    getSingleAgent: {

    },
    createAgent: {
        csd: `${HTTPADDR}/create_csd_agent.php`,
        collection: `${HTTPADDR}/collection/create_collection_agent_api.php`,
        sales: `${HTTPADDR}/sales/create_sales_agent_api.php`
    },
    updateAgent:{
        csd: `${HTTPADDR}/updatecsd.php`,
        collection: `${HTTPADDR}/collection/update_collection_agent_api.php`,
        sales: `${HTTPADDR}/sales/update_sales_agent_api.php`
    },
    deleteAgent: {
        csd: `${HTTPADDR}/delete_csd.php`,
        collection: `${HTTPADDR}/collection/delete_collection_agent_api.php`,
        sales: `${HTTPADDR}/sales/delete_sales_agent_api.php`
    },
    getCommentTag: {
        csdinbounddetails: `${HTTPADDR}/csdinbound/get_inbound_call_comment_api.php`,
        csdoutbounddetails: `${HTTPADDR}/csdoutbound/get_outbound_call_comment_api.php`,
        collectiondetails: `${HTTPADDR}/collection/get_collection_call_comment_api.php`,
        salesdetails: `${HTTPADDR}/sales/get_sales_call_comment_api.php`,
        missedcalls: `${HTTPADDR}/csdinbound/get_inbound_call_comment_api.php`,
    },

    putCommentTag: {
        csdinbounddetails: `${HTTPADDR}/csdinbound/put_inbound_call_comment_api.php`,
        csdoutbounddetails: `${HTTPADDR}/csdoutbound/put_outbound_call_comment_api.php`,
        collectiondetails: `${HTTPADDR}/collection/put_collection_call_comment_api.php`,
        salesdetails: `${HTTPADDR}/sales/put_sales_call_comment_api.php`,
        missedcalls: `${HTTPADDR}/csdinbound/put_inbound_call_comment_api.php`,
    },

    searchNumber: {
      csdinbounddetails:  `${HTTPADDR}/csdinbound/search_inbound_number_api.php`,
      csdoutbounddetails: `${HTTPADDR}/csdoutbound/search_outbound_number_api.php`,
      collectiondetails: `${HTTPADDR}/collection/search_collection_number_api.php`,
      salesdetails: `${HTTPADDR}/sales/search_sales_number_api.php`
    },
    login: `${HTTPADDR}/login.php`,

    getTags: `${HTTPADDR}/tag_manage.php`,
    createTag : `${HTTPADDR}/create_tag.php`,
    deleteTag: `${HTTPADDR}/delete_tag.php`,

    generateMetrics: `${HTTPADDR}/get_metrics.php`, 

    insertCustomerInfo: `${HTTPADDR}/insert_customer_info.php`,
    updateCustomerInfo: `${HTTPADDR}/update_customer_info.php` ,
    getcustomerregisteredcount: `${HTTPADDR}/getcustomertotalregistered.php`,
    searchcustomer : `${HTTPADDR}/search_customer.php`,
    deletecustomer: `${HTTPADDR}/delete_customer.php`,

}
export default API


