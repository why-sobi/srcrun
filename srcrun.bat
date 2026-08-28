@echo off
set SCRIPT_NAME=%1

:: Store raw args
set ARGS=%*

:: Strip out %1 (and any trailing space) from ARGS
call set ARGS=%%ARGS:*%1=%%

:: Run Python script with filtered args
python "D:\scripts\%SCRIPT_NAME%.py" %ARGS%