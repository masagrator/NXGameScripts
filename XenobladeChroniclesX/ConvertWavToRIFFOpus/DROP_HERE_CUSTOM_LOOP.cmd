@echo off
cd %~dp0
set /p "start_l=Write loop start in milliseconds (Write 0 to play from the beginning): "
python Convert.py %1 --loop %start_l%
pause