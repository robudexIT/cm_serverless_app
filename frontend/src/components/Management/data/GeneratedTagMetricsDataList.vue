<template>
       <tr v-for="(data, index) in tdata" :key="index">
          <td v-for="(item, i) in data" :key="i">{{item}}</td>
          <td>{{getTotal(data)}}</td>
       </tr>
</template>


<script>

export default {
    props:['tdata'],
    methods:{
        getTotal(data){
            let total = data.filter(el => {
                if(typeof el === 'number'){
                    return el
                }
            }).reduce((subtotal ,nextVal) => {
                return subtotal + nextVal
            },0)
            return total
        }
    }
}
</script>