@echo off
setlocal enabledelayedexpansion

cd %~dp0

docker compose build

docker compose up
