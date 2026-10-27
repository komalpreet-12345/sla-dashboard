@echo off
cd /d C:\Users\komal\OneDrive\Desktop\sla-dashboard
if not exist logs mkdir logs
echo ---- %date% %time% ---- >> logs\run_log.txt
"C:\Users\komal\AppData\Local\Programs\Python\Python310\python.exe" main.py >> logs\run_log.txt 2>&1
