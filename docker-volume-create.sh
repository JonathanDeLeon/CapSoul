tar -cvf ~/backups/capsoul/db.backup.tar db/
docker volume create --name capsoul-db
docker create -v /code/db --name capsoul-db-restore busybox true
docker run --rm -v ~/backups/capsoul:/backup --mount source=capsoul-db,target=/code/db busybox tar -xvf /backup/db.backup.tar
docker rm capsoul-db-restore
