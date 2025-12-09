import os, time, json, requests, boto3, subprocess
from datetime import datetime

SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN")
HEADERS = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}

def load_cfg():
    with open("/data/options.json") as f:
        return json.load(f)

def create_backup():
    name = f"auto_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
    r = requests.post(
        "http://supervisor/supervisor/backups",
        headers=HEADERS,
        json={"name": name}
    )
    r.raise_for_status()
    return r.json()["slug"]

def download_backup(slug, path="/tmp/backup.tar"):
    dl = requests.get(
        f"http://supervisor/supervisor/backups/{slug}/download",
        headers=HEADERS,
        stream=True
    )
    dl.raise_for_status()
    with open(path, "wb") as f:
        for chunk in dl.iter_content(1024 * 64):
            f.write(chunk)
    return path

def encrypt_backup(input_path, password):
    output_path = input_path + ".enc"
    subprocess.run([
        "openssl", "enc", "-aes-256-cbc",
        "-salt", "-pbkdf2",
        "-k", password,
        "-in", input_path,
        "-out", output_path
    ], check=True)
    return output_path

def upload_minio(path, cfg, backup_type):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=cfg["minio_access_key"],
        aws_secret_access_key=cfg["minio_secret_key"],
        endpoint_url=cfg["minio_endpoint"]
    )
    key = f"{backup_type}/backup_{int(time.time())}{os.path.splitext(path)[1]}"
    s3.upload_file(path, cfg["minio_bucket"], key)
    print(f"[OK] Uploaded: {key}")
    cleanup_retention(s3, cfg["minio_bucket"], backup_type, cfg)

def cleanup_retention(s3, bucket, backup_type, cfg):
    prefix = f"{backup_type}/"
    keep = cfg["monthly_to_keep"] if backup_type == "monthly" else cfg["daily_to_keep"]
    objs = s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", [])
    if len(objs) <= keep:
        return
    objs.sort(key=lambda x: x["LastModified"])
    to_delete = objs[:-keep]
    for o in to_delete:
        s3.delete_object(Bucket=bucket, Key=o["Key"])
        print(f"[CLEAN] Deleted old backup: {o['Key']}")

def main():
    cfg = load_cfg()
    backup_type = "monthly" if datetime.now().day == 1 else "daily"

    print("[INFO] Creating backup…")
    slug = create_backup()

    print("[INFO] Downloading backup…")
    path = download_backup(slug)

    # optional encryption
    if cfg.get("encryption_enabled") and cfg.get("encryption_password"):
        print("[INFO] Encrypting with AES-256…")
        path = encrypt_backup(path, cfg["encryption_password"])
    else:
        print("[INFO] Encryption disabled.")

    print("[INFO] Uploading to MinIO…")
    upload_minio(path, cfg, backup_type)

    try:
        os.remove(path)
    except:
        pass

    print("[DONE] Backup process finished.")

if __name__ == "__main__":
    main()
