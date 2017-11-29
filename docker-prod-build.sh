docker build -f Dockerfile-prod . --tag capsoul-backend
docker run -P --mount source=capsoul-files,target=/code/files --mount source=capsoul-db,target=/code/db --name capsoul_backend -p 42000:8000 -d capsoul-backend
