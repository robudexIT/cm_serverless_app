<template>
   
   <div class="nav-scroller bg-body shadow-sm">
     <super-admin-nav  v-if="loggedInUserPosition=='99' || loggedInUserPosition=='0'"  :mvpTotalCounts="mvpTotalCounts"></super-admin-nav >
     <hr-admin-nav v-else-if="loggedInUserPosition=='10'" :mvpTotalCounts="mvpTotalCounts"></hr-admin-nav>
     <csd-manager-nav v-else-if="loggedInUserPosition=='20'" :mvpTotalCounts="mvpTotalCounts"></csd-manager-nav>
     <csd-tl-nav v-else-if="loggedInUserPosition=='30'" :mvpTotalCounts="mvpTotalCounts"></csd-tl-nav>
     <collection-tl-nav  v-else-if="loggedInUserPosition=='40'"></collection-tl-nav>
     <csd-agent-nav v-else-if="loggedInUserPosition=='31'" :mvpTotalCounts="mvpTotalCounts"></csd-agent-nav>
     <collection-agent-nav v-else-if="loggedInUserPosition=='41'"></collection-agent-nav>
     <collection-csd-agent-nav v-else-if="loggedInUserPosition=='21'" :mvpTotalCounts="mvpTotalCounts"></collection-csd-agent-nav>
     <collection-csd-tl-nav v-else-if="loggedInUserPosition=='22'" :mvpTotalCounts="mvpTotalCounts"></collection-csd-tl-nav>
     <qc-sales-nav v-else-if ="loggedInUserPosition=='1'"></qc-sales-nav>
     <qc-csd-collection-nav v-else-if="loggedInUserPosition=='2'"></qc-csd-collection-nav>
     <qc-all-agents-nav v-else-if="loggedInUserPosition=='3'"></qc-all-agents-nav>

  </div>
 
</template>

<script>
 import SuperAdminNav from  './navoptions/SuperAdminNav.vue'
 import HrAdminNav from './navoptions/HrAdminNav.vue'
 import CsdManagerNav from './navoptions/CsdManagerNav.vue'
 import CsdTlNav from './navoptions/CsdTlNav.vue'
 import CollectionTlNav from './navoptions/CollectionTlNav.vue'
 import CollectionCsdTlNav from './navoptions/CollectionCsdTlNav.vue'
 import CsdAgentNav from './navoptions/CsdAgentNav.vue'
 import CollectionAgentNav from './navoptions/CollectionAgentNav.vue'
 import QcSalesNav from './navoptions/QcSalesNav.vue'
 import CollectionCsdAgentNav from './navoptions/CollectionCsdAgentNav.vue'
 import QcCsdCollectionNav from './navoptions/QcCsdCollectionNav.vue'
 import QcAllAgentsNav from './navoptions/QcAllAgentsNav.vue'

export default {
  components: {
     SuperAdminNav,
     HrAdminNav,
     CsdManagerNav,
     CsdTlNav,
     CollectionTlNav,
     CollectionCsdTlNav,
     CsdAgentNav,
     CollectionAgentNav,
     CollectionCsdAgentNav,
     QcSalesNav,
     QcAllAgentsNav,
     QcCsdCollectionNav,
  }, 
  data(){
    return {
      managementMenuActive: false
    }
  },
  methods:{
    gotoManagement(){
      this.managementMenuActive = true
    },
    gotoHome(){
      this.managementMenuActive = false
    },
    async fetchMvpTotalCounts(){
        this.$store.dispatch('agentcdr/fetchMvpTotalCounts')
    }
  },
  computed:{
    switchMenu(){
      return this.managementMenuActive ? 'HOME' : "MANAGEMENT"
    },
    mvpTotalCounts(){
      return this.$store.getters['agentcdr/getMpvTotalCounts']
    },
     loggedInUserPosition(){
        return this.$store.getters['getLoggedinUserData'].position
      }, 
    getAutoLogoutStatus(){
       return this.$store.getters['getAutoLogoutStatus']
    }
    

  },
  created(){
     this.$store.dispatch('checkIfCurrentLogin')
    this.fetchMvpTotalCounts()
  },
   watch:{
      getAutoLogoutStatus(currentstatus , oldstatus){
            if(currentstatus && currentstatus !== oldstatus){
            this.$router.replace('/login')
        }
      }
    }
}
</script>

<style scoped>
.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
  margin: 20px 5px;
}
</style>