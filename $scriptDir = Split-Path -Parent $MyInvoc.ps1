$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $scriptDir

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "AI Music Hub - Music Recommendation System" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting the application..." -ForegroundColor Yellow
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
    Write-Host "Application exited with code $exitCode" -ForegroundColor Red
} else {
    Write-Host "Application exited successfully." -ForegroundColor Green
}

Read-Host -Prompt "Press Enter to exit"
Pop-Location
