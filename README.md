# Automatyzacja skanowania podatności

## Stuktura repo

```
/
|---src
|    |
|    |---gvm_handler.py
|    |
|    |---scanner.py
|    
|---config
|    |
|    |---smtp_setup.sh
|    |
|    |---update.sh    
|
|---Dockerfile
```

* `gvm_handler.py` - skrypt obsługujący działanie GVM: uruchamanie skanowania, generowanie raportu, IP urządzeń powinny być pobierane od skanera sieci (`scanner.py`)
* `scanner.py` - skrypt skanujący sieć (TODO: albo piszemy sami taki skaner albo korzystamy z gotowca typu `nmap`,`rustscanner`,`netdiscover`)
* `smtp_setup.sh` - skrypt stawiający serwer SMTP
* `update.sh` - skrypt aktualizujący: poszczególne komponenenty GVM, samo GVM, system operacyjny
* `Dockerfile` - skrypt dockera odpowiedzialny za zbudowanie obrazu kontenera


## Uruchamianie kontenera

Download:
```
docker pull ghcr.io/adi7312/vuln-scan:latest
```

Skopiuj `IMAGE_ID` najnowszego builda.

Zmienne środowiskowe:
* `IP` - IP skanowanej sieci podane wraz z maską (WYMAGANE)
* `USERNAME` - login umożliwiający zalogowanie się na GVM (OPCJONALNE)
* `PASSWORD` - hasło umożliwiające zalogowanie się na GVM (OPCJONALNE)
* `EMAIL` - email na który będzie wysyłany raport (WYMAGANE)
* `FREQUENCY` - częstotliwość skanowania, możliwe opcje (WYMAGANE):
  * `1H` - co godzine
  * `1D` - codziennie
  * `1W` - raz w tygodniu
  * `1M` - raz w miesiącu


> Uwaga! O ile można ustawić hasło poprzez zmienne środowiskowe, to zalecane jest aby po pierwszym uruchomieniu, zmienić hasło, ponieważ w historii poleceń (lub w `/proc`) będzie można znaleźć hasło zapisane tekstem jawnym



Normalne uruchomienie (może zająć aż 30/40 minut):
```
docker run --detach --publish 8090:9392 -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas ghcr.io/adi7312/vuln-scan:latest
```

Uruchomienie bez synchronizacji baz zagrożeń (szybsze uruchomienie):

```
docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=<NETWORK_IP/MASK> -e USERNAME=<USERNAME> -e PASSWORD=<PASSWORD> -e EMAIL=<EMAIL> -e FREQUENCY=<FREQUENCY> --name openvas <IMAGE_ID> 
```



