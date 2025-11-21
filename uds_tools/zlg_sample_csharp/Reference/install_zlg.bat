@echo off
setlocal

REM 取得這個bat所在的資料夾 (結尾含反斜線)
set "BASEDIR=%~dp0"
REM 去掉最後一個反斜線
if "%BASEDIR:~-1%"=="\" set "BASEDIR=%BASEDIR:~0,-1%"

set "TARGET_PLATFORM=x86"
set "CONFIGURATION_NAME=Debug"
set "SDK_VER=net8.0"
REM 目標資料夾：..\zlg_sample_csharp\bin\x64\Debug（以本bat所在位置為基準）
set "TARGETDIR=%BASEDIR%\..\zlg_sample_csharp\bin\%TARGET_PLATFORM%\%CONFIGURATION_NAME%\%SDK_VER%"

REM 確保目標資料夾存在
if not exist "%TARGETDIR%" mkdir "%TARGETDIR%"

REM 檢查壓縮檔是否存在
if not exist "%BASEDIR%\CAN_lib.zip" (
  echo [ERROR] 找不到 %BASEDIR%\CAN_lib.zip
  pause
  exit /b 1
)

echo == 解壓縮 CAN_lib.zip ==
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%BASEDIR%\CAN_lib.zip' '%BASEDIR%\CAN_lib'"

echo == 複製 zlgcan_x86/64\kerneldlls 到目標資料夾 ==
xcopy /E /I /Y "%BASEDIR%\CAN_lib\zlgcan_%TARGET_PLATFORM%\kerneldlls" "%TARGETDIR%\kerneldlls\"

echo == 複製 zlgcan_x86/64\zlgcan.dll 到目標資料夾 ==
copy /Y "%BASEDIR%\CAN_lib\zlgcan_%TARGET_PLATFORM%\zlgcan.dll" "%TARGETDIR%\zlgcan.dll"

echo.
echo 完成: %TARGETDIR%
pause
