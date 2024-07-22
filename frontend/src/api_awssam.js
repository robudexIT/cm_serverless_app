

const HTTPADDR = "https://zmvk3tmbxe.execute-api.us-east-1.amazonaws.com/Prod/api"

const API = {
   login: `${HTTPADDR}/login`,

   getCallSummaries: {
    csdinbound:  `${HTTPADDR}/callsummaries/csdinbound`,
    csdoutbound: `${HTTPADDR}/callsummaries/csdoutbound`,
    collection: `${HTTPADDR}/callsummaries/collection`,
    sales: `${HTTPADDR}/callsummaries/sales`,
    missecalls: `${HTTPADDR}/callsummaries/missedcalls`
   },
  getCallDetails: {
    csdinbounddetails: `${HTTPADDR}/calldetails/csdinbounddetails`,
    csdoutbounddetails: `${HTTPADDR}/calldetails/csdoutbounddetails`,
    collectiondetails: `${HTTPADDR}/calldetails/csdinbounddetails`,
    salesdetails: `${HTTPADDR}/calldetails/csdoutbounddetails`,
    missedcallsdetails:`${HTTPADDR}/calldetails/missedcallsdetails`,
   },

   searchNumber: {
    csdinbounddetails:  `${HTTPADDR}/searchnumber/csdinbounddetails`,
    csdoutbounddetails: `${HTTPADDR}/searchnumber/csdoutbounddetails`,
    collectiondetails: `${HTTPADDR}/searchnumber/collectiondetails`,
    salesdetails: `${HTTPADDR}/searchnumber/salesdetails`,
    customerdetails: `${HTTPADDR}/searchnumber/customer`
  },
   
  agents: {
    agent: `${HTTPADDR}/agents`,
    // collection: `${HTTPADDR}/agents/collection`,
    // sales:`${HTTPADDR}/agents/sales`, 
    phoneLoggedIn: `${HTTPADDR}/agents/csd/inbound_group?group=active`,
    phoneLogggedOut: `${HTTPADDR}/agents/csd/inbound_group?group=inactive`, 
    phoneLogsDetails : `${HTTPADDR}/agents/csd/agentphonelogsdetails`,  
  },

  getcounts: `${HTTPADDR}/getcounts`,

tags: `${HTTPADDR}/tags`,
  
generateMetrics: `${HTTPADDR}/getmetrics`, 

insertCustomerInfo: `${HTTPADDR}/cdr/customer?querytype=insert`,
updateCustomerInfo: `${HTTPADDR}/cdr/customer?querytype=update` ,
deletecustomer: `${HTTPADDR}/cdr/customer?querytype=delete` ,
getcustomerregisteredcount: `${HTTPADDR}/getcounts/customer` ,

commentTag: {
  csdinbounddetails: `${HTTPADDR}/cdr/csdinbound`,
  csdoutbounddetails: `${HTTPADDR}/cdr/csdoutbound`,
  collectiondetails: `${HTTPADDR}/cdr/collection`,
  salesdetails: `${HTTPADDR}/cdr/sales`,
  missedcalls: `${HTTPADDR}/cdr/missecalls`,
},


}


export default API


// const HTTPADDR = `${process.env.VUE_APP_API_ENDPOINT}/api`    //'https://z5hj7lt6bd.execute-api.us-east-1.amazonaws.com/Prod/api'
// const  HTTPADDR = 'https://z5hj7lt6bd.execute-api.us-east-1.amazonaws.com/Prod/api'

// const  HTTPADDR = 'http://167.71.22.129:3000/api' //process.env.VUE_APP_HTTPADDR_AWSSAM