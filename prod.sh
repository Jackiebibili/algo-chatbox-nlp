echo "Starting to deploy docker image..."

AWS_REGION=us-east-2
DOCKER_CONTAINER_NAME=chatbox-nlp-api-gunicorn-container
REPOSITORY_URI=public.ecr.aws/q0s5b2t6/chatbox-nlp-api
DEPLOY_DOCKER_COMPOSE_FILE=/home/ec2-user/server/docker-compose.yml

echo "Stopping previous containers..."
docker ps -q --filter "name=$DOCKER_CONTAINER_NAME" | grep -q . && docker stop $DOCKER_CONTAINER_NAME && docker rm -fv $DOCKER_CONTAINER_NAME
if [[ "$(docker images -q $REPOSITORY_URI:latest 2> /dev/null)" != "" ]]; then
   docker rmi $REPOSITORY_URI:latest
fi

echo "Deploying new docker image..."
# aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI
docker-compose -f $DEPLOY_DOCKER_COMPOSE_FILE up -d

echo "Restarting the web server..."
sudo systemctl reload nginx