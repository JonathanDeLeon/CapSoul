wget http://docker.cs.wallawalla.edu/public/capsoul-db.tar -P ~/backups/capsoul/
docker volume create --name capsoul-db
docker create -v /code/db --name capsoul-db-restore busybox true
docker run --rm -v ~/backups/capsoul:/backup --mount source=capsoul-db,target=/code/db busybox tar -xvf /backup/capsoul-db.tar
docker rm capsoul-db-restore
