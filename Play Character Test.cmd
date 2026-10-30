@echo off
cd /d "%~dp0runtime\ikemen"
if not exist chars\mvb_prototype\mvb_prototype.def (
  echo Build the prototype first. See IKEMEN-CHARACTER-TEST.md.
  pause
  exit /b 1
)
start "" /D "%CD%" "Ikemen_GO.exe" -p1 mvb_prototype -p2 kfm -p2.ai 0 -s stages/stage0.def -time -1 -windowed
