// import API from '../../api.js'

import API from '../../api_awssam.js'
import store from '../index.js'
export default {
    async fetchCallsSummaries(context,payload){
        const token = store.getters.getJwtToken
      
        if (token == null) {
          store.dispatch('autLogout')
          return
        }
        console.log(token)
        const calltype = payload.calltype
        const response = await fetch(`${API.getCallSummaries[calltype]}?${payload.querystring}`,{
           method: 'GET',
           headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           }
        })
        
        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
        }

        if(!response.ok){
            const error = new Error('Error in fetch Calls Summary')
            throw error
        }
       
        const data = await response.json()
        

        const extension = context.rootGetters.getLoggedinUserData.extension
        const position  = context.rootGetters.getLoggedinUserData.position
        
        if(position == '21' || position == '31' || position == '41'){
          data[0] = data[0].filter(d => d.extension === extension)
        }
       
        payload.data = data
        
       //excel export settings 
       const summariesExportObject = {
            "options": {
              "fileName": ""
            },
            "tableData": [
              {
                "sheetName": "Sheet1",
                "data": [
                  [ 
                    {
                      "text": "EXTENSION"
                    },
                    {
                      "text": "NAME"
                    },
                    {
                      "text": "TOTAL CALLS DURATION (HH:MM:SS)"
                    },
                    {
                      "text": "DATE"
                    }
                   
                  ]
                  
                ]
              }
            ]
          }
          //insert element between NAME and TOTAL CALLS DURATION (HH:MM:SS)
          let insertHeading
          if(calltype== 'csdinbound' ){
               insertHeading =  {text: "TOTAL CALL ANSWERED" }
              
          }else{
            insertHeading = { text: "TOTAL MADE CALLS" }
          }
          summariesExportObject.tableData[0].data[0].splice(1,0,insertHeading)

          
          for (const agent of data[0]){    
             let arraySummies = []
             arraySummies.push({text: agent.extension})
             arraySummies.push({text: agent.name})
             arraySummies.push({text: agent.total_counts})
             arraySummies.push({text: agent.total_duration})
             arraySummies.push({text: agent.getdate})
             summariesExportObject.tableData[0].data.push(arraySummies)
          }
         summariesExportObject.options.fileName = `${calltype}-${data[0].getdate}-summary`
         
         payload.summariesExportObject = summariesExportObject

        context.commit('mutCallsSummaries', payload)

    },
    async fetchCallsDetails(context,payload){
        const calltype = payload.calltype
        const token = store.getters.getJwtToken
        const response = await fetch(`${API.getCallDetails[calltype]}?${payload.querystring}`,{
          method: 'GET',
          headers:{
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${token}`,
       
          }
        })
         //if no token or token is expire logout the apps..
         if (response.status === 403){
          store.dispatch('autoLogout')
        }    

        if(!response.ok){
          
            const error = new Error('Error in fetching Calls Details.Please Try again')
            throw error
        }

        const data = await response.json()
       
        if(!Array.isArray(data) || data.length == 0 || data.message){
          const error = new Error('Result Not Found ')
          
          payload.data = []
          context.commit('mutCallsDetails', payload)
          throw error 
        }else{
          payload.data = data
        }
        
  
        //excel export settings
        const detailsExportObject = {
            "options": {
              "fileName": ""
            },
            "tableData": [
              {
                "sheetName": "Sheet1",
                "data": [
                  [ {
                      "text" : "NAME"
                    },
                    {
                      "text": "EXTENSION"
                    },
                    {
                      "text": "CALLEDNUMBER"
                    },
                    {
                      "text": "CALLER"
                    },
                    {
                      "text": "CALLSTATUS"
                    },
                    {
                      "text": "STARTTIME"
                    },
                    {
                      "text": "ENDTIME"
                    },
                    {
                      "text": "CALLDURATION"
                    },
                    {
                      "text": "CALL-RECORDINGS"
                    },
                    {
                      "text": "DATE"
                    },
                    {
                      "text": "COMMENT"
                    },
                    {
                      "text" : "TAG"
                    }
                   
                  ]
                  
                ]
              }
            ]
          }

          for (const agent of data[0]){
            let agentarray = [];
            agentarray.push({text: agent.name})
            agentarray.push({text: agent.extension})
            agentarray.push({text: agent.calledNumber})
            agentarray.push({text: agent.caller})
            agentarray.push({text: agent.callStatus})
            agentarray.push({text: agent.startime})
            agentarray.push({text: agent.endtime})
            agentarray.push({text: agent.callDuration})
            agentarray.push({text: agent.callrecording})
            agentarray.push({text: agent.getDate })
            agentarray.push({text: agent.comment})
            agentarray.push({text: agent.tag })
            detailsExportObject.tableData[0].data.push(agentarray)
          }
          detailsExportObject.options.fileName = `${data[0][0].name}-(${data[0][0].daterange})-calldetails`
          payload.detailsExportObject = detailsExportObject
        
        context.commit('mutCallsDetails', payload)
    }, 
    async fetchMissedCallsSummaries(context,payload){
       // console.log(payload.querystring)
       const token = store.getters.getJwtToken
       console.log(`${API.getCallSummaries.missecalls}`)
        const response = await fetch(`${API.getCallSummaries.missecalls}?${payload.querystring}`,{
          method: 'GET',
          headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           }
        })
          //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }      
        if(!response.ok){
            const error = new Error('Cannot Fetcch Summaries of MissedCalls')
            throw error
        }else{
            const data = await response.json()
            
            if(data.length == 0 || !Array.isArray(data)){
              const error = new Error('No MissedCalls')
              context.commit('mutMissedCallsSummaries',[])
              throw error
            }
            // tranform misscalls_details fields from
            // "misscalls_details": "csd_missed_calls_details.php?startdate=2021-09-01&enddate=2021-09-10"
            // to "misscalls_details": "/missedcallsdetails?startdate=2021-09-01&enddate=2021-09-10"
          
            // const transformdata = data.map(d => {
            //     const getquery = d.misscalls_details.split('?')[1]
            //     d.misscalls_details = `missedcallsdetails?${getquery}`
            //     return d
            // })
            context.commit('mutMissedCallsSummaries',data)
        }
    },
    async fetchMissedCallsDetails(context, payload){
      console.log('It is not empty...')
      const token = store.getters.getJwtToken
      console.log(`${API.getCallDetails.missedcallsdetails}`)
      const response = await fetch(`${API.getCallDetails.missedcallsdetails}?${payload.querystring}`,{
        method: 'GET',     
        headers:{
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    
       }
    })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
     
        }    
        if(!response.ok){
         
            const error = new Error('Cannot Fetch MisseCalls Details')
            throw error
        }

        else{

          const data = await response.json()
          console.log(data)
          if(data.length == 0 || !Array.isArray(data)){
           
            const error = new Error('No MissedCalls')
            const errorData = {}
            errorData.data = []
            errorData.missedcallsExportObject = {}
            context.commit('mutMissedCallsDetails',errorData)
            
            throw error
          }
           
            const missedcallsExportObject = {
              "options": {
                "fileName": "missed_call_details"
              },
              "tableData": [
                {
                  "sheetName": "Sheet1",
                  "data": [
                    [ 
                      {
                        "text": "StartTime"
                      },
                      {
                        "text": "EndTime"
                      },
                      {
                        "text": "Caller"
                      },
                      {
                        "text": "CallStatus"
                      },
                      {
                        "text": "Comment"
                      },
                      {
                        "text": "CommentBy"
                      },
                      {
                        "text": "Date"
                      }
                     
                    ]
                    
                  ]
                }
              ]
            }
            for(let missedcall of data){
              let missedCallsArray = []
              missedCallsArray.push({text:missedcall.startime})
              missedCallsArray.push({text:missedcall.endtime})
              missedCallsArray.push({text:missedcall.caller})
              missedCallsArray.push({text:missedcall.callStatus})
              missedCallsArray.push({text:missedcall.comment})
              missedCallsArray.push({text:missedcall.commentby})
              missedCallsArray.push({text: missedcall.getDate})
              missedcallsExportObject.tableData[0].data.push(missedCallsArray)

            }
            //startdate=2021-08-01&enddate=2021-08-23&tagname=all&option=summary
            let startdate = payload.querystring.split('&')[0].split('=')[1]
            let enddate = payload.querystring.split('&')[1].split('=')[1]

            let dateRange; 
            if(startdate === enddate){
              dateRange = startdate
            }else{
              dateRange = startdate + '-' + enddate
            }
            missedcallsExportObject.options.fileName = `(${dateRange})-csd-missedcalls-details`

            payload.missedcallsExportObject = missedcallsExportObject
            payload.data = data
            context.commit('mutMissedCallsDetails', payload)
        }
    },
    async putCommentTag(context, payload){
        const calltype = payload.calltype
        const token = store.getters.getJwtToken

        const response = await fetch(API.commentTag[calltype], {
            method: 'POST', 
            headers:{
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
          
             },
            body: JSON.stringify(payload.data)
        })

        //if no token or token is expire logout the apps..
        if (response.status === 403){
          store.dispatch('autoLogout')
        }  

        if(!response.ok){
            const error = new Error('Cannot Put or update comment or tag')
            throw error
        }else{
            context.dispatch('fetchtUpdatedTagComment',payload)
        }
    }, 
    async fetchtUpdatedTagComment(context, payload){
       const token = store.getters.getJwtToken
        //getInboundCallComment($extension,$getdate,$starttimestamp
        const starttimestamp = payload.data.starttimestamp
        const getdate = payload.data.getdate
        const extension = payload.data.whoansweredcall
        const calltype = payload.calltype
        
        const newQueryString =`extension=${extension}&getdate=${getdate}&starttimestamp=${starttimestamp}`
      
        const response = await fetch(`${API.commentTag[calltype]}?${newQueryString}`,{
          headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           },
           method: 'GET'
        })
        //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
        }

        if(!response.ok){
            const error = new Error('Cannot get updated comment or tag')
            throw error
        }else{
         
            const data = await response.json()
            payload.data.comment = data.comment
            payload.data.tag = data.tag
            payload.data.commentby = data.commentby
            context.commit('mutCommentTag', payload)
        }

    },
    async fetchTotalCounts(context){
       const response = await fetch(API.mpvTotalCounts)
      //if no token or token is expire logout the apps..
        if (response.status === 403){
            store.dispatch('autoLogout')
       }
       if(!response.ok){
         const error = new Error('Cannot Fetch')
         throw error
       }
       const data = await response.json()
       context.commit('mutTotalCounts', data)
       

    },
    async fetchVoiceMails(context){
      const response = await fetch(API.getVoiceMails)
  
         //if no token or token is expire logout the apps..
      if (response.status === 403){
          store.dispatch('autoLogout')
      }     
       if(!response.ok){
          const error = new Error('Cannot Fetch VoiceMails')
          throw error

       }
       const data = await response.json()
       if(!Array.isArray(data) || data.length == 0 || data.message){
         const error = new Error('Result not found')
         context.commit('mutVoiceMails',[])
         throw error
       }else{
         context.commit('mutVoiceMails',data)
       }

    },
    async deleteVoiceMails(context, payload){
     
      const timestamp = payload.timestamp
  
      const response = await fetch(`${API.deleteVoiceMails}?timestamp=${timestamp}`)
   
        //if no token or token is expire logout the apps..
       if (response.status === 403){
          store.dispatch('autoLogout')
      }      
      if(!response.ok){
        const error = new Error('Cannot be delete')
        throw error
      }
      // const data = await response.json()
     

      context.dispatch('fetchVoiceMails')


    },
    async fetchParkedCalls(context){
      const response = await fetch(API.getParkedCalls)

        //if no token or token is expire logout the apps..
      if (response.status === 403){
          store.dispatch('autoLogout')
      }      
      if(!response.ok){
        const error = new Error('Cannot fetch ParkedCalls')
        throw error
      }
      const data = await response.json()
      
      if(!Array(data) || data.length == 0 || data.message){
        const error = new Error('Result not found')
        context.commit('mutParkedCalls', [])
        throw error
      }else{
        context.commit('mutParkedCalls', data)
      }
    },
    
    async fetchSearchedNumber(context,payload){
      const querystring = payload.querystring
      const calltype = payload.calltype
      const token = store.getters.getJwtToken
      const response = await fetch(`${API.searchNumber[calltype]}?${querystring}`,{
        headers:{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
      
         },
         method: 'GET'
      })

        //if no token or token is expire logout the apps..
      if (response.status === 403){
          store.dispatch('autoLogout')
      }  

      if(!response.ok){
        const error = new Error('No Number Found')
        throw error
      }
      const data = await response.json()

     
      if(!Array.isArray(data) || data.length == 0 || data.message){
        const error = new Error('Result Not Found ')
       
        payload.data = []
        context.commit('mutCallsDetails', payload)
        throw error 
      }else{
        payload.data = data
      }
    
      context.commit('mutCallsDetails',payload)
    },

    async insertCustomerInfo(context, payload){
      const token = store.getters.getJwtToken
      console.log(payload)
      const response = await fetch(API.insertCustomerInfo, {
          method: 'POST', 
          body: JSON.stringify(payload),
          headers:{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        
           },
      })

        //if no token or token is expire logout the apps..
      if (response.status === 403){
          store.dispatch('autoLogout')
      }      
      if(!response.ok){
          const error = new Error('Cannot Insert Customer Info')
          throw error
      }else{
          // context.dispatch('fetchtUpdatedTagComment',payload)
          console.log("New Customer Info Added")
      }
  },

  async  updateCustomerInfo(context, payload){
    const token = store.getters.getJwtToken   
    console.log(payload)
    const response = await fetch(API.updateCustomerInfo, {
        method: 'POST', 
        body: JSON.stringify(payload),
        headers:{
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
      
         },
    })

        //if no token or token is expire logout the apps..
     if (response.status === 403){
          store.dispatch('autoLogout')
      }

    if(!response.ok){
        const error = new Error('Cannot Update Customer Info')
        throw error
    }else{
        // context.dispatch('fetchtUpdatedTagComment',payload)
        console.log("New Customer Info Updated")
    }
},
  
 
      
}