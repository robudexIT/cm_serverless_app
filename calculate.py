from datetime import datetime

# Example row data (simulating $row_calls in PHP)
row_calls = {
    'StartTimeStamp': '20240524-182510',
    'EndTimeStamp': '20240524-182513'
}


def sec_to_hr(seconds):
      hours = int(seconds // 3600)
      minutes = int((seconds // 60) % 60) 
      seconds = int(seconds % 60) 
      return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
 


# Split the timestamps
endtime = row_calls['EndTimeStamp'].split('-')
starttime = row_calls['StartTimeStamp'].split('-')

# Parse the date and time components
end_datetime = datetime.strptime(endtime[0] + endtime[1], '%Y%m%d%H%M%S')
start_datetime = datetime.strptime(starttime[0] + starttime[1], '%Y%m%d%H%M%S')

# Calculate the total difference in seconds
total = (end_datetime - start_datetime).total_seconds()

total_duration = sec_to_hr(total)

startdate = datetime.now().strftime('%Y-%m-%d')
enddate = datetime.now().strftime('%Y-%m-%d')


callstart = datetime.strptime(starttime[1], "%H%M%S").strftime("%I:%M:%S %p")

 
print(callstart)
