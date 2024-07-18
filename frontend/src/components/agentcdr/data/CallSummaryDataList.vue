<template>
     <tr v-for="(item, index) in tdata" :key="index">
       <td>{{index+1}}</td>
       <td>{{item.extension}}</td>
       <td>{{item.name}}</td>
       <td v-if="item.teamlead">{{item.teamlead}}</td>
       <td>{{item.total_counts}}</td>
       <td>{{item.total_duration}}</td>
       <td><router-link :to="appName+item.link_details">{{item.getdate}}</router-link></td>
     </tr>
</template>

<script>
    export default {
        props:['tdata','tags'],
        data() {
          return {
            appName: '/'+ this.$store.getters.getAppName  + '/'
          }
        }
     
    }
    
</script>
