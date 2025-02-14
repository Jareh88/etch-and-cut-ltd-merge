# Run by typing the following into Powershell window: .\tail_log.ps1


# Get today's date in YYYYMMDD format
$todaysDate = Get-Date -Format "yyyyMMdd"

# Construct the log file name
$logFileName = "C:\EtchCut\DATA\LOGS\" + $todaysDate + ".log"

# Execute the Get-Content command with -Wait
Get-Content $logFileName -Wait