# Run tests in Docker container
Write-Host "Building test container..." -ForegroundColor Cyan
docker build -f backend/Dockerfile.test -t grievance-api-test backend/

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nRunning tests..." -ForegroundColor Cyan
    docker run --rm grievance-api-test
} else {
    Write-Host "`nFailed to build test container" -ForegroundColor Red
    exit 1
}
