
# MinIO Add-on for Home Assistant

## 📌 Opis
Ten add-on umożliwia uruchomienie serwera **MinIO** w środowisku Home Assistant Supervisor. MinIO to wysokowydajny serwer obiektowy kompatybilny z Amazon S3, idealny do przechowywania plików i backupów.

---

## ✅ Funkcje
- Hostowanie serwera MinIO w kontenerze Home Assistant.
- Obsługa **persistent storage** w katalogu `/data`.
- Konfiguracja kluczy dostępu z poziomu UI.
- Możliwość integracji z certyfikatami SSL Home Assistant.

---

## 📂 Struktura Add-onu
```
minio/
├── config.json
├── Dockerfile
├── run.sh
└── README.md
```

---

## ⚙️ Instalacja
1. Skopiuj folder `minio` do katalogu `addons/` w Home Assistant.
2. W **Supervisor → Add-on Store** dodaj lokalne repozytorium.
3. Zainstaluj add-on **MinIO Server**.
4. Skonfiguruj opcje w UI:
   - `access_key` – klucz dostępu (domyślnie: `minioadmin`)
   - `secret_key` – sekret (domyślnie: `minioadmin`)
5. Uruchom add-on.

---

## 🔐 Konfiguracja
- Domyślny port: **9000** (API MinIO)
- Konsola administracyjna: **9001**
- Dane przechowywane w `/data` (mapowane na persistent storage Home Assistant).

---

## 🌐 Dostęp
Po uruchomieniu:
- Panel MinIO: `http://<IP_HA>:9001`
- API S3: `http://<IP_HA>:9000`

---

## 🛡️ TLS / SSL
Aby włączyć HTTPS:
- Dodaj mapowanie certyfikatów z Home Assistant (`ssl`).
- Uruchom MinIO z parametrami:
```
--certs-dir /ssl
```

---

## 📖 Dokumentacja
- https://min.io/docs/minio/linux/index.html
- https://developers.home-assistant.io/docs/add-ons/

---

### Autor
Przykładowa integracja
