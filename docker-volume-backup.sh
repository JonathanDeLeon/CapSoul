docker run --rm --volumes-from capsoul_backend -v /var/www/static/public/:/backup busybox tar cvf /backup/capsoul-db.tar /code/db
