// import { defineAsyncComponent } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import CallsSummaries from './components/agentcdr/CallsSummaries.vue'
//import CallsDetails from './components/agentcdr/CallsDetails.vue'
import ActiveInactive from './components/agentcdr/csd/phoneAuth/ActiveInactive.vue'
//import AgentPhoneLogsDetails from './components/agentcdr/csd/phoneAuth/AgentPhoneLogsDetails.vue'
import MissedCallsSummies from './components/agentcdr/csd/MissedCallsSummaries.vue'
//import MissedCallsDetails from './components/agentcdr/csd/MissedCallsDetails.vue'
import ParkedCalls from './components/agentcdr/csd/ParkedCalls.vue'
import VoiceMails from './components/agentcdr/csd/VoiceMails'
// import ManagementMenu from './components/Management/ManagementMenu.vue'
//import ManageAgents from './components/Management/ManageAgents.vue'
//import ManageTags from './components/Management/ManageTags.vue'
//import GeneratedMetrics from './components/Management/GeneratedMetrics.vue'
// import TheMetrics from './components/Management/TheMetrics.vue'
import LoginToApp from './components/auth/LoginToApp.vue'

import store from './store/index.js'

//defined lazy loading 
// download only if needed
//good for production 
const AgentPhoneLogsDetails =  () => import('./components/agentcdr/csd/phoneAuth/AgentPhoneLogsDetails.vue')
const ManagementMenu = () => import('./components/Management/ManagementMenu.vue')
const ManageAgents = () => import('./components/Management/ManageAgents.vue')
const ManageTags = () => import('./components/Management/ManageTags.vue')
const TheMetrics = () => import('./components/Management/TheMetrics.vue')
const GeneratedMetrics = () => import('./components/Management/GeneratedMetrics.vue')
const CallsDetails = () => import('./components/agentcdr/CallsDetails.vue')
const MissedCallsDetails = () => import('./components/agentcdr/csd/MissedCallsDetails.vue')
const ManageCustomerInfo = () => import('./components/Management/ManageCustomerInfo.vue')

//const CoachDetail = () => import('./pages/coaches/CoachDetail.vue');

//study
import PlayGround from './components/PlayGround.vue'

const appName = store.getters.getAppName
const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    routes:[
        // {
        //     path: '/' , redirect: '/phone/loggedin',  meta:{requiredAuth: true}
        // },
        {
            path: `/${appName}/callsummaries/:calltype`, component: CallsSummaries, props:true, meta:{requiredAuth: true,allowedPosition:['1','2','3','99','10','20','21','22','30','31','40','41']}
        },
        {
            path: `/${appName}/calldetails/:calltype`, component: CallsDetails, props:true,  meta:{requiredAuth: true,allowedPosition:['1','2','3','99','10','20','21','22','30','31','40','41']}
        },
        {
            path: `/${appName}/phone/:phonestatus`, component: ActiveInactive,props: true,  meta:{requiredAuth:true ,allowedPosition:['99','20','21','22','30','31']}
        },
        {
            path: `/${appName}/agentphonelogsdetails`, component: AgentPhoneLogsDetails, props: true , meta:{requiredAuth: true,allowedPosition:['99','20','21','22','30','31']}
        },
        {
            path: `/${appName}/callsummaries/missedcalls`, component: MissedCallsSummies, props: true ,  meta:{requiredAuth: true,allowedPosition:['99','20','21','22','30','31']}
        },
        {
             path: `/${appName}/calldetails/missedcallsdetails`, component: MissedCallsDetails, props: true , meta:{requiredAuth: true, allowedPosition:['99','20','21','22','30','31']}
         },
        
        {
            path: `/${appName}/parkedcalls`, component: ParkedCalls ,  meta:{requiredAuth: true,allowedPosition:['99','20','21','22','30','31']}
        },
        {
            path: `/${appName}/voicemails`, component: VoiceMails ,  meta:{requiredAuth: true,allowedPosition:['99','20','21','22','30','31']}
        },
 
        {
            path: `/${appName}/management`, component: ManagementMenu , meta:{requiredAuth: true,allowedPosition:['99','10','20','22','30','40']} ,children:[
                { path: 'manage/:agent', component: ManageAgents , props : true , meta:{requiredAuth: true,allowedPosition:['99','10','20','22','30','40']}},
                { path: 'tags', component: ManageTags, props: true ,  meta:{requiredAuth: true, allowedPosition:['99','20','22','30','40']}},
                { path: 'metrics', component: TheMetrics, props: true ,  meta:{requiredAuth: true,allowedPosition:['99','20','22','30','40']}},
                { path: 'customerinfo', component: ManageCustomerInfo, props: true ,  meta:{requiredAuth: true,allowedPosition:['99','20','22','30','40']}}
            ]
        }, 
        
        {name:'generatedmetrics', path: `/${appName}/generatedmetrics/:sort_order/:option_metrics`, component: GeneratedMetrics, props: true ,  meta:{requiredAuth: true, allowedPosition:['99','10','20','22','10','30','40']}},

        { name:'loginpage', path:`/${appName}/login`, component: LoginToApp, props: true,  meta:{requiredNoAuth: true, }},
       
        {
            path: `/${appName}/searchnumber/:calltype`, component: CallsDetails, props:true, 
            
        },
        
        {path :`/${appName}/playground`, component: PlayGround}



    ]
    
})

