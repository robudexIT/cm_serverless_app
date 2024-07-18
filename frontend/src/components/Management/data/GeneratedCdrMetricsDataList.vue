<template>
       <tr v-for="(item, index) in tdata" :key="index">
         <td>{{index+1}}</td>
         <td>{{item.name}}</td>
         <td>{{item.extension}}</td>
         <td v-if="optiondata.callcount_weight != 0">{{item.total_counts}}</td>
         <td v-if="optiondata.duration_weight != 0">{{item.total_duration}}</td>
         <td v-if="optiondata.callcount_weight != 0">{{item.c_percentage}}%</td>
         <td v-if="optiondata.duration_weight != 0">{{item.d_percentage}}%</td>
         <td>{{item.total_percentage}}%</td>
       </tr>
</template>

<script>

export default {
    props:['tdata','optiondata'],
   
}
</script>