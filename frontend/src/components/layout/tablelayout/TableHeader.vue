<template>

    <tr v-if="theader=='csdinbound' || theader=='csdoutbound' || theader=='collection' || theader=='sales'">
        <th scope="col">#</th>
        <th scope="col">EXTENSION</th>
        <th scope="col">NAME</th>
        <th scope="col" v-if="theader=='sales'">TEAMLEADER</th>
        <th scope="col">Total Made Calls </th>
        <th scope="col">Total Calls Duration</th>
         <slot></slot>
    </tr>

    <tr v-if="theader=='csdinbounddetails' || theader=='csdoutbounddetails' || theader=='collectiondetails' || theader=='salesdetails'">
        <th scope="col">#</th>
        <th scope="col" v-if="theader=='csdinbounddetails'">Extension</th>
        <th scope="col">Called(#)</th>
        <th scope="col">Caller</th>
        <th scope="col">CallStatus</th>
        <th scope="col">StartTime</th>
        <th scope="col">EndTime</th>
        <th scope="col">Duration</th>
        <th scope="col">Recordings</th> 
        <slot></slot>
        <th scope="col">Comment/Tag</th>
     </tr>

     <tr v-if="theader=='parkedcalls'">
        <th scope="col">#</th>
        <th scope="col">Caller</th>
        <th scope="col">Waiting Time</th>
        <th scope="col">Date</th>                  
    </tr>

     <tr v-if="theader=='missedcalls'">
         <th scope="col">#</th>
        <th scope="col" >Total Missed Calls</th>
        <slot></slot>
    </tr>

     <tr  v-if="theader=='detailedmissedcalls'"> 
         <th scope="col">#</th>
         <th scope="col">StartTime</th>
         <th scope="col">EndTime</th>
         <th scope="col">Caller</th>
         <th scope="col">CallStatus</th>
         <th scope="col">Comment</th>
         <th scope="col">Comment By</th>
         <slot></slot>
     </tr>

     <tr v-if="theader=='voicemails'">
        <th scope="col">#</th>
        <th scope="col">Caller</th>
        <th scope="col">Date</th>
        <th scope="col">Time</th>
        <th scope="col">VoiceMail</th>
        <th scope="col">Action</th>
    </tr>

     <tr v-if="theader=='phoneloginheader'">
        <th scope="col">#</th>
        <th scope="col">EXTENSION</th>
        <th scope="col">NAME</th>
        <th scope="col">LOGIN/LOGOUT</th>
        <th scope="col">LOGIN DURATION</th>
        <th scope="col">SERVER USED</th>
        <th scope="col">SERVER STATUS</th>
        <th scope="col">CHANNEL STAT</th>
    </tr>

     <tr v-if="theader=='phoneloginheaderdetails'">
        <th scope="col">#</th>
        <th scope="col">LOG</th>
        <th scope="col">DATE</th>
        <th scope="col">TIME</th>
    </tr>

     <tr v-if="theader=='agent'">
        <th scope="col"><h3>#</h3></th>
        <th scope="col"><h3>Extension</h3></th>
        <th scope="col"><h3>Name</h3></th>
        <th scope="col"><h3>Email</h3></th>
        <th scope="col"><h3>Action</h3></th>
     </tr>

     <tr v-if="theader=='tags'">
        <th scope="col">#</th>  
       <th scope="col">TAGTYPE</th>
       <th scope="col">TAGNAME</th>
       <th scope="col">CREATED</th>
       <th scope="col">CREATED DATE</th>
       <th scope="col">ACTION</th>
    </tr>

    <tr v-if="theader=='metricsHeader'">
        <th v-for="header in metricsHeader" :key='header'>{{header}}</th>
    </tr>
    <tr v-if="theader=='searchnumberIn'">
        <th scope="col">#</th>
        <th  scope="col">Answered_By</th>
        <th scope="col">Extn</th>
         <th scope="col">Called(#)</th>
         <th scope="col">Caller</th>
        <th scope="col">CallStatus</th>
        <th scope="col">StartTime</th>
        <th scope="col">EndTime</th>
        <th scope="col">Duration</th>
        <th scope="col">Recordings</th> 
        <th scope="col">Date</th>
        <th scope="col">Comment/Tag</th>
      
    </tr>

    <tr v-if="theader=='searchnumberOut'">
        <th scope="col">#</th>
        <th  scope="col">Caller</th>
         <th scope="col">Extn</th>
        <th scope="col">Called(#)</th>
        <th scope="col">CallStatus</th>
        <th scope="col">StartTime</th>
        <th scope="col">EndTime</th>
        <th scope="col">Duration</th>
        <th scope="col">Recordings</th> 
        <th scope="col">Date</th>
        <th scope="col">Comment/Tag</th>
      
    </tr>

    <tr v-if="theader=='customerinfo'">
        <th scope="col">Customer_Number</th> 
        <th scope="col">Customer_ID</th>
        <th scope="col">Customer_Name</th>
        <th scope="col">Updated_By</th>
    </tr>
    <select-date-range-modal-form></select-date-range-modal-form>
    
</template>

<script>

export default {

    props:['theader','metricsHeader', 'calltype',],


   
}

</script>