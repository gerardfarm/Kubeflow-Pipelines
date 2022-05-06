import boto3
import docker

import base64

#sudo chmod 666 /var/run/docker.sock

def ecr_login(region, Account_Id, verbose=True):
    ecr = boto3.client('ecr', region_name=region)
    resp = ecr.get_authorization_token(registryIds=[Account_Id,])
    auth_resp = resp['authorizationData'][0]
    token = auth_resp['authorizationToken']
    registry = auth_resp['proxyEndpoint']
    username, password = base64.b64decode(token).decode('utf-8').split(':')

    if verbose:
        print('username: ', username)
        print('password: ', password)
        print('registry: ', registry)

    return username, password, registry


AWS_REGION='us-east-1'                                                                                 
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')


username, password, registry = ecr_login(AWS_REGION, AWS_ACCOUNT_ID)
auth_config = {'username': username, 'password': password}                                              

# get local docker client
dockerClient = docker.from_env() 

regClient = dockerClient.login(username, password, registry=registry)
#print("Login Status: ", regClient.keys())


# build/tag image here....

# then override the docker client config by passing auth_config
# dockerClient.image.push('gfarm', auth_config=auth_config)