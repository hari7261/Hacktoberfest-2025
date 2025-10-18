$ErrorActionPreference = "Stop"

# Always run Uvicorn from the project root so imports work
# Script location: <project>/backend/scripts/run_server.ps1
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Split-Path -Parent $scriptDir
$projectRoot = Split-Path -Parent $backendDir
Set-Location $projectRoot

# Resolve Python interpreter preference order:
# 1) Local venv at .venv\Scripts\python.exe if present
# 2) uvicorn on PATH
# 3) system 'python -m uvicorn'

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
Write-Host "[FactReal] Project root:" $projectRoot
if (Test-Path $venvPython) {
	Write-Host "[FactReal] Using venv interpreter:" $venvPython
	& $venvPython -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
}
elseif (Get-Command uvicorn -ErrorAction SilentlyContinue) {
	$uvPath = (Get-Command uvicorn).Source
	Write-Host "[FactReal] Using uvicorn on PATH:" $uvPath
	uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
}
else {
	$py = (Get-Command python -ErrorAction SilentlyContinue)
	if ($py) { Write-Host "[FactReal] Using system python:" $py.Source }
	else { Write-Host "[FactReal] 'python' not found on PATH" }
	python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
}
