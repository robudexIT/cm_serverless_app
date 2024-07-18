<template>
   <tr v-for="(item, index) in tdata" :key="index">
        <td>{{index+1}}</td>
        <td>{{item.caller}}</td>
        <td>{{item.date}}</td>
        <td>{{item.time}}</td>
        <td>{{item.voicemail}}</td>
		<td>
            <button class="btn btn-danger btn-sm font-weight-normal lead" @click="deleteVoiceMail(item.timestamp)"  >DELETE</button>
		</td>
     </tr>
</template>


<script>
export default {
    props:['tdata'],
    methods: {
        deleteVoiceMail(timestamp){
            this.$emit('emittedData', timestamp)
        }
    }
}
</script>