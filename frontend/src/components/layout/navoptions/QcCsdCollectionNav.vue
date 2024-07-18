<template>
    <nav class="nav nav-underline" aria-label="Secondary navigation">
        <router-link class="nav-link mx-0 px-2" :to="'/'+appName+'/callsummaries/csdinbound'">CSD-INBOUND</router-link>
        <router-link class="nav-link mx-0 px-2" :to="'/'+appName+'/callsummaries/csdoutbound'">CSD-OUTBOUND</router-link>
        <router-link class="nav-link mx-0 px-2" :to="'/'+appName+'/callsummaries/collection'">COLLECTION-TEAM</router-link>
      
    </nav>
</template>

<script>
export default {
  data() {
    return {
      appName: this.$store.getters.getAppName
    }
  },
}
</script>

<style  scoped>
.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
  margin: 300px 5px;
}

.nav-underline .nav-link:hover  {
  background-color: grey;
  border-radius:25px;
   border: 2px solid grey;
  color: white;
}

.nav-link {
  color: grey;
  font-size: 15px;
  /* transition: background-color 2s, height 2s, width 2s; */
}
a.router-link-active {
     background-color: #007bff;
     color: white;
     border-radius:25px;
     border: 2px solid blue;
     font-weight: bold;
}
span {
  font-weight: bold;
  color : black;
  font-size: 15px;
}
</style>