@echo off
setlocal EnableDelayedExpansion

if not exist  "%~1"    call :end 1
if not exist  "%~2"    call :end 2
if "%~x1" neq ".py"    call :end 3

pushd %~f2
if %errorlevel% neq 0 call :end 4
popd

set file="%~dpnx1"
set path="%~f2"

::Debug
echo %file%
echo %path%
echo.

for /r %path% %%P in (*.py) do ( 
    if "%%P" neq %file% if "%%~nxP" equ "%~nx1" ( 
        echo "%%P"
        C:\Windows\System32\choice.exe /m "Copy ?"
        if !errorlevel!==1 copy /y %file% "%%P">nul
    )
)

call :end 0

:end
echo Code %1
endlocal
pause
exit %1
