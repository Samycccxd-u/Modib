@echo off
cd /d "%~dp0"
title Creando Modib.exe

if not exist interfaz.py (
  echo No encuentro interfaz.py en esta carpeta.
  pause
  exit /b 1
)
if not exist modib.ico (
  echo No encuentro modib.ico en esta carpeta.
  pause
  exit /b 1
)
if not exist assets\fondo_fnf.png (
  echo Falta assets\fondo_fnf.png. Crea la carpeta assets y pon ahi los fondos.
  pause
  exit /b 1
)
if not exist assets\fondo_ddlc.png (
  echo Falta assets\fondo_ddlc.png. Crea la carpeta assets y pon ahi los fondos.
  pause
  exit /b 1
)

echo Creando Modib.exe ... (tarda uno o dos minutos, no cierres esta ventana)
echo.
python -m PyInstaller --onefile --windowed --icon modib.ico --add-data "assets;assets" --name Modib --workpath "%TEMP%\modib_build" interfaz.py
if errorlevel 1 (
  echo.
  echo Algo salio mal. Copia el mensaje de arriba y mandaselo a Claude.
  pause
  exit /b 1
)

move /y dist\Modib.exe Modib.exe >nul
if errorlevel 1 (
  echo.
  echo No pude dejar Modib.exe aqui. Si Modib esta abierto, cierralo y vuelve a intentarlo.
  pause
  exit /b 1
)

rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
rmdir /s /q "%TEMP%\modib_build" 2>nul
del /q Modib.spec 2>nul

echo.
echo Listo! Modib.exe esta en esta carpeta.
pause
