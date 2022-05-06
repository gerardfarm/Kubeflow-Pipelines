import kfp
import boto3


AWS_REGION='region-name'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

REPO_NAME = 'repository-name'
BUCKET_NAME = 'bucket-name'
DOCKER_REGISTRY = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(AWS_ACCOUNT_ID, 
                                                            AWS_REGION, 
                                                            REPO_NAME)

def hello_world(text: str) -> str:
    print(text)
    return text

hello_task = kfp.components.create_component_from_func(hello_world, 
                                                        base_image=DOCKER_REGISTRY) 


@kfp.dsl.pipeline(name='hello-world', description='A simple intro pipeline')
def pipeline_hello_world(text: str = 'hi there'):
    """Pipeline that passes small pipeline parameter string to consumer op."""

    consume_task = hello_task(text)

if __name__ == "__main__":
    # execute only if run as a script
    kfp.compiler.Compiler().compile(
        pipeline_func=pipeline_hello_world,
        package_path='pipeline.yaml')
