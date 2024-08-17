#! /bin/bash
set -e

DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME}"
DOCKER_HUB_PASSWORD="${DOCKER_HUB_PASSWORD}"
REMOTE_DOCKER_HUB_REPO="${REMOTE_DOCKER_HUB_REPO}"
DB_CONNECTION_URL="${DB_CONNECTION_URL}"
PORT=8001
HOST="0.0.0.0"
LOCAL_DOCKER_IMAGE_TAG="db-fastapi"
TAG="latest"

echo "Trying to login to dockerhub..."
echo "$DOCKER_HUB_PASSWORD" | docker login -u $DOCKER_HUB_USERNAME --password-stdin
echo "Logged in to dockerhub"

echo "Building image"
docker build -t $LOCAL_DOCKER_IMAGE_TAG .. \
    --build-arg="HOST=$HOST" \
    --build-arg="PORT=$PORT" \
    --build-arg="DB_CONNECTION_URL=$DB_CONNECTION_URL"

echo "Tagging Local Image to Remote"
docker tag $LOCAL_DOCKER_IMAGE_TAG $REMOTE_DOCKER_HUB_REPO

echo "publishing to dockerhub"
docker push $REMOTE_DOCKER_HUB_REPO:$TAG

echo "Done"