@echo off
%1(start /min cmd.exe /c %0 :&exit)

D: && cd D:\Pyproject\ncwuConnector && python Main.py