router.beforeEach((to, _, next) => {
    if(to.path == `/${appName}/` && !store.getters.hasToken){
        next(`/${appName}/login`)
    }
    else if(to.meta.requiredAuth && !store.getters.hasToken){
        next(`/${appName}/login`)
    }else if (to.meta.requiredNoAuth && store.getters.hasToken){
        next(`/${appName}`)
    }else if(to.meta.requiredAuth && !to.meta.allowedPosition.includes(store.getters.getLoggedinUserData.position) && store.getters.hasToken){
        alert('You currently not Allowed to Access this resource..')  
        next(false)
    }else if((to.path == `/${appName}/callsummaries/csdinbound` ||
             to.path == `/${appName}/callsummaries/csdoutbound` || 
             to.path == `/${appName}/calldetails/csdinbounddetails` || 
             to.path == `/${appName}/calldetails/csdinbounddetails`) && store.getters.hasToken && 
             (['1','40','41'].includes(store.getters.getLoggedinUserData.position))){
       alert('You currently not Allowed to Access this resource..')           
       next(false)
    }else if((to.path == `/${appName}/callsummaries/collection` || 
             to.path == `/${appName}/calldetails/collectiondetails` ||
             to.path == `/${appName}/callsummaries/sales` || 
             to.path == `/${appName}/calldetails/salesdetails`) && store.getters.hasToken && 
             (['30','31'].includes(store.getters.getLoggedinUserData.position))){
        alert('You currently not Allowed to Access this resource..')           
        next(false)
    }else if((to.path == `/${appName}/callsummaries/csdinbound` ||
             to.path == `/${appName}/callsummaries/csdoutbound` || 
             to.path == `/${appName}/calldetails/csdinbounddetails` || 
             to.path == `/${appName}/calldetails/csdinbounddetails`) && store.getters.hasToken && 
             (['1','40','41'].includes(store.getters.getLoggedinUserData.position))){
       alert('You currently not Allowed to Access this resource..')            
       next(false)
    }else if((to.path == `/${appName}/callsummaries/csdinbound` ||
            to.path == `/${appName}/callsummaries/csdoutbound` || 
            to.path == `/${appName}/calldetails/csdinbounddetails` || 
            to.path == `/${appName}/calldetails/csdinbounddetails` ||
            to.path == `/${appName}/callsummaries/collection`  ||
            to.path == `/${appName}/calldetails/collectiondetails` ) && store.getters.hasToken && 
            (['1'].includes(store.getters.getLoggedinUserData.position))){
     alert('You currently not Allowed to Access this resource..')             
     next(false)
    }else if((to.path == `/${appName}/management/manage/csd` ||
            to.path == `/${appName}/management/manage/collection`) && store.getters.hasToken && 
            (['10'].includes(store.getters.getLoggedinUserData.position))){
     alert('You currently not Allowed to Access this resource..')           
     next(false)
    }else if((to.path == `/${appName}/management/manage/sales` || to.path.includes('sales') || to.path.includes('salesdetails')) && store.getters.hasToken &&
        (['20','30','40','2','22'].includes(store.getters.getLoggedinUserData.position))){
    alert('You currently not Allowed to Access this resource..')  
    next(false)        
    // }else if(store.getters.hasToken && store.getters.getLoggedinUserData.position == '0'){
    //  alert('You currently dont have any access to all resource.. Please your immediate superior')   
    //  next(false)
    }else if((to.path == `/${appName}/management/manage/csd` ||
         to.path == `/${appName}/management/manage/sales`) && store.getters.hasToken && 
       (['40'].includes(store.getters.getLoggedinUserData.position))){
         alert('You currently not Allowed to Access this resource..')           
        next(false)
    }
    else if((to.path == `/${appName}/management/manage/sales` ||
            to.path == `/${appName}/management/manage/collection`) && store.getters.hasToken && 
            (['30'].includes(store.getters.getLoggedinUserData.position))){
             alert('You currently not Allowed to Access this resource..')           
        next(false)
    }
    else if( store.getters.hasToken &&
         to.path == `/${appName}` && (
             store.getters.getLoggedinUserData.position == '99' ||
             store.getters.getLoggedinUserData.position == '20' ||
             store.getters.getLoggedinUserData.position == '21' ||
             store.getters.getLoggedinUserData.position == '22' ||
             store.getters.getLoggedinUserData.position == '30' ||
             store.getters.getLoggedinUserData.position == '31')){
        next(`/${appName}/phone/loggedin`)
    
    }else if(store.getters.hasToken &&
        to.path == `/${appName}/` && (
            store.getters.getLoggedinUserData.position == '40' ||
            store.getters.getLoggedinUserData.position == '41')){
      next(`/${appName}/callsummaries/collection`)       
    }else if( store.getters.hasToken &&
        to.path == `/${appName}` && (store.getters.getLoggedinUserData.position == '2' ||
        store.getters.getLoggedinUserData.position == '3' ||
        store.getters.getLoggedinUserData.position == '10'
        )){
       next(`/${appName}/callsummaries/csdinbound`)
   }else if(store.getters.hasToken && 
        to.path == `/${appName}` && store.getters.getLoggedinUserData.position == '1'){
      next(`/${appName}/callsummaries/sales`)

   }else if(store.getters.hasToken && (store.getters.getLoggedinUserData.position == '21' ||
    store.getters.getLoggedinUserData.position == '31' || 
    store.getters.getLoggedinUserData.position == '41'
   )&& ( to.query.extension && to.query.extension !== store.getters.getLoggedinUserData.extension)){
    alert('You currently not Allowed to Access this resource..') 
    next(false)
   }else {
     
       next()
   }

})

export default router