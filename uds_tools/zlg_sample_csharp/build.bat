@echo off
setlocal enabledelayedexpansion

REM ===== 預設參數（可由命令列覆寫） =====
set "CONFIGURATION=Debug"
set "BUILD_ARCH=x64"                         REM 會拿來當輸出資料夾名（也用來選 zlgcan_%BUILD_ARCH%）
set "NOWARN=0618;8632;1998"                  REM 壓掉的警告
set "BUILD_VERSION=1.0.0"                    REM -p:Version
set "PLATFORM=x64"                           REM -p:Platform

REM 用法：build_dotnet.bat [Config] [BuildArch]
if not "%~1"=="" set "CONFIGURATION=%~1"
if not "%~2"=="" set "BUILD_ARCH=%~2"

REM ===== 基本路徑 =====
set "BASEDIR=%~dp0"
if "%BASEDIR:~-1%"=="\" set "BASEDIR=%BASEDIR:~0,-1%"

REM ===== 路徑設定 =====
set "OUTDIR=%BASEDIR%\build\%BUILD_ARCH%"
set "ZLG_INSTALL_BAT=%BASEDIR%\Reference\install_zlg.bat"
set "ZLG_ZIP=%BASEDIR%\Reference\CAN_lib.zip"
set "UNZIP_DIR=%TEMP%\canlib_extract_%RANDOM%%RANDOM%"
set "SRC_ARCH=zlgcan_%BUILD_ARCH%"

REM ===== 前置檢查 =====
where dotnet >nul 2>nul
if errorlevel 1 (
  echo [ERROR] 找不到 dotnet CLI，請先安裝 .NET SDK。
  exit /b 1
)

echo == dotnet --info ==
dotnet --info | findstr /C:".NET SDK" /C:"RID" /C:"OS Platform"
echo.

echo == 參數 ==
echo   Configuration : %CONFIGURATION%
echo   BuildArch     : %BUILD_ARCH%
echo   Output Dir    : %OUTDIR%
echo   NoWarn        : %NOWARN%
echo   Version       : %BUILD_VERSION%
echo   Platform      : %PLATFORM%
echo.

REM ===== 清理 / 重建 OUTDIR =====
if exist "%OUTDIR%" (
  echo 清除舊的輸出資料夾：%OUTDIR%
  rmdir /s /q "%OUTDIR%"
)
mkdir "%OUTDIR%" >nul 2>nul

REM ===== Restore + Build =====
dotnet restore
if errorlevel 1 (
  echo [ERROR] restore 失敗
  exit /b 1
)

REM ===== Build =====
dotnet build ^
  -c %CONFIGURATION% ^
  -o "%OUTDIR%" ^
  -p:Version=%BUILD_VERSION% ^
  -p:Platform=%PLATFORM%

set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" (
  echo.
  echo [ERROR] Build 失敗（錯誤碼 %ERR%）
  exit /b %ERR%
)

echo.
echo [OK] Build 成功 → "%OUTDIR%"
echo.

REM ===== 安裝 ZLG 依賴（優先呼叫你現成的 install_zlg.bat；若不存在則走內建流程） =====
if exist "%ZLG_INSTALL_BAT%" (
  echo == 呼叫 Reference\install_zlg.bat 將 ZLG 依賴安裝到 OUTDIR ==
  REM 若你的 install_zlg.bat 支援外部覆寫 TARGETDIR，這裡直接傳入
  set "TARGET_PLATFORM=%BUILD_ARCH%"
  set "CONFIGURATION_NAME=%CONFIGURATION%"
  set "DOTNET_VERSION=net8.0"
  set "TARGETDIR=%OUTDIR%"
  call "%ZLG_INSTALL_BAT%"
) else (
  echo == 直接從 Reference\CAN_lib.zip 安裝 ZLG 依賴到 OUTDIR ==
  if not exist "%ZLG_ZIP%" (
    echo [WARN] 找不到 %ZLG_ZIP% ，略過 ZLG 依賴複製。
    goto :END
  )

  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZLG_ZIP%' '%UNZIP_DIR%'"
  if errorlevel 1 (
    echo [ERROR] 解壓 ZLG zip 失敗：%ZLG_ZIP%
    goto :END
  )

  if not exist "%UNZIP_DIR%\%SRC_ARCH%\zlgcan.dll" (
    echo [ERROR] 找不到 %SRC_ARCH%\zlgcan.dll，請檢查 zip 內容與 BUILD_ARCH。
    goto :CLEAN_TMP
  )

  echo 複製 kerneldlls -> %OUTDIR%\kerneldlls\
  xcopy /E /I /Y "%UNZIP_DIR%\%SRC_ARCH%\kerneldlls" "%OUTDIR%\kerneldlls\" >nul

  echo 複製 zlgcan.dll -> %OUTDIR%\
  copy /Y "%UNZIP_DIR%\%SRC_ARCH%\zlgcan.dll" "%OUTDIR%\zlgcan.dll" >nul
)

:CLEAN_TMP
if exist "%UNZIP_DIR%" rmdir /s /q "%UNZIP_DIR%"

:END
echo.
echo 完成：%OUTDIR%
exit /b 0
