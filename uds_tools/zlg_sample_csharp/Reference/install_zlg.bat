@echo off
setlocal

REM === 基本路徑 ===
set "BASEDIR=%~dp0"
if "%BASEDIR:~-1%"=="\" set "BASEDIR=%BASEDIR:~0,-1%"

REM === 可調參數 ===
set "TARGET_PLATFORM=x64"          REM 可改成 x86
set "CONFIGURATION_NAME=Debug"     REM Debug / Release
set "DOTNET_VERSION=net8.0"     REM Debug / Release

REM === 路徑設定 ===
set "TARGETDIR=%BASEDIR%\..\zlg_sample_csharp\bin\%TARGET_PLATFORM%\%CONFIGURATION_NAME%\%DOTNET_VERSION%"
set "ZIP_PATH=%BASEDIR%\CAN_lib.zip"
set "UNZIP_DIR=%BASEDIR%\CAN_lib"
set "SRC_ARCH=zlgcan_%TARGET_PLATFORM%"

REM 目標資料夾
if not exist "%TARGETDIR%" mkdir "%TARGETDIR%"

REM 檢查 ZIP 是否存在
if not exist "%ZIP_PATH%" (
  echo [ERROR] 找不到 %ZIP_PATH%
  echo 請先把 CAN_lib.zip 放到同一層資料夾再執行。
  pause
  exit /b 1
)

echo == 解壓縮 CAN_lib.zip ==
if exist "%UNZIP_DIR%" rmdir /s /q "%UNZIP_DIR%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZIP_PATH%' '%UNZIP_DIR%'"

echo == 複製 %SRC_ARCH%\kerneldlls 到目標資料夾 ==
xcopy /E /I /Y "%UNZIP_DIR%\%SRC_ARCH%\kerneldlls" "%TARGETDIR%\kerneldlls\" >nul

echo == 複製 %SRC_ARCH%\zlgcan.dll 到目標資料夾 ==
copy /Y "%UNZIP_DIR%\%SRC_ARCH%\zlgcan.dll" "%TARGETDIR%\zlgcan.dll" >nul

echo.
echo 完成: %TARGETDIR%
pause
