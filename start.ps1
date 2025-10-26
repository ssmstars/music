# Change to script directory and run app.py
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $scriptDir

Write-Host "===================================="
Write-Host "AI Music Recommendation System"
Write-Host "===================================="
Write-Host ""
Write-Host "Starting the application..."
Write-Host ""

if (Test-Path ".\app.py") {
    try {
        & python ".\app.py" $args
        $exitCode = $LASTEXITCODE
    } catch {
        Write-Error "Failed to start python: $_"
        $exitCode = 1
    }
} else {
    Write-Error "app.py not found in $scriptDir"
    $exitCode = 1
}

Write-Host ""
if ($exitCode -ne 0) {
    Write-Host "Application exited with code $exitCode"
} else {
    Write-Host "Application exited."
}

Read-Host -Prompt "Press Enter to exit"
Pop-Location
