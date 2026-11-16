@echo off
rem Deletes stray compiled Ren'Py files (.rpyc whose .rpy is gone). Close the game first.
cd /d "%~dp0.."
python tools\clean_orphan_rpyc.py
pause
