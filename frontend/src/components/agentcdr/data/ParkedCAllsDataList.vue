<template>
   <tr v-for="(item, index) in tdata" :key="index">
        <td>{{index+1}}</td>
        <td>{{item.caller}}</td>
        <td>{{item.time}}</td>
        <td>{{item.getdate}}</td>
	
   </tr>
</template>


<script>
export default {
    props:['tdata'],
    
}
</script>