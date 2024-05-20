echo "[*] Performing an audit of the image ghcr.io/adi7312/vuln-scan:latest..."
sudo docker scout cves --format only-packages --output vuln_scan_image_audit.txt --exit-code ghcr.io/adi7312/vuln-scan:latest 
if [ $? -ne 0 ]; then
    echo "[+] No vulnerabilities found. Audit completed with 0 vulnerabilities"
    exit 0
fi
echo "[!] Found vulnerabilities. Audit completed. Results saved to vuln_scan_image_audit.txt."
echo "[*] Performing propability analysis of exploiting vulnerabilities..."
sudo docker scout cves --epss --epss-score 0.2 --output vuln_scan_prob_analysis.txt --exit-code ghcr.io/adi7312/vuln-scan:latest
if [ $? -ne 0 ]; then
    echo "[+] Probability of found vulnerabilities being exploited is low. Anaylsis completed."
    exit 0
fi
echo "[!] Probability of found vulnerabilities being exploited is above 20%. Anaylsis completed. Results saved to vuln_scan_prob_analysis.txt."