<template>
  <div>
    <base-dialog v-if="displaySpinner" :show="displaySpinner">
        <base-spinner>
           <h2>Logging Out</h2>
           <p>Clearing UserData and Token.. Please wait</p>
        </base-spinner>
  </base-dialog>
    <the-header v-if="loggedInUser && isAuthenticated" @logoutUser="logoutUser"></the-header>
    <the-navigation  v-if="loggedInUser && isAuthenticated" ></the-navigation>
     <router-view ></router-view>
      <!-- <router-view v-slot="slotProps">
        <transition name="fade-button" mode="out-in">
          <component :is="slotProps.Component"></component>
        </transition>
    </router-view> -->
     <!-- <play-ground></play-ground> -->
    <switch-agent-modal-form :belongsTo="belongsTo" ></switch-agent-modal-form>
  </div>
 
</template>

<script>

import TheHeader from './components/layout/TheHeader.vue'
import TheNavigation from './components/layout/TheNavigation.vue'
import SwitchAgentModalForm from  './components/layout/modal/SwitchAgentModalForm.vue'
// import PlayGround from './components/PlayGround.vue'
export default {
    components: {
      TheHeader,
      TheNavigation,
      SwitchAgentModalForm,
    },
    data(){
      return {
        isLogin: false,
        displaySpinner: false,
        appName: this.$store.getters.getAppName
      }
    },
    methods: {
      logoutUser(logout){
        if(logout){
          this.displaySpinner = true
          setTimeout(() => {
            this.$store.dispatch('logoutUser')
            this.$router.replace('/'+this.appName+'/login')
            this.displaySpinner = false
          }, 10000);
          
        }else{
          return
        }
        
      },
      
    },
    computed: {
      loggedInUser(){
        return this.$store.getters['getLoggedinUserData']
      },
      isAuthenticated(){
        return this.$store.getters['hasToken']
      },
      getAutoLogoutStatus(){
        return this.$store.getters['getAutoLogoutStatus']
      },
       belongsTo(){
       return this.$store.getters['agentinfo/getAgentBelongsTo']
     }
    },
    beforeCreate(){
      document.body.className = 'home';
    },
    created(){
      this.$store.dispatch('checkIfCurrentLogin')
    },
    mounted(){
      const scripts = [
            "js/xlsx.core.min.js",
            "js/jhxlsx.js",
            "js/FileSaver.js"
        ];
        scripts.forEach(script => {
            let tag = document.head.querySelector(`[src="${ script }"`);
            if (!tag) {
                tag = document.createElement("script");
                tag.setAttribute("src", script);
                tag.setAttribute("type", 'text/javascript');
                document.head.appendChild(tag); 
            }
        });
    },
    watch:{
      getAutoLogoutStatus(currentstatus , oldstatus){
        if(currentstatus && currentstatus !== oldstatus){
          this.$router.replace('/'+this.appName+'/login')
        }
      }
    }
    
}
</script>

<style >
html{
  overflow-x: hidden; /* Prevent scroll on narrow devices */
}

body.home {
  padding-top: 56px;
  overflow-x: hidden; /* Prevent scroll on narrow devices */
  
}
body.login {
    margin: 0;
    padding: 0;
    background: url('./images/images.jpg')  ;
    background-size: cover;
    background-position: center;
    font-family: Arial, Helvetica, sans-serif;
}

.fade-button-enter-from,
.fade-button-leave-to {
  opacity: 0;
}

.fade-button-enter-active {
  transition: opacity 1s ease-out;
}

.fade-button-leave-active {
  transition: opacity 1s ease-in;
}

.fade-button-enter-to,
.fade-button-leave-from {
  opacity: 1;
}


</style>