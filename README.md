# Vulnerability Scanning Automation

## Project Description

A tool for automating the scanning and assessment of vulnerabilities in a local network using the OpenVAS vulnerability scanner. The purpose of tool is conducting regular vulnerability scans in your local network and sending security reports after finished scan.

## Running with the script

### Environment variables:
* `IP` - the IP of the network to be scanned, provided with a mask (REQUIRED)
* `EMAIL` - email address to which the report will be sent (REQUIRED)
* `FREQUENCY` - scan frequency, possible options (REQUIRED):
  * `1D` - daily
  * `1W` - weekly
  * `1M` - monthly
* `S_PASS` - app password for the sender (Gmail)

The tool is primarily intended for platforms running Linux. It can also be run on Windows systems, but this is not officially supported due to issues with local network scanning.

### Linux

```
git clone https://github.com/adi7312/vuln-scan.git
cd ./vuln-scan
chmod +x start.sh
export IP=<IP>/<MASK>
export EMAIL=<EMAIL>
export FREQUENCY=<FREQ>
export S_PASS=<S_PASS>
./start.sh
```


## Running the container manually

Pull the container image:
```
docker pull ghcr.io/adi7312/vuln-scan:latest
```

Normal startup (may take 30-40 minutes):
```
docker run --detach --publish 8090:9392 -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

Startup without syncing the threat databases (faster startup):

```
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

## Container Audit

It is possible to conduct a security audit of the pulled container image when running the `start.sh` script by providing the `--audit-enable` argument. In that case, `start.sh` will invoke another script: `audit.sh`. An audit can also be performed at any time by executing the command: `bash audit/audit.sh`.

The result of the audit includes the following files: `vuln_scan_image_audit.txt` - a list of detected vulnerabilities, `vuln_scan_prob_analysis.txt` - vulnerabilities with a likelihood of exploitation greater than 20%, and `vuln_scan_image_sbom.txt` - Software Bill of Materials.

## Repository structure

```
/
|---src
|    |
|    |---gvm_handler.py
|    |
|    |---smtp_handler.py
|    |
|    |---logger.py
|
|    
|---config
|    |
|    |---update.sh  
|    |
|    |---setup_cron.sh
|
|
|---audit
|    |
|    |---audit.sh
|
|---start.sh
|
|---Dockerfile
```

* `gvm_handler.py` - script handling the operation of GVM: starting scans, generating reports, and retrieving IP addresses of devices from the network scanner (`scanner.py`)
* `smtp_handler.py` - script responsible for sending the PDF report to the end user
* `logger.py` - a simple script that logs events during the application's execution
* `update.sh` - script for updating GVM components, the operating system, etc.
* `setup_cron.sh` - script to set up the scan schedule
* `start.sh` - script that starts the container with default parameters
* `audit.sh` - script responsible for conducting a security audit of the container image
* `Dockerfile` - docker script responsible for building the container image



