<template>
     <tr v-for="(item, index) in tdata" :key="index">
       <td >{{index+1}}</td>
       <td :style="tagNameStyle(item.tagtype)" >{{item.tagtype}}</td>
       <td >{{item.tagname}}</td>
       <td >{{item.createdby}}</td>
       <td >{{item.createddate}}</td>
        <td>
            <button class="btn btn-danger btn-sm font-weight-normal lead" :id="item.tagId" @click="deleteTag(item.tagId)">DELETE</button>
        </td>
     </tr>
     
</template>

<script>
    export default {
        props:['tdata'],
        methods:{       
            tagNameStyle(tagtype){
                let tagnameColor
                if(tagtype== 'CSDINBOUND'){
                    tagnameColor = 'green'
                }else if(tagtype =='CSDOUTBOUND'){
                    tagnameColor = 'blue'
                }else if(tagtype == 'COLLECTION'){
                    tagnameColor = 'purple'
                }else {
                    tagnameColor = 'purple'
                }  
                return { color: tagnameColor, fontWeight : 700 }
            },
            deleteTag(tagId){
                this.$emit('click', tagId)
            }
        }
     
    }
    
</script>