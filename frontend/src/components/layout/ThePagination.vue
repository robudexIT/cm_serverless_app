<template>
    <base-container>
    <div class="row justify-content-center">
        <!-- <button v-for="page in numberOfPages" :key="page" @click="getCurrentPage" :id="page">{{page}}</button> -->
        <div class="col-4 "></div>
        <div v-if="numberOfPages==2" class="col-4 mb-3">
            <button @click="getCurrentPage" id="1" :class="{activebtn:activePage}">1</button>
            <button @click="getCurrentPage" id="2" :class="{activebtn:!activePage}">2</button>
        </div>
        <div v-else class="col-4 align-self-center mb-3 ">
            <button :disabled="disabledPrevBtn" @click="prevbtn" class="btn btn-outline-primary me-1"> &lt;&lt;prev({{currentPage-1}}) </button>
            <button @click="getCurrentPage" :id="currentPage" class="btn btn-success ">{{currentPage}}</button>
            <button :disabled="disabledNextBtn" @click="nextbtn" class="btn btn-outline-primary ms-1">next ({{currentPage+1}})&gt;&gt;</button>
        </div>
         <div class="col-4  "></div>
    </div>
    </base-container>
</template>

<script>
import BaseContainer from './BaseContainer.vue'
export default {
  components: { BaseContainer },
    props:['numberOfPages'],
    data(){
        return {
            numberPerPage: 5,
            currentPage: 1,
            activePage: true
        }
    },
    methods: {
        getCurrentPage(event) {
        this.activePage = !this.activePage
        this.$emit('emittedData',  event.target.id)
      },
      nextbtn(){
          this.currentPage++
          this.$emit('emittedData',  this.currentPage)
      }, 
      prevbtn(){
          this.currentPage--
          this.$emit('emittedData',  this.currentPage)
      }  
    },
    computed: {
        disabledPrevBtn(){
           return this.currentPage == 1 ? 'disabled' : 0
        },
        disabledNextBtn(){
            return this.currentPage >= parseInt(this.numberOfPages) ? 'disabled' : 0
        }
    }
    
}
</script>

<style scoped>
    .activebtn {
        color: white;
        background-color:blue;
        font-weight: bold;
    }
</style>