import kfp
import boto3

from typing import NamedTuple


# ================================================================
#                         Upload dataset to S3
# ================================================================
def Preprocessing() -> NamedTuple('My_Output',[('feedback', str)]):
    
    # You should upload your dataset to s3
    
    # import os
    # import boto3

    # conn_s3 = boto3.client('s3', region_name=AWS_REGION)
    
    # # Images names list
    # filenames = os.listdir(data_path)

    # # Upload all images to s3
    # for filename in filenames:
    #     conn_s3.upload_file(os.path.join(data_path, filename), 
    #                         bucket_name, 
    #                         os.path.join(output_path, filename))

    from collections import namedtuple
    feedback_msg = 'Done! Data are on S3.'
    func_output = namedtuple('MyOutput', ['feedback'])
    return func_output(feedback_msg)

# ================================================================
#             Object Detection Evaluation on CoCo dataset
# ================================================================
def test_object_detection(msg, bucket_name, AWS_REGION):

    import os
    import boto3
    import subprocess

    subprocess.call("python3 test.py --data coco128.yaml --weights yolov5s.pt --img 640 --batch-size 2", shell=True)

    print(msg)
    #print(os.listdir('runs/test/exp'))
    
    # Upload results to s3
    conn_s3 = boto3.client('s3', region_name=AWS_REGION)
    output_path = 'runs/test/exp/'

    for filename in os.listdir(output_path):
        path = os.path.join(output_path, filename)
        conn_s3.upload_file(path, bucket_name, os.path.join("object-detection/results/", filename))



# Define registry
AWS_REGION='us-east-1'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

REPO_NAME = 'object-detection'
BUCKET_NAME = 'ali-bucket-gerard'
TAG_NAME = 'latest'
DOCKER_REGISTRY = '{}.dkr.ecr.{}.amazonaws.com/{}:{}'.format(
                                                    AWS_ACCOUNT_ID, 
                                                    AWS_REGION, 
                                                    REPO_NAME,
                                                    TAG_NAME
                                                )

# Create components
preprocess_task = kfp.components.create_component_from_func(Preprocessing, 
                                                    base_image=DOCKER_REGISTRY,
                                                  #  output_component_file = 'preprocessing.yaml'
                                                )

main_task = kfp.components.create_component_from_func(test_object_detection, 
                                                    base_image=DOCKER_REGISTRY,
                                                  #  output_component_file = 'preprocessing.yaml'
                                                )

# Create pipeline
@kfp.dsl.pipeline(
    name='Object Detection Algorithm', 
    description='Testing YOLOv5 on few images.'
)
def object_detection_pipeline(bucket_name: str = BUCKET_NAME,
                                AWS_REGION: str = 'us-east-1'
                                ):

    # Upload your dataset to s3
    first_task = preprocess_task()
    second_task = main_task(first_task.outputs['feedback'], bucket_name, AWS_REGION)

if __name__ == "__main__":
    # execute only if run as a script
    kfp.compiler.Compiler().compile(
        pipeline_func=object_detection_pipeline,
        package_path='full-pipeline-object-detection.yaml')