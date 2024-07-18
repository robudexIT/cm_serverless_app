<template>       
        <div>
            <form method="GET" id="genMentrics" @submit.prevent="generateMetrics">
             <div :class="divError">
                 <p  class="pError" v-if="!group.isValid">Please Select option below</p>
                <div class="input-group mb-3">
                  
                    <div class="input-group-prepend">
                        <label class="input-group-text" for="inputGroupSelect01">Select </label>
                      </div>
                    <select class="form-select" name="group" form="genMentrics"  id="group" v-model="group.val" @blur="clearErrorField(group)">
                      <option value="csdinbound">CSD-INBOUND</option>
                      <option value="csdoutbound">CSD-OUTBOUND</option>
                        <option value="collection">COLLECTION</option>
                    </select>
                </div>
                <div :class="inValidDateRange">
                  <p class="pError" v-if="!isValidDateRange">Start Date should not be greater the End Date</p>
                  <p class="pError" v-if="!isValidDateRange">Or Selected Date Should not be greater than the current Date</p>
                  <div class="form-group">
                        <label for="start_date_and_time">Start Date & Time</label>
                          <p class="pError" v-if="!startDateTime.isValid">Empty Fields Are not Allowed</p>
                        <!-- <input type="text" class="form-control" id="start_date_and_time" name="start_date_and_time" aria-describedby="start_date_and_time" placeholder="Enter Date & Time" required> -->
                        <!-- <datetime v-model="startDateTime"></datetime> -->
                        <!-- <vue-ctk-date-time-picker v-model="startDateTime"></vue-ctk-date-time-picker> -->
                        <date-picker v-model="startDateTime.val" placeholder="Enter Date and Time ..." position="left" ref="start_date_and_time" @click="clearErrorField(startDateTime)"></date-picker>
                  </div>
                  <div class="form-group">
                      
                        <label for="end_date_and_time">End Date & Time</label>
                        <p class="pError" v-if="!endDateTime.isValid">Empty Fields Are not Allowed</p>
                        <!-- <vue-ctk-date-time-picker v-model="endDateTime"></vue-ctk-date-time-picker> -->
                        <!-- <datetime v-model="endDateTime"></datetime> -->
                        <!-- <input type="text" class="form-control" id="end_date_and_time" name="end_date_and_time" aria-describedby="end_date_and_time" placeholder="Enter Date & Time" > -->
                          <date-picker v-model="endDateTime.val" placeholder="Enter Date and Time ..." position="left" ref="end_date_and_time"  @click="clearErrorField(endDateTime)"></date-picker>
                  </div>
                </div>
                  <p class="pError" v-if="!optionMetrics.isValid">Please Select Valid Option Metrics</p>
                  <div class="input-group mb-3">
                      <div class="input-group-prepend">
                        <label class="input-group-text" for="inputGroupSelect01">Select Metrics </label>
                      </div>
                      <select class="form-select" name="option_metrics"  id="option_metrics" v-model="optionMetrics.val" @change="selectMetrics" @blur="clearErrorField(optionMetrics)">
                        <option option value="" disabled selected></option>
                        <option value="callduration">Call Durations</option>
                        <option value="callcounts">Call Counts</option>
                        <option value="blended">Blended Durations/Counts</option>
                          <option value="tag">Tags</option>
                      </select>
                      
                  </div>
                  <div class="border" v-if="selectBlended" >
                    
                    <p>Choose Your Desired Weight Percentage(%):</p>
                    <p class="pError" v-if="!hasWeightOption"> Please Desired Percentage Other Than 0(%)</p>
                      <div class="row">
                        <div class="cl">

                        </div>
                          <div class="col-2 pr-0 mr-0 ">
                              <label class="pr-0 mr-0 ">Select CallDuration Weight: </label>
                          </div>
                          <div class="col-2 pl-0 ml-0">
                            <select class="custom-select"  id="duration_weight" name="duration_weight" v-model="callDurationWeight" v-on:change="setDurationPercentage" >
                              <option value="0" selected>0</option>
                              <option  v-for=" count in 100" :key="count" :value="count" selected>{{count}}</option>
                            </select>
                        </div>
                      </div>
                        <br>
                      <div class="row">
                        <div class="col-2 pr-0 mr-0">
                            <label class="pr-0 mr-0 ">Select CallCounts Weight: </label>
                        </div>
                          <div class="col-2 pl-0 ml-0">
                            <select class="custom-select" id="callcount_weight" name="callcount_weight" v-model="callCountsWeight" v-on:change="setCountPercentage" >
                              <option value="0" selected>0</option>
                                <option  v-for=" count in 100" :key="count" :value="count" selected>{{count}}</option>
                            </select>
                        </div>
                      </div>             
                  </div>
                  <div class="row">
                          <p class="pError" v-if="!sortedOrder.isValid">Please Select Valid SortOrder</p>
                          <div class="col-2">
                            <label class="pr-0 mr-0 mt-2">Sort Order: </label>
                            <select class="form-select" id="sorted_order" name="sorted_order" v-model="sortedOrder.val" @blur="clearErrorField(sortedOrder)">
                              <option value="descending" selected>DESCENDING</option>
                              <option value="ascending" >ASCENDING</option>
                            </select>
                        </div>
                  </div>                 
                    <br>
                  <div class="text-left mb-3">
                        <input type="submit" name="genbtn"  class="btn btn-primary ml-auto" value="Generate" id="genbtn" generateMetrics>
                  </div>
             </div>  
            </form>
        </div>
        <div id="calltype_modal"></div>

</template>

<script>

 import DatePicker from 'vue3-date-time-picker';


