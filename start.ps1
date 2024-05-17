# Your script code goes here
Write-Host "Hello, World!"
if (-not (Test-Path "C:\Program Files\Docker\Docker\DockerCli.exe")) {
    Write-Host "[!] Docker is not installed."
    exit 1
}
else {
    Write-Host "[*] Docker is installed."
}


if (-not $env:FREQUENCY) {
    Write-Host "[!] FREQUENCY is not set. Switching to default frequency: 1D."
    $env:FREQUENCY = "1D"
}

if (-not $env:EMAIL) {
    Write-Host "[!] EMAIL is not set."
    Write-Host "[!] Please set the EMAIL environment variable."
    exit 1
}

if (-not $env:IP) {
    Write-Host "[!] IP is not set."
    Write-Host "[!] Please set the IP environment variable."
    exit 1
}

if (-not $env:SENDER_PASS) {
    Write-Host "[!] SENDER_PASS is not set."
    Write-Host "[!] Please set the SENDER_PASS environment variable."
    exit 1
}

if (-not $env:USERNAME) {
    Write-Host "[!] USERNAME is not set. Switching to default username: admin."
    $env:USERNAME = "admin"
}

if (-not $env:PASSWORD) {
    Write-Host "[!] PASSWORD is not set. Switching to default password: admin."
    $env:PASSWORD = "admin"
}

Write-Host "[*] Pulling ghcr.io/adi7312/vuln-scan:latest..."
docker pull ghcr.io/adi7312/vuln-scan:latest
Write-Host "[*] Running the container in detached mode..."
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=$env:IP -e FREQUENCY=$env:FREQUENCY -e SENDER_PASS="$env:SENDER_PASS" -e EMAIL=$env:EMAIL -e USERNAME=$env:USERNAME -e PASSWORD=$env:PASSWORD --name avs ghcr.io/adi7312/vuln-scan:latest
docker exec avs /bin/bash /opt/app/config/setup_cron.sh
docker exec -it avs python3 /opt/app/gvm_handler.py