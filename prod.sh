DOCKER_CONTAINER_NAME=chatbox-nlp-api-gunicorn-container
REPOSITORY_URI=algo-chatbox-nlp-haystack-api
# DEPLOY_DOCKER_COMPOSE_FILE=/home/ec2-user/server/docker-compose.yml

echo "Starting to deploy docker image..."
echo "Stopping previous containers..."
docker ps -q --filter "name=$DOCKER_CONTAINER_NAME" | grep -q . && docker stop $DOCKER_CONTAINER_NAME && docker rm -fv $DOCKER_CONTAINER_NAME
if [[ "$(docker images -q $REPOSITORY_URI:latest 2> /dev/null)" != "" ]]; then
   docker rmi $REPOSITORY_URI:latest
fi

echo "Deploying new docker image..."
git reset --hard
git pull
# aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI
# docker-compose -f $DEPLOY_DOCKER_COMPOSE_FILE up -d
docker build . -t $REPOSITORY_URI:latest
docker run -d --name $DOCKER_CONTAINER_NAME --gpus all -p 8080:8080 $REPOSITORY_URI:latest

echo "Restarting the web server..."
sudo systemctl reload nginx