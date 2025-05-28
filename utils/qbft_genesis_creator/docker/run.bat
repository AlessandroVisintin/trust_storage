@echo off
setlocal enabledelayedexpansion

:: Change to script directory
cd /d "%~dp0"

:: Create directories
if not exist "..\data" mkdir "..\data"
if not exist "..\data\contracts" mkdir "..\data\contracts"

:: Initialize variables
set "contracts="
set "bootnodes="
set "validators="

:: Parse command line arguments
:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="--config" (
    if "%~2"=="" (
        echo Error: --config requires a filename
        exit /b 1
    )
    call :read_config_file "%~2"
    shift
    shift
    goto parse_args
) else (
    echo Unknown parameter: %~1
    echo Use --help for usage information
    exit /b 1
)

:end_parse

echo Current directory: %cd%

:: Handle contracts parameter
if defined contracts (
    echo Processing contracts...
    call :process_contracts
)

:: Handle validators parameter
if defined validators (
    echo Processing validators...
    type nul > "..\data\validators.txt"
    call :process_validators
)

:: Handle bootnodes parameter
if defined bootnodes (
    echo Processing bootnodes...
    type nul > "..\data\bootnodes.txt"
    call :process_bootnodes
)

:: Create build directory
if not exist "..\build" mkdir "..\build"

:: Run docker commands
docker compose build
if errorlevel 1 (
    echo Error: docker compose build failed
    exit /b 1
)

docker compose run --rm --remove-orphans qbft_genesis_creator
if errorlevel 1 (
    echo Error: docker compose run failed
    exit /b 1
)

echo Script completed successfully!
goto :eof

:: Function to read config file
:read_config_file
set "config_file=%~1"
if not exist "%config_file%" (
    echo Error: Configuration file '%config_file%' not found
    exit /b 1
)

echo Reading configuration from: %config_file%

for /f "usebackq tokens=* delims=" %%a in ("%config_file%") do (
    set "line=%%a"
    :: Skip empty lines and lines starting with # (comments)
    if not "!line!"=="" (
        if not "!line:~0,1!"=="#" (
            :: Check if line contains =
            echo !line! | findstr "=" >nul
            if not errorlevel 1 (
                for /f "tokens=1,* delims==" %%b in ("!line!") do (
                    set "key=%%b"
                    set "value=%%c"
                    :: Remove leading/trailing spaces (basic trimming)
                    set "key=!key: =!"
                    set "value=!value: =!"
                    
                    if "!key!"=="contracts" set "contracts=!value!"
                    if "!key!"=="bootnodes" set "bootnodes=!value!"
                    if "!key!"=="validators" set "validators=!value!"
                )
            )
        )
    )
)
goto :eof

:: Function to process contracts
:process_contracts
set "temp_contracts=%contracts:,= %"
for %%a in (%temp_contracts%) do (
    set "contract_path=%%a"
    :: Remove quotes if present
    set "contract_path=!contract_path:"=!"
    set "runtime_file=!contract_path!.bin-runtime"
    :: Convert to absolute path
    for %%i in ("!runtime_file!") do set "abs_runtime_file=%%~fi"
    for %%i in ("..\data\contracts\") do set "abs_dest_dir=%%~fi"

    if exist "!abs_runtime_file!" (
        echo   Copying: !abs_runtime_file!
        echo   To: !abs_dest_dir!
        copy "!abs_runtime_file!" "!abs_dest_dir!" 
        if errorlevel 1 (
            echo   Error: Failed to copy !abs_runtime_file!
        )
    ) else (
        echo   Warning: Contract file not found: !abs_runtime_file!
    )
)
goto :eof

:: Function to process validators
:process_validators
set "temp_validators=%validators:,= %"
for %%a in (%temp_validators%) do (
    set "node_path=%%a"
    :: Remove quotes if present
    set "node_path=!node_path:"=!"
    set "address_file=!node_path!\.address"
    if exist "!address_file!" (
        echo   Reading address from: !address_file!
        type "!address_file!" >> "..\data\validators.txt"
    ) else (
        echo   Warning: Address file not found: !address_file!
    )
)
goto :eof

:: Function to process bootnodes
:process_bootnodes
set "temp_bootnodes=%bootnodes:,= %"
for %%a in (%temp_bootnodes%) do (
    set "node_path=%%a"
    :: Remove quotes if present
    set "node_path=!node_path:"=!"
    set "pubkey_file=!node_path!\.pub"
    if exist "!pubkey_file!" (
        echo   Reading pubkey from: !pubkey_file!
        for /f "usebackq delims=" %%b in ("!pubkey_file!") do (
            echo %%b@placeholder >> "..\data\bootnodes.txt"
        )
    ) else (
        echo   Warning: Pubkey file not found: !pubkey_file!
    )
)
goto :eof
