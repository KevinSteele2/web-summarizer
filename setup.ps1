$venvPython = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
$requirements = Join-Path $PSScriptRoot 'requirements.txt'

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
    if (-not (Test-Path $venvPython)) {
        Write-Error "Failed to create venv. Is 'python' on PATH?"
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "Upgrading pip and installing requirements using the venv python..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r $requirements

Write-Host ""
Write-Host "Setup complete."
Write-Host "To activate the venv in this shell run:"
Write-Host "  .\venv\Scripts\Activate"