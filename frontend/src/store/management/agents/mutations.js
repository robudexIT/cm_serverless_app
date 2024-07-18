export default {
    mutAgents(state, payload){
      if(payload.agent == 'csd'){
          state.csdAgents = payload.data
      }else if(payload.agent == 'collection'){
        state.collectionAgents = payload.data
      }else if(payload.agent == 'sales'){
          state.salesAgents = payload.data
      }
    },
    mutAgentBelongsTo(state, payload){
      state.agentBelongsTo = payload
    }

  //   mutSingleAgent(state, payload){
  //  //   console.log(payload.extension)
     
  //     const updateAgentState = (method, currentAgentList) => {
  //     console.log(currentAgentList)  
  //     let newAgentList
      
  //     if(method == 'delete'){
  //       newAgentList = currentAgentList.filter(agent => agent.extension !== payload.extension)
            
  //     }else if(method == 'update'){
  //       newAgentList = currentAgentList.map(agent => agent.extension === payload.extension ? {...agent, name:payload.name, email:payload.email} : agent )
        
  //     }
  //     currentAgentList = []
  //     //currentAgentList = [...newAgentList]
        
  //     }

  //     if(payload.agent == 'csd'){
  //       updateAgentState(payload.method, state.csdAgents)
  //     // }else if (payload.agent == 'collection'){
  //     //   updateAgentState(payload.method,  state.collectionAgents)
  //     // }else if(payload.agent == 'sales'){
  //     //   updateAgentState(payload.method, state.salesAgents)

  //      }
      
  //   }
    
}