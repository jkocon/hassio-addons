
#!/usr/bin/with-contenv bashio
ACCESS_KEY=$(bashio::config 'access_key')
SECRET_KEY=$(bashio::config 'secret_key')

export MINIO_ROOT_USER=$ACCESS_KEY
export MINIO_ROOT_PASSWORD=$SECRET_KEY

exec minio server /data --console-address ":
