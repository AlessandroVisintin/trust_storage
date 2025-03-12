@echo off
setlocal enabledelayedexpansion

cd %~dp0

mkdir "..\build" 2>nul

docker compose build

docker compose run --remove-orphans --rm qbft_genesis_creator
