# MinIO Backup Add-on

This add-on automatically creates Home Assistant backups, stores them on a MinIO
(S3-compatible) server, and manages retention for daily and monthly backups.

### Features
- Automatic daily and monthly backups
- Retention control (default: 3 daily, 12 monthly)
- Optional AES-256 encryption
- Upload to MinIO / S3-compatible servers
- Uses Supervisor API for snapshot creation

### Decryption (if encryption is enabled)
openssl enc -d -aes-256-cbc -pbkdf2 -in backup.tar.enc -out backup.tar -k "PASSWORD"

### Configuration options
- `minio_endpoint` – MinIO server URL
- `minio_access_key`
- `minio_secret_key`
- `minio_bucket`
- `daily_to_keep`
- `monthly_to_keep`
- `encryption_enabled` – true/false
- `encryption_password`
