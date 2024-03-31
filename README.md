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
```

* `gvm_handler.py` - skrypt obsługujący działanie GVM: uruchamanie skanowania, generowanie raportu, IP urządzeń powinny być pobierane od skanera sieci (`scanner.py`)
* `scanner.py` - skrypt skanujący sieć (TODO: albo piszemy sami taki skaner albo korzystamy z gotowca typu `nmap`,`rustscanner`,`netdiscover`)
* `smtp_setup.sh` - skrypt stawiający serwer SMTP
* `update.sh` - skrypt aktualizujący: poszczególne komponenenty GVM, samo GVM, system operacyjny





