

""" To run this pipeline, put into your terminal:
        dsl-compile --py utils.py --output pipeline.yaml
"""

def unzip_func(bucket_name, zip_data_path_in_s3='mnist.zip',
                            unzip_data_path_in_s3='dest/',
                            downloaded_data_path_out='data/mnist.zip',
                            unzip_downloaded_data_path='./unzipped_data',
                            AWS_REGION='us-east-1'):
    """ 
    Download zip data from s3, extract and then re-upload it to S3
    Parameters:
        - bucket_name : str, name of the bucket
        - zip_data_path_in_s3: str, complete path of zip data on S3
        - unzip_data_path_in_s3: str, path where you want to extract your data on S3
        - downloaded_data_path_out: str, path where data is downloaded on PC
        - unzip_downloaded_data_path: str, path to extract data
    """

    # It is mandotory to put necessary libraries here
    import os
    import boto3
    import zipfile

    os.makedirs("data", exist_ok=True)
    os.makedirs("unzipped_data", exist_ok=True)

    # Access S3
    conn_s3 = boto3.client('s3', region_name=AWS_REGION)
    s3 = boto3.resource('s3', region_name=AWS_REGION)
    my_bucket = s3.Bucket(bucket_name)

    # Download data on your PC
    obj = my_bucket.Object(zip_data_path_in_s3)
    obj.download_file(Filename=downloaded_data_path_out)
    
    # Unzip downloaded data
    with zipfile.ZipFile(downloaded_data_path_out, 'r') as file:
        file.extractall(unzip_downloaded_data_path)
            
    # Upload unzipped data to your S3 Storage Bucket
    for file in os.listdir(unzip_downloaded_data_path):
        output_path = unzip_data_path_in_s3 + file
        conn_s3.upload_file(os.path.join(unzip_downloaded_data_path, file), bucket_name, output_path)

#unzip_func(bucket_name='ali-bucket-gerard')

import kfp
import boto3

AWS_ACCESS_KEY_ID = 'AKIAXGFLDDSAOLDBHRMK'
AWS_SECRET_ACCESS_KEY = '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'

AWS_REGION='us-east-1'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

REPO_NAME = 'hello-repository'
BUCKET_NAME = 'ali-bucket-gerard'
DOCKER_REGISTRY = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(AWS_ACCOUNT_ID, 
                                                            AWS_REGION, 
                                                            REPO_NAME)

unzip_files_op = kfp.components.create_component_from_func(unzip_func, base_image=DOCKER_REGISTRY) 

@kfp.dsl.pipeline(
    name='testing-s3-in-pipeline',
    description='dowload zip mnist data and re-upload it on s3.'
)
def unzip_and_read_pipeline(BUCKET_NAME='ali-bucket-gerard'):  
    # Call the first OP
    first_task = unzip_files_op(BUCKET_NAME)

if __name__ == "__main__":
    # execute only if run as a script
    kfp.compiler.Compiler().compile(
        pipeline_func=unzip_and_read_pipeline,
        package_path='test-s3-pipeline.yaml')