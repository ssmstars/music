@echo off
pushd "%~dp0"
echo ====================================
echo AI Music Hub - Music Recommendation System
echo ====================================
echo.
echo Starting the application...
echo.
if exist "%~dp0app.py" (
    python "%~dp0app.py" %*
    set EXIT_CODE=%ERRORLEVEL%
) else (
    echo ERROR: app.py not found in "%~dp0"
    set EXIT_CODE=1
)
echo.
if %EXIT_CODE% neq 0 (
    echo Application exited with error code %EXIT_CODE%.
) else (
    echo Application exited successfully.
)
echo.
pause
popd
