//import API from '../../../api.js'

import API from '../../../api_awssam.js'
import store from '../../index.js'

export default {
   async generateMetrics(context,payload){
       console.log(payload.querystring)
       const token = store.getters.getJwtToken 

        const response = await fetch(`${API.generateMetrics}?${payload.querystring}`,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${token}`
            }
        })
        
        if (response.status === 403){
            store.dispatch('autoLogout')
        }
        if(!response.ok){
            const error = new Error('Error in generating metrics')
            throw error
        }else{
            const data = await response.json()
            //context.commit('mutGeneratedMetrics',data)
            console.log(data[1])
            payload.data = data
            if(payload.option_metrics == 'tag'){
                context.dispatch('generateMetricsBasedOnTags', payload)
            }else{
                context.dispatch('generatedMetricsBasedCdr' , payload)
            }

        }
    },
    generateMetricsBasedOnTags(context,payload){
        //begin extracting the payload.data
        const data = payload.data
        const sortOrder = payload.sort_order
        const option = payload.data.option+ ' TAGS'

        const tagsOptions = []
        const listOfTags = []
        const listOfMonths = []

        //tagmetricsexport object settings
        //export  object base structure
        const metricsExportObject =   {
            "options": {
                "fileName": ""
            },
            "tableData": [
                {
                "sheetName": "Sheet1",
                "data": [
                
                ],
                "granddata" : [


                ]
                }
            ]
           }
         const head = []  
         head.push(option)

        for (let [key,value] of Object.entries(data)){
            for( let t=0; t <tagsOptions.length;t++ ){
                if(key == tagsOptions[t]){
                    tagsOptions.splice(t,1)
                }
            }
            //extact available months used for table header
            if(typeof value == 'object'){
                for(let key1 of Object.keys(value)){
                    
                    if(listOfMonths.includes(key1) === false){
                        let heading = {text: key1}
                        head.push(heading)
                        listOfMonths.push(key1)
                    }
                }
            }
        }

         //tagmetricsexport object settings
        let total = {text: `Total `}
         head.push(total)
         metricsExportObject.tableData[0].data.push(head)

        //create table header tag metrics
        const tableTagHeader = [option, ...listOfMonths, 'Total']
         
        //construct the value to be put on the table
        for (const [key, value] of Object.entries(data)){
            let listOfTag = []
            if (typeof value === 'object'){
            listOfTag.push(key)
            for (let value1 of Object.values(value)){
                if (value1 === 0){
                value1 === '';
                }
                listOfTag.push(value1)
            }
            listOfTags.push(listOfTag)
            }

        }

        //sort the tags base on the selected order
        let sortedTagRecords;
        if(sortOrder === "descending"){
            sortedTagRecords = listOfTags.sort(function(a,b){
            return b.filter(el =>{
                if(typeof el === 'number'){
                    return el
                }
            }).reduce((subtotal,nextVal) => {
                return subtotal + nextVal
            },0) - a.filter(el => {
                if(typeof el === 'number'){
                    return el
                }
            }).reduce((subtotal, nextVal) => {
                return subtotal + nextVal
            },0)
        })
        }else{
            sortedTagRecords = listOfTags.sort(function(a,b){
            return a.filter(el =>{
                if(typeof el === 'number'){
                    return el
                }
            }).reduce((subtotal,nextVal) => {
                return subtotal + nextVal
            },0) - b.filter(el => {
                if(typeof el === 'number'){
                    return el
                }
            }).reduce((subtotal, nextVal) => {
                return subtotal + nextVal
            },0)
            })
        }

        for(let i= 0; i<sortedTagRecords.length ;i++){ 
            let data_array = [];
            let d
            for(let j=0 ; j<sortedTagRecords[i].length; j++){
                if(sortedTagRecords[i][j] == "0" || sortedTagRecords[i][j] == 0){
                   d = {text : ""}
                }else {
                    d = {text : sortedTagRecords[i][j]}
                }
               
               
               data_array.push(d)
               
            }
            //filter out the non number element and get the total value of all number element in filtered array
            let count = sortedTagRecords[i].filter(el => {
               if(typeof el === 'number'){
                return el
               }
            }).reduce((subtotal , nextVal) => {
              return subtotal + nextVal
            },0)
             var t = {text : count}
             data_array.push(t)
             metricsExportObject.tableData[0].data.push(data_array)
          }

         let data_range = { text : `Date Range: ${data.dateRange}`}
         let grand_total_tag = {text : `Grand Total Tag: ${data.total_records}`}
         let data_array = [data_range,'',grand_total_tag ];
         metricsExportObject.tableData[0].data.push([])
         metricsExportObject.tableData[0].data.push(data_array)

         metricsExportObject.options.fileName = `${data.option}-${data.dateRange}-tag`;
        

        payload.tagMetricsData = {tableHeader:tableTagHeader, tableTagRecords: sortedTagRecords,metricsExportObject }
        context.commit('mutGeneratedMetrics', payload)
        

    },
    generatedMetricsBasedCdr(context, payload){
        //begin extracting the payload.data
        let data = payload.data
        let sortOrder = payload.sort_order
        let option = payload.data[1].option
        const callCountsPercentage = `Call Counts Percentage(${data[1].callcount_weight}%)`
        const callDurationPercentage = `Call Duration Percentage(${data[1].duration_weight}%)`
        let tableCdrHeader = []

        //tagmetricsexport object settings
        //export  object base structure
         let metricsExportObject =   {
            "options": {
                "fileName": ""
            },
            "tableData": [
                {
                "sheetName": "Sheet1",
                "data": [
                
                ],
                "granddata" : [


                ]
                }
            ]
           }
           

            let heading = []
            let name = {text:  'NAME'}
            let extension = {text :"EXTENSION"}
            heading.push(name)
            heading.push(extension)

            if(data[1].callcount_weight == '0'){
                tableCdrHeader = [`${option}#`.toUpperCase(),'NAME,','EXTENSION', 'Total Calls Duration(HH:MM:SS)',  callDurationPercentage, 'Total(100%)']
               
                //for excel headings
                heading.push({text:'Total Calls Duration(HH:MM:SS)'})
                heading.push({text:callDurationPercentage})

            }else if(data[1].duration_weight == '0'){
                tableCdrHeader = [`${option}#`.toUpperCase(),'NAME,','EXTENSION', 'Total Call Counts(#)',  callCountsPercentage, 'Total(100%)']

                //for excel headings
                heading.push({text:'Total Call Counts(#)'})
                heading.push({text:callCountsPercentage})

            }else{
                tableCdrHeader = [`${option}#`.toUpperCase(),'NAME,','EXTENSION', 'Total Call Counts(#)', 'Total Calls Duration(HH:MM:SS)', callCountsPercentage, callDurationPercentage, 'Total(100%)']
                
                //for excel headings
                heading.push({text:'Total Call Counts(#)'})
                heading.push({text:'Total Calls Duration(HH:MM:SS)'})
                heading.push({text:callCountsPercentage})
                heading.push({text:callDurationPercentage})

            }
            heading.push({text:'Total(100%)'})
            metricsExportObject.tableData[0].data.push(heading)

         //perform map function to  data array  to get  and add the total percentage to each object and make save it to new transformedata array  
        let transformedata = data[0].map(el => {
        el.c_percentage = (Number(el.total_counts/data[1].grand_total_counts)* Number(data[1].callcount_weight)).toFixed(3)
        el.d_percentage = (Number(el.total_sec/data[1].grand_total_duration_sec) * Number(data[1].duration_weight)).toFixed(3)	
        el.total_percentage = (Number(el.c_percentage) + Number(el.d_percentage)).toFixed(4)
        return el;
        })
        let sortedtransformedata 
        if(sortOrder === "descending"){
            sortedtransformedata  = transformedata.sort(function(a,b){
            return b.total_percentage - a.total_percentage;
        })
        }else {
            sortedtransformedata  = transformedata.sort(function(a,b){
            return a.total_percentage - b.total_percentage;
            })		     	
        }
        let outSideTableData  = {
            option: option,
            duration_weight: data[1].duration_weight,
            callcount_weight: data[1].callcount_weight ,
            grand_total_duration_sec: data[1].grand_total_duration_sec ,
            grand_total_duration:data[1].grand_total_duration ,
            grand_total_counts: data[1].grand_total_counts ,
            datetimeRange: data[1].datetimeRange ,
         }

         //construct logic for export object
        for(const d of sortedtransformedata){
            let metrics = []
            metrics.push({ text: d.name})
            metrics.push({text: d.extension})
            if(data[1].duration_weight == '0'){ 
                metrics.push({ text: d.total_counts})
                metrics.push({text : d.c_percentage + "%"} )
                metrics.push({ text: d.c_percentage + "%"})
                
            }else if(data[1].callcount_weight == '0'){
                metrics.push({ text: d.total_duration})
                metrics.push({ text: d.d_percentage + "%"})
                metrics.push({ text: d.d_percentage + "%"})
            }else{
                metrics.push({ text: d.total_counts})
                metrics.push({ text: d.total_duration})
                metrics.push({text : d.c_percentage + "%"} )
                metrics.push({ text: d.d_percentage + "%"})
                metrics.push({ text: d.total_percentage + "%"})

            }
            metricsExportObject.tableData[0].data.push(metrics)
         
            
        }
        metricsExportObject.tableData[0].data.push([]) // create extra line
        metricsExportObject.tableData[0].data.push([]) // create extra line
        metricsExportObject.tableData[0].data.push([]) // create extra line

        if(data[1].duration_weight == '0'){
            metricsExportObject.tableData[0].data.push([{text: 'Date Range: ' + data[1].datetimeRange}])
            metricsExportObject.tableData[0].data.push([{text: 'Grand Total Counts: '+ data[1].grand_total_counts}])
            metricsExportObject.options.fileName = `${data[1].option}-${data[1].datetimeRange}-callcounts`;

        }else if(data[1].callcount_weight == '0'){
            metricsExportObject.tableData[0].data.push([{text: 'Date Range: ' + data[1].datetimeRange}])
            metricsExportObject.tableData[0].data.push([{text: 'Grand Total Call Duration(HH:MM:SS): ' + data[1].grand_total_duration }])
            metricsExportObject.options.fileName = `${data[1].option}-${data[1].datetimeRange}-callduration`;
        }else{
            metricsExportObject.tableData[0].data.push([{text: 'Date Range: ' + data[1].datetimeRange}])
            metricsExportObject.tableData[0].data.push([{text: 'Grand Total Counts: '+ data[1].grand_total_counts}])
            metricsExportObject.tableData[0].data.push([{text: 'Grand Total Call Duration(HH:MM:SS): ' + data[1].grand_total_duration }])
            metricsExportObject.options.fileName = `${data[1].option}-${data[1].datetimeRange}-blended`;
        }
       
         //construct logic for export object end

       

        payload.cdrMetricsData = { tableHeader:tableCdrHeader, tableCdrRecords:sortedtransformedata, outSideTableData:outSideTableData, metricsExportObject }
        context.commit('mutGeneratedMetrics',payload)
    }
}