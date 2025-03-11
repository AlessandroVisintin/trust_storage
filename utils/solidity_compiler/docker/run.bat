@echo off
setlocal enabledelayedexpansion


set "folder=%~dp0"

if not exist "%folder%\docker-compose.yaml" (
    echo Error: docker-compose.yaml not found in script directory.
    exit /b 1
)

mkdir "%folder%\..\build" 2>nul

echo Searching for .sol files in %folder%
echo.

for %%F in ("%folder%\..\contracts\*.sol") do (
    set "filename=%%~nF"
    set "CONTRACT_NAME=!filename!"
    echo Processing contract: !filename!.sol
    echo.

    docker-compose -f "%~dp0docker-compose.yaml" up
    
    echo.
    if errorlevel 1 (
        echo Error: Docker Compose failed for !filename!.sol
    ) else (
        echo Successfully processed !filename!.sol
    )
    echo.
)

echo.
echo Search completed.