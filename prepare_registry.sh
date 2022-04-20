# Install docker on your pc
sudo pip3 install docker
sudo chmod 666 /var/run/docker.sock

# Configure credentials
aws configure

# To be defined
# REPO_NAME = ''
# AWS_REGION = ''
# AWS_ACCOUNT_ID = ''
# DOCKER_IMAGE_NAME = ''

# Create repo on aws ecr
aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION

# Build a docker image
nano Dockerfile

# add necessary lines to Dockerfile and then build it
sudo docker build -t $DOCKER_IMAGE_NAME .

# login to image -- output should be Login suceeded
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Check image
docker images $DOCKER_IMAGE_NAME

# Check image ID
docker images $DOCKER_IMAGE_NAME --format {{.ID}}

# tag the built image to the created repo -- Image id is the out put of the previous command
docker tag $DOCKER_IMAGE_ID $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

# puhs the image in the repo
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME

# Now you can use your repo for pipelines

# see https://aws.amazon.com/blogs/devops/how-to-use-docker-images-from-a-private-registry-in-aws-codebuild-for-your-build-environment/
