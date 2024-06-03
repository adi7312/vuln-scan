# Automatyzacja skanowania podatności

## Opis projektu

Narzędzie do automatyzacji skanowania i oceniania podatności w sieci lokalnej z wykorzystanem skanera podatności OpenVAS.

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

* `gvm_handler.py` - skrypt obsługujący działanie GVM: uruchamanie skanowania, generowanie raportu, IP urządzeń powinny być pobierane od skanera sieci (`scanner.py`)
* `smtp_handler.py` - skrypt obsługujący wysyłanie raportu PDF do użytkownika końcowego
* `logger.py` - prosty skrypt prowadzący rejestr zdarzeń w trakcie działania aplikacji
* `update.sh` - skrypt aktualizujący: poszczególne komponenenty GVM, system operacyjny, itd.
* `setup_cron.sh` - skrypt uruchamiający harmonogram skanów
* `start.sh` - skrypt uruchamiający kontener z domyślnymi parametrami
* `audit.sh` - skrypt odpowiedzialny za przeprowadzenie audytu bezpieczeństwa obrazu kontenera
* `Dockerfile` - skrypt dockera odpowiedzialny za zbudowanie obrazu kontenera

Zmienne środowiskowe:
* `IP` - IP skanowanej sieci podane wraz z maską (WYMAGANE)
* `EMAIL` - email na który będzie wysyłany raport (WYMAGANE)
* `FREQUENCY` - częstotliwość skanowania, możliwe opcje (WYMAGANE):
  * `1D` - codziennie
  * `1W` - raz w tygodniu
  * `1M` - raz w miesiącu


Narzędzie przeznaczone jest przede wszystkim na platformy z systemem Linux. Narzędzie można uruchomić na systemie Windows, jednak jest to podejście niewspierane, z powodu problemów z skanowaniem sieci lokalnej.

## Uruchomienie przy pomocy skryptu

### Linux

```
git clone https://github.com/adi7312/vuln-scan.git
cd ./vuln-scan
chmod +x start.sh
export IP=<IP>/<MASK>
export EMAIL=<EMAIL>
export FREQUENCY=<FREQ>
./start.sh
```


## Uruchamianie kontenera ręcznie

Pobranie obrazu kontenera:
```
docker pull ghcr.io/adi7312/vuln-scan:latest
```

Normalne uruchomienie (może zająć aż 30/40 minut):
```
docker run --detach --publish 8090:9392 -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

Uruchomienie bez synchronizacji baz zagrożeń (szybsze uruchomienie):

```
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

## Audyt kontenera

Istnieje możliwość przeprowadzenia audytu bezpieczeństwa obrazu pullowanego kontenera przy wywołaniu skryptu `start.sh` poprzez podanie argumentu `--audit-enable`, wówczas `start.sh` wywołuje jeszcze jeden skrypt: `audit.sh`. Audyt można również przeprowadzić w dowolnym czasie poprzez polecenie: `bash audit/audit.sh`.

Rezultatem audytu są pliki: `vuln_scan_image_audit.txt` - lista znalezionych podatności, `vuln_scan_prob_analysis.txt` - podatności których prawdpodobieństwo użycia jest większe niż 20% oraz `vuln_scan_image_sbom.txt` - Software Bill of Materials.




