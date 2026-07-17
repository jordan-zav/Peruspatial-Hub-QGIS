@echo off
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
set "PLUGIN_NAME=peruspatial_hub"
set "DIST_DIR=%SCRIPT_DIR%dist"
set "STAGE_DIR=%DIST_DIR%\_staging"

set "VERSION=%~1"
if not defined VERSION (
  echo.
  set /p "VERSION=Indique la version a empaquetar (ejemplo 1.2.0): "
)

if not defined VERSION (
  echo ERROR: debe indicar una version.
  exit /b 1
)

powershell -NoProfile -Command "if ($env:VERSION -notmatch '^[0-9]+(\.[0-9]+)+$') { exit 1 }"
if errorlevel 1 (
  echo ERROR: version no valida. Use numeros separados por puntos, por ejemplo 1.2.0.
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$path = Join-Path $env:SCRIPT_DIR 'metadata.txt';" ^
  "$content = [IO.File]::ReadAllText($path);" ^
  "$pattern = [regex]::new('(?m)^version=.*$');" ^
  "if (-not $pattern.IsMatch($content)) { exit 2 };" ^
  "$content = $pattern.Replace($content, 'version=' + $env:VERSION, 1);" ^
  "[IO.File]::WriteAllText($path, $content, [Text.UTF8Encoding]::new($false))"

if errorlevel 1 (
  echo ERROR: no se pudo actualizar la version en metadata.txt.
  exit /b 1
)

set "ZIP_FILE=%DIST_DIR%\PeruSpatial_Hub_QGIS_v%VERSION%.zip"

if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"
if exist "%STAGE_DIR%" rmdir /s /q "%STAGE_DIR%"
mkdir "%STAGE_DIR%\%PLUGIN_NAME%"

echo Preparando archivos del plugin...
robocopy "%SCRIPT_DIR%." "%STAGE_DIR%\%PLUGIN_NAME%" /E /R:1 /W:1 ^
  /XD "dist" "release" ".git" ".agents" ".codex" "__pycache__" ".pytest_cache" ".mypy_cache" ^
  /XF "*.pyc" "*.pyo" "*.zip" "generar_zip.bat" >nul

if errorlevel 8 (
  echo ERROR: no se pudieron copiar los archivos para empaquetar.
  if exist "%STAGE_DIR%" rmdir /s /q "%STAGE_DIR%"
  exit /b 1
)

if exist "%ZIP_FILE%" del /q "%ZIP_FILE%"

echo Generando ZIP instalable para QGIS...
set "ARCHIVE_BASE=%DIST_DIR%\PeruSpatial_Hub_QGIS_v%VERSION%"
python -c "import shutil; shutil.make_archive(r'%ARCHIVE_BASE%', 'zip', root_dir=r'%STAGE_DIR%')"

if errorlevel 1 (
  echo ERROR: Python no pudo generar el ZIP.
  if exist "%STAGE_DIR%" rmdir /s /q "%STAGE_DIR%"
  exit /b 1
)

rmdir /s /q "%STAGE_DIR%"

echo.
echo ZIP generado correctamente:
echo %ZIP_FILE%
exit /b 0
