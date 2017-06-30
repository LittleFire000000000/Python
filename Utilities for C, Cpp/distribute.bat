@echo off
setlocal EnableDelayedExpansion
if exist release rd /q /s release
if exist release.zip del /q /s release.zip
md release
for /F "delims=\ tokens=2" %%B in (list.txt) do xcopy /s "%%B" "release\%%B"
choice /n /m "Password [y/n]: "
if !errorlevel! equ 1 (
        set /p password=Password: 
        set password=!password:"=!
        set password=!password: =_!
        echo Final : !password!
        7za a release.zip -tzip -mx9 "-p!password!" @list.txt
) else 7za a release.zip -tzip -mx9 @list.txt
rd /q /s release
endlocal
pause
exit 0