echo -e "\e[0;31m[!]\e[m WARNING: For this operation you need to be authentictaed into DockerHub!"
if ! docker scout version &> /dev/null; then
    echo -e "\e[0;31m[!]\e[m Docker Scout is not installed."
    echo -e "\e[0;36m[*]\e[m Installing Docker Scout..."
    curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
    sudo sh install-scout.sh
    echo -e "\e[0;32m[+]\e[m Docker Scout has been installed successfully."
else
    echo -e "\e[0;36m[*]\e[m Docker Scout is installed."
fi
echo -e "\e[0;36m[*]\e[m Performing an audit of the image ghcr.io/adi7312/vuln-scan:latest..."
sudo docker scout cves --format only-packages --output vuln_scan_image_audit.txt --exit-code ghcr.io/adi7312/vuln-scan:latest 
if [ $? -ne 2 ]; then
    echo -e "\e[0;32m[+]\e[m No vulnerabilities found. Audit completed with 0 vulnerabilities"
    exit 0
fi
echo -e "\e[0;31m[!]\e[m Found vulnerabilities. Audit completed. Results saved to vuln_scan_image_audit.txt."
echo -e "\e[0;36m[*]\e[m Performing propability analysis of exploiting vulnerabilities..."
sudo docker scout cves --epss --epss-score 0.2 --output vuln_scan_prob_analysis.txt --exit-code ghcr.io/adi7312/vuln-scan:latest
if [ $? -ne 2 ]; then
    echo -e "\e[0;32m[+]\e[m Probability of found vulnerabilities being exploited is low. Anaylsis completed."
    exit 0
fi
echo -e "\e[0;31m[!]\e[m Probability of found vulnerabilities being exploited is above 20%. Anaylsis completed. Results saved to vuln_scan_prob_analysis.txt."
echo -e "\e[0;36m[*]\e[m Generating SBOM for the image ghcr.io/adi7312/vuln-scan:latest..."
sudo docker sbom ghcr.io/adi7312/vuln-scan:latest --output vuln_scan_image_sbom.txt
