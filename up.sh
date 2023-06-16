echo "Stopping containers..."
docker stop $(docker ps -q)
echo "Containers stopped!"

echo "Building and starting docker image"

docker-compose --env-file .env up --build --remove-orphans