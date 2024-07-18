<template>
    
    <div class="modal fade" id="myDateRange" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">Select Date Range</h4>
        </div>
        <div class="modal-body">
                 <form @submit.prevent="submitFormata">
                    <div class="form-group">
                      <label for="startdate">From:</label>
                      <input type="date" class="form-control" aria-describedby="dateHelp"  required="true" v-model="fromDate" @change="validateDate()">
                    </div>
                     <div class="form-group">
                      <label for="enddate">To:</label>
                      <input type="date" class="form-control" aria-describedby="dateHelp" required="true" v-model="toDate" @change="validateDate()">
                    </div>
                     <div class="mb-3">
                      <label for="TagType">Filter By Tag:</label>
                       <select class="form-select" required v-model="selectedTag" >
                            <option selected value="all">all</option>
                             <option  value="">NO TAG</option>
                             <option v-for="tag in tags" :key="tag" :value="tag" >{{tag}}</option>

                      </select>
                    
                    </div>
                     <div class="mb-3" v-if="calltype != 'csdinbound'">
                      <label for="TagType">Select Duration Options(in seconds):</label>
                       <select class="form-select" required v-model="durationOptions" >
                            <option selected value="0 UP">0 UP</option>
                            <option  value="10 UP">10 UP</option>
                            <option  value="20 UP">20 UP</option>
                            <option  value="30 UP">30 UP</option>
                            <option  value="40 UP">40 UP</option> 
                            <option  value="50 UP">50 UP</option> 
                            <option value="60 UP">60 UP</option> 
                             <option  value="10 DWN">10 DOWN</option>
                            <option  value="20 DOWN">20 DOWN</option>
                            <option  value="30 DOWN">30 DOWN</option>
                            <option  value="40 DOWN">40 DOWN</option>
                            <option  value="50 DOWN">50 DOWN</option>
                            <option  value="60 DOWN">60 DOWN</option>
                      </select>
                    
                    </div>
                    <hr>
                    <div class="text-right mb-3">
                          <button type="submit " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal" id="addbtn" >Submit</button>
                         <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" >Close</button>
                    </div>

                </form> 
                
        </div>


      </div>

    </div>
  </div>
</template>

<script>
export default {
    props:['tags', 'calltype'],
    data(){
        return {
            fromDate: null,
            toDate: null,
            selectedTag: 'all',
            durationOptions: '0 UP'
        }
    },
    methods: {
        validateDate(){
            let startdate = this.fromDate.toString()
            
            let startdateSplit = startdate.split("-");
            let newStartDate = new Date(startdateSplit[0],startdateSplit[1]-1,startdateSplit[2]);
            let startdateTimeStamp = newStartDate.getTime();
            
            var enddate = this.toDate.toString()
            //get the timestamp of the  start date
            let enddateSplit = enddate.split("-");
            let newEndDate = new Date(enddateSplit[0],enddateSplit[1]-1,enddateSplit[2]);
            let enddateTimeStamp = newEndDate.getTime();

             var d = new Date();
            
             if(startdateTimeStamp > d.getTime() || enddateTimeStamp > d.getTime()){
              alert('Selected Date Must Not be Greater on the Current Date')
              
             
             }
             if(startdateTimeStamp > enddateTimeStamp){
              alert('StartDate Must not Greater on EndDate')
          
             }
        },
        submitFormata(){
            let duration = this.durationOptions.split(" ")[0]
            let direction = this.durationOptions.split(" ")[1]
            if(this.calltype == 'csdinbound'){
               duration = "0"
               direction = "UP"
            }
            this.$emit('emittedData',this.fromDate,this.toDate,this.selectedTag, duration, direction)
        }
    }
}
</script>