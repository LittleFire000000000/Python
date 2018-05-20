@echo off
setlocal EnableDelayedExpansion

echo Handle "%~nx1"
choice /n /m "Install/remove [y/n]: "
set /a install=%errorlevel%
choice /n /m "Send a y/n? "
set /a send=%errorlevel%

if !install! == 1 (
	if !send! == 1 ( echo y|pip install "%~dpnx1"
	) else           echo n|pip install "%~dpnx1"
) else (
	if !send! == 1 ( echo y|pip uninstall "%~dpnx1"
	) else           echo n|pip uninstall "%~dpnx1"
)

endlocal
pause
exit /b
