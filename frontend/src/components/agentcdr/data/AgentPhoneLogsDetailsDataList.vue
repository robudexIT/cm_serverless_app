<template>
     <tr v-for="(item, index) in tdata" :key="index">
       <td>{{index+trimStart+1}}</td>
       <td>{{item.log}}</td>
       <td>{{item.date}}</td>
       <td>{{item.time}}</td>
     </tr>
</template>

<script>
    export default {
       props: {
        trimStart: {
            type:Number,
            required:false
        },
        tdata: {
          type:Array,
          required: false,
        }
    },

    }
    
    
</script>


