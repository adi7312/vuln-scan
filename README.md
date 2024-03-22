# Automatyzacja skanowania podatności

## Stuktura repo

```
/
|---src
|    |
|    |---gvm_handler.py
|    |
|    |---scanner.py
|    |
|    |---smtp_handler.py
|
|---Dockerfile
```

* `gvm_handler.py` - skrypt obsługujący działanie Openvasa: uruchamanie skanowania, generowanie raportu, IP urządzeń powinny być pobierane od skanera sieci (`scanner.py`)
* `scanner.py` - skrypt skanujący sieć (TODO: albo piszemy sami taki skaner albo korzystamy z gotowca typu `nmap`,`rustscanner`,`netdiscover`)
* `smtp_handler.py` - skrypt obsługujący wysyłanie raportów poprzez email
* `Dockerfile` - skrypt służący do budowania obrazu kontenera

## Uruchamianie

Build:

```
docker build .
```

Run:

Skopiuj `IMAGE ID` korzystając z polecenia `docker image ls`.

```
docker run -d -p 443:443 --name openvas <IMAGE_ID>
```
