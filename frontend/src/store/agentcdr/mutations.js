export default {
    mutCallsSummaries(state, payload){
        if(payload.calltype === 'csdinbound'){
            state.csdInBoundSummaries = payload.data
        }else if(payload.calltype === 'csdoutbound'){
            state.csdOutBoundSummaries = payload.data
        }else if(payload.calltype === 'collection'){
            state.collectionOutBoundSummaries = payload.data
        }else if(payload.calltype == 'sales'){
            state.salesOutBoundSummaries = payload.data
        }
        state.summariesExportData = payload.summariesExportObject
    },
    mutCallsDetails(state,payload){
        if(payload.calltype === 'csdinbounddetails'){
            state.csdInBoundAgentDetails = payload.data
        }else if( payload.calltype === 'csdoutbounddetails'){
            state.csdOutBoundAgentDetails = payload.data
        }else if(payload.calltype === 'collectiondetails'){
            state.collectionOutBoundAgentDetails = payload.data
        }else if(payload.calltype === 'salesdetails'){
           state.salesOutBoundAgentDetails = payload.data
        }
        
        state.detailsExportData = payload.detailsExportObject
    },
    mutMissedCallsSummaries(state, payload){
        state.missedCallsSummaries = payload
    },
    mutMissedCallsDetails(state, payload){
        state.missedCallsDetails = payload.data
        state.missedCallsDetailsExport = payload.missedcallsExportObject
    },
    //just for fun
    mutCommentTag(state, payload){
        const updateTagComment = (currentCallDetailsState) => {
            const updatedCallDetailsState  = currentCallDetailsState[0].map(agentCallDetails =>
               agentCallDetails.extension === payload.data.whoansweredcall
               && agentCallDetails.starttimestamp === payload.data.starttimestamp
               && agentCallDetails.getDate === payload.data.getdate ?
               {...agentCallDetails, comment: payload.data.comment, tag:payload.data.tag} : agentCallDetails
            ) 
           currentCallDetailsState[0] = updatedCallDetailsState
       }
        if(payload.calltype == 'missedcalls'){
            const missedCallsDetails = state.missedCallsDetails.map(missedcall => 
               missedcall.extension === payload.data.whoansweredcall 
               && missedcall.starttimestamp === payload.data.starttimestamp 
               && missedcall.getDate === payload.data.getdate ? {...missedcall,  comment: payload.data.comment, commentby: payload.data.commentby}
               : missedcall
            )
           
            state.missedCallsDetails = missedCallsDetails
        }else if(payload.calltype == 'csdinbounddetails'){
            updateTagComment(state.csdInBoundAgentDetails)
            
        }
        else if(payload.calltype == 'csdoutbounddetails'){
          
            updateTagComment(state.csdOutBoundAgentDetails)
        }
        
       else if(payload.calltype == 'collectiondetails'){
           updateTagComment(state.collectionOutBoundAgentDetails)
       
       }
       else if(payload.calltype == 'salesdetails'){
           updateTagComment(state.salesOutBoundAgentDetails)
      
      }

      
    },   
    mutMpvTotalCounts(state, payload){
        state.mpvTotalCounts = payload
    },
    mutVoiceMails(state, payload){
        state.voiceMails = payload
    },
    mutParkedCalls(state, payload){
        state.parkedCalls = payload
    },
    mutResultSearchNumber(state, payload){
        state.resultSearchNUmber = payload
    }   
}