export default {
    components: {
       DatePicker
    },
    data(){
        return {
            sortedOrder: {
              val: null,
              isValid: true
            },
            group: {
              val: null,
              isValid: true
            },
            optionMetrics: {
              val: null,
              isValid: true
            },
            callDurationWeight: 0,
            callCountsWeight: 0,
            hasWeightOption: true,

            startDateTime: {
              val: '',
              isValid: true
            },
            endDateTime: {
              val: '',
              isValid: true
            },
            isValidDateRange: true,
            selectBlended: false,
            formIsValid: true,
                
        }
    },
    methods:{
      
        setDurationPercentage(){
            this.callCountsWeight = 100 - this.callDurationWeight
        },
        setCountPercentage(){
            this.callDurationWeight = 100 - this.callCountsWeight
        },
        selectMetrics(){
            if(this.optionMetrics.val == 'callduration'){
                this.callDurationWeight = 100
                this.callCountsWeight = 0
                this.selectBlended = false
            }   
            if(this.optionMetrics.val == 'callcounts'){
                this.callDurationWeight = 0
                this.callCountsWeight = 100
                this.selectBlended = false
            }
            if(this.optionMetrics.val == 'blended'){
                this.callDurationWeight = 0
                this.callCountsWeight = 0
                this.selectBlended = true
            }
            if(this.optionMetrics.val == 'tag'){
              this.callDurationWeight = 0
              this.callCountsWeight = 0
              this.selectBlended = false

            }
        },
        formValidation()
        {
          this.formIsValid = true
           if(this.group.val == '' || this.group.val == null){
             this.group.isValid = false
             this.formIsValid = false
             return
           }
           if(this.startDateTime.val == '' || this.startDateTime.val == null){
             this.startDateTime.isValid = false
             this.formIsValid = false
             return
           }
           if(this.endDateTime.val == '' || this.endDateTime.val == null){
             this.endDateTime.isValid = false
             this.formIsValid = false
             return
           }

           if(this.optionMetrics.val == '' || this.optionMetrics.val == null){
             this.optionMetrics.isValid = false
             this.formIsValid = false
             return
           }
           if(this.optionMetrics.val == 'blended'){
             if(this.callDurationWeight == 0 && this.callCountsWeight == 0){
              this.formIsValid = false
              this.hasWeightOption = false
              return
            }
           }
           if(this.sortedOrder.val == '' || this.sortedOrder.val == null){
             this.formIsValid = false 
             this.sortedOrder.isValid = false 
             return
           }
           
         
           const startTimeStamp =  this.startDateTime.val.getTime()
           const endTimeStamp =  this.endDateTime.val.getTime()
           const currentTimeStamp = new Date().getTime()

           
           if(startTimeStamp > currentTimeStamp || endTimeStamp > currentTimeStamp){
             alert('Select Date is out of Range. Please Select Valid Date')
             this.formIsValid = false
             this.isValidDateRange = false
             return
           }
            
           if(startTimeStamp > endTimeStamp){
              // this.$refs.end_date_and_time.clearValue()
              // this.$refs.start_date_and_time.clearValue()
              alert('Start Date should not be greater the End Date')
              this.formIsValid = false
              this.isValidDateRange = false
              return
              
           }
           return this.formIsValid
        },
        clearErrorField(inputField){
          inputField.isValid = true
        },
        generateMetrics(){
           if(!this.formValidation()){
             return
           }
        
           //get offset in milliseconds bet utc and localtime
           //by default, getTimezoneOffset return the offset in minutes   
           let getTimezoneOffset = new Date().getTimezoneOffset() * 60000

           //convert startTimeStamp and endTimeStamp to milliseconds and subtract the getTimezoneOffset
           //do this because always .toISOString() convert to the localtime to utc
           //so to able to achive the original localtime when the convertion happened,
           //get the timezoneoffset of the localtime to utc and subtract it.
           let startTimeStamp =  this.startDateTime.val.getTime() - getTimezoneOffset
            let endTimeStamp =    this.endDateTime.val.getTime() - getTimezoneOffset
 
           // convert to a string of YYYY-MM-DD HH:MM:ss
           let start_date_and_time = new Date(startTimeStamp).toISOString().substr(0, 19).replace('T', ' ')
           let end_date_and_time = new Date( endTimeStamp).toISOString().substr(0, 19).replace('T', ' ')

      
           
           this.$router.push({name: 'generatedmetrics',
              params: {
                sort_order: this.sortedOrder.val,
                option_metrics: this.optionMetrics.val
              },
              query: {group: this.group.val,
                      start_date_and_time,
                      end_date_and_time,
                      option_metrics: this.optionMetrics.val,
                      duration_weight: this.callDurationWeight,
                      callcount_weight: this.callCountsWeight,
                      
              },
              
           
           })
        }
    
    },
    computed:{
      getTypeOf(){
        return typeof this.bob
      },
      divError(){
        return !this.formIsValid ? 'divError' : ''
      },
      inValidDateRange(){
        return !this.isValidDateRange ? 'dateRangeError' : ''
      }
        
    },
    created(){
      
    },
   
}
</script>

<style >
   @import '../../../../node_modules/vue3-date-time-picker/dist/main.css';
  .invalid label {
  color: red;
  }
  .form_invalid {
    color: red;
  }
  .invalid input,
  .invalid textarea {
    border: 1px solid red;
  }

 .dp__input {
   color: blue;
   height: 40px;
   font-size: 20px;
   background-color: rgb(235, 227, 227);
   padding: 5px;
   margin:20px 0  ;

 }
  #tj-datetime-input{
      color: blue;
      background-color: rgb(238, 238, 238);
      height: 40px;
  }
  .divError {
     border: 5px solid red;
     padding: 15px;
  }
  .dateRangeError {
    border: 1px solid red;
    padding: 5px;
  }
  .pError {
    color: red;
    font-weight: bold;
  }
</style>