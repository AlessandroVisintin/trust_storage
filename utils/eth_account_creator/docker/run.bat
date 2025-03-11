@echo off
setlocal enabledelayedexpansion

cd %~dp0

mkdir "..\build" 2>nul

docker compose build

set /p NUM_ACCOUNTS="How many Ethereum accounts do you want to create? "
for /l %%i in (1,1,%NUM_ACCOUNTS%) do (
    echo Creating account %%i of %NUM_ACCOUNTS%...
    docker compose run --rm eth_account_generator
)
