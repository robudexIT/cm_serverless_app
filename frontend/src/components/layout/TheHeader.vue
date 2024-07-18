<template>
 
  <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark " aria-label="Main navigation">
  <div class="container-fluid ">
    <router-link class="navbar-brand" to="/">{{displayAppTitle}}</router-link>

    <button class="navbar-toggler p-0 border-0" type="button" id="navbarSideCollapse" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">

       <li v-if="blendedCalltype"><button type="button" class="btn btn-primary"  data-bs-toggle="modal" data-bs-target="#switchAgent" dataset-backdrop="static" dataset-keyboard="false" > {{belongsTo}} <font-awesome-icon :icon="myPhone" /></button></li>
     
      </ul>
      <form class="d-flex" @submit.prevent="logoutUser">
        <p class="currentUserName">{{loggedInUserName}}</p>
        <button class="btn btn-outline-success logout" type="submit">Logout</button>

      </form>
      
    
    </div>
  </div>
</nav>

</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPhoneVolume } from '@fortawesome/free-solid-svg-icons'

export default {
  components: {
    FontAwesomeIcon,

  },
  data(){
    return {
      displaySpinner: true,
      myPhone : faPhoneVolume,
      error: null
    }
  },
  computed: {
     loggedInUserName(){
        return this.$store.getters['getLoggedinUserData'].name
      },
     displayAppTitle(){
      let position = this.$store.getters['getLoggedinUserData'].position
      if(position == '1' || position == '2' || position == '3'){
        return 'QC MONITORING APPS'
      }else if(position == '10'){
        return 'HR MONITORING APPS'
      }else if(position == '99'){
        return 'IT/SYSADMIN APPS'
      }else {
        return 'CSD/COLLECTION APPS'
      }
     },
     blendedCalltype(){
       //return 1 if user/agent are belong to CSD and Collection
       //return 0 if user/agent is only belong to CSD or Collection
       let blended = this.$store.getters['getLoggedinUserData'].blended
       let position = this.$store.getters['getLoggedinUserData'].position

       return blended === '1'  && (position == '21' || position == '22' || position == '99' || position == '20') ? true : false
     },
     belongsTo(){
       return this.$store.getters['agentinfo/getAgentBelongsTo']
     }
  },
  methods: {
    logoutUser(){
      const logout = confirm('Are you you want to logout?')
      if (logout){
         this.$emit('logoutUser', logout)
      }else{
        return
      }
     
      
    },
    async fetchAgentBelongsTo(){
       try {
         this.$store.dispatch('agentinfo/fetchAgentBelongsTo')
       }catch(e){
         this.error = e.message
       }
    }
  },
  created(){
    this.fetchAgentBelongsTo()
  }
}
</script>

<style scoped>
  .currentUserName {
    color:grey;
    font-weight: bold;
    font-size: 20px;
    /* border: 1px solid yellow; */
    padding-top: 8px;
    padding-right: 5px;
    margin-right: 10px;
  }
  .logout {
    height: 40px;
     margin-top: 0px;
  
  }
  
</style>