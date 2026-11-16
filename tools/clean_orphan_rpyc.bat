@echo off
rem Tidies compiled Ren'Py files after a pull. Close the game first.
rem Moves the .rpyc of a moved script to its new place (tools/dev/rpyc_moves.json) so saves
rem keep their place, then deletes the remaining stray .rpyc (whose .rpy is gone).
cd /d "%~dp0.."
python tools\clean_orphan_rpyc.py
pause
