@ECHO OFF
REM Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
REM recoil-master-everyone Copyright (C) 2024 numlinka.

ECHO ========== START ==========

ECHO Clean up old cache ...
rd /s /q .\build 1>nul
rd /s /q .\dist 1>nul

ECHO Build win32api-mouse ...
pyinstaller -i .\assets\favicon.ico -F .\src\win32api-mouse\win32api-mouse.py 1>nul 2>nul

ECHO Build recoil-master-everyone ...
pyinstaller -i .\assets\favicon.ico -w .\src\desktop\recoil-master-everyone.py 1>nul 2>nul

ECHO Prepare the directory structure ...
mkdir .\dist\recoil-master-everyone\assistance 1>nul
mkdir .\dist\recoil-master-everyone\assistance\mouse 1>nul
mkdir .\dist\recoil-master-everyone\assistance\deyboard 1>nul
move .\dist\win32api-mouse.exe .\dist\recoil-master-everyone\assistance\mouse\ 1>nul
rename .\dist\recoil-master-everyone\assistance\mouse\win32api-mouse.exe win32api.exe 1>nul

ECHO Prepare resource files ...
xcopy .\assets .\dist\recoil-master-everyone\assets\ /E /I /H /Y 1>nul

ECHO Clean up cache ...
rd /s /q .\build 1>nul

ECHO ========== FINISH ==========
explorer .\dist\
