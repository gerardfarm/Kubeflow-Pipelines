# ACCESS S3 
import boto3

verbose = False

# Set REGION for s3 bucket and elastic contaienr registry
AWS_REGION='region-name'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

# Access S3
conn_s3 = boto3.client('s3', region_name=AWS_REGION)

if verbose:  
    print("S3 list of buckets:")
    list_buckets = conn_s3.list_buckets()
    for i, key in enumerate(list_buckets):
        print()
        print(f"Bucket {i} | {key} :")
        print(f"{list_buckets[key]}")
    print("=========================================================")

# My Bucket
bucket_name = 'bucket-name'
contents = conn_s3.list_objects(Bucket=bucket_name)['Contents'] 

print(f"Bucket {bucket_name} Contents:")
for f in contents:
    print(f['Key']) 
print("=========================================================")

# Access ECR
conn_ecr = boto3.client('ecr', region_name=AWS_REGION)
list_repos = conn_ecr.describe_repositories()

if verbose:
    print("ECR repositories:")                                                            
    for i, key in enumerate(list_repos):                                                                  
        print()
        print(f"Repository {i} | {key} :")
        print(f"{list_repos[key]}")
    print("=========================================================")

print("List of my repositories:")
for l in list_repos['repositories']:
    print(f"Name: {l['repositoryName']} | url: {l['repositoryUri']}")
