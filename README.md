# Automatyzacja skanowania podatności

## Opis projektu

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
* `Dockerfile` - skrypt dockera odpowiedzialny za zbudowanie obrazu kontenera

Zmienne środowiskowe:
* `IP` - IP skanowanej sieci podane wraz z maską (WYMAGANE)
* `USERNAME` - login umożliwiający zalogowanie się na GVM (WYMAGANE)
* `PASSWORD` - hasło umożliwiające zalogowanie się na GVM (WYMAGANE)
* `EMAIL` - email na który będzie wysyłany raport (WYMAGANE)
* `FREQUENCY` - częstotliwość skanowania, możliwe opcje (WYMAGANE):
  * `1D` - codziennie
  * `1W` - raz w tygodniu
  * `1M` - raz w miesiącu
* `SENDER_PASS` - app password do maila podmiotu wysyłającego (WYMAGANE)

> Uwaga! O ile można ustawić hasło poprzez zmienne środowiskowe, to zalecane jest aby po pierwszym uruchomieniu, zmienić hasło, ponieważ w historii poleceń (lub w `/proc`) będzie można znaleźć hasło zapisane tekstem jawnym

Narzędzie przeznaczone jest przede wszystkim na platformy z systemem Linux. Narzędzie można uruchomić na systemie Windows, jednak jest to podejście niewspierane, z powodu problemów z skanowaniem sieci lokalnej.

## Uruchomienie przy pomocy skryptu

### Linux

```
git clone https://github.com/adi7312/vuln-scan.git
cd ./vuln-scan
chmod +x start.sh
./start.sh
```

### Windows
```
git clone https://github.com/adi7312/vuln-scan.git
cd .\vuln-scan
.\start.ps1
```

## Uruchamianie kontenera ręcznie

Pobranie obrazu kontenera:
```
docker pull ghcr.io/adi7312/vuln-scan:latest
```

Normalne uruchomienie (może zająć aż 30/40 minut):
```
docker run --detach --publish 8090:9392 -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> -e SENDER_PASS=<SENDER_PASS> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

Uruchomienie bez synchronizacji baz zagrożeń (szybsze uruchomienie):

```
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> -e SENDER_PASS=<SENDER_PASS> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

## Audyt kontenera

Istnieje możliwość przeprowadzenia audytu obrazu pullowanego kontenera przy wywołaniu skryptu `start.sh` poprzez podanie argumentu `--audit-enable`, wówczas `start.sh` wywołuje jeszcze jeden skrypt: `audit.sh`. Audyt można również przeprowadzić w dowolnym czasie poprzez polecenie: `bash audit/audit.sh`.


