

""" To run this pipeline, put into your terminal:
        dsl-compile --py utils.py --output pipeline.yaml
"""

def s3_data_handle(bucket_name, data_path_in_s3='data/images',
                            AWS_REGION='us-east-1',
                            ):
    """ 
    Download images data from s3 on your machine
    Parameters:
        - bucket_name : str, name of the bucket
        - data_path_in_s3: str, path of data on S3
    """

    # It is mandotory to put necessary libraries here
    import os
    import boto3
    import tempfile
    import cv2

    #os.makedirs("data", exist_ok=True)
    os.makedirs(data_path_in_s3, exist_ok=True)

    # Access S3
    s3 = boto3.resource('s3', region_name=AWS_REGION) # aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY)
    my_bucket = s3.Bucket(bucket_name)

    for i, object_summary in enumerate(my_bucket.objects.filter(Prefix=data_path_in_s3)):
        print(i, object_summary.key)

        if i==0:
            continue

        obj = my_bucket.Object(object_summary.key)
        #print(obj.key.split('/')[-1])

        tmp = tempfile.NamedTemporaryFile(prefix='img') #, dir='data') #, delete=False)
        #print(tmp.name)
        with open(tmp.name, 'wb') as f:
            obj.download_fileobj(f)
            img = cv2.imread(tmp.name)
            # print(img.shape)
            cv2.imwrite(obj.key, img)
        tmp.close()


import kfp
import boto3


AWS_REGION='region-name'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

REPO_NAME = 'repository-name'
BUCKET_NAME = 'bucket-name'
TAG_NAME = 'latest'
DOCKER_REGISTRY = '{}.dkr.ecr.{}.amazonaws.com/{}:{}'.format(AWS_ACCOUNT_ID, 
                                                            AWS_REGION, 
                                                            REPO_NAME,
                                                            TAG_NAME)

# =============================================================
# First method: Download data in temporary files
# =============================================================
s3_data_handle(bucket_name=BUCKET_NAME)

# =============================================================
# Second method: Directly link dataloader to your dataset on s3
# =============================================================
import _pywrap_s3_io
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms

# list of images
url_list = [f's3://{BUCKET_NAME}/data/images/000000000139.jpg',
            f's3://{BUCKET_NAME}/data/images/000000000285.jpg',
            f's3://{BUCKET_NAME}/data/images/000000000632.jpg',
            f's3://{BUCKET_NAME}/data/images/000000000724.jpg'
            ]

# include all files in images folder
urls = f's3://{BUCKET_NAME}/data/images/0' 


handler = _pywrap_s3_io.S3Init()
print(handler.list_files(url_list[1]))


# ========================================================
#                    Dataloader with S3
# ========================================================

from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import io


class S3BaseClass(object):
    """A base class for defining urls_list for S3Dataset and S3IterableDataset
    """
    def __init__(self, urls_list):
        urls = [urls_list] if isinstance(urls_list, str) else urls_list
        self._urls_list = self.create_urls_list(urls)

    def create_urls_list(self, urls):
        handler = _pywrap_s3_io.S3Init()
        urls_list = list()
        for url in urls:
            if not handler.file_exists(url):
                url_objects = handler.list_files(url)
                assert len(url_objects) != 0, \
                    f"The directory {url} does not contain any objects."
                urls_list.extend(url_objects)
            elif urls_list:
                urls_list.append(url)
            else:
                urls_list = [url]
        return urls_list

    @property
    def urls_list(self):
        return self._urls_list

class S3Dataset(S3BaseClass, Dataset):
    """A mapped-style dataset for objects in s3.
    """
    def __init__(self, urls_list):
        """
        Args:
            urls_list (string or list of strings): the prefix(es) and
                filenames starting with 's3://'. Each string is assumed
                as a filename first. If the file doesn't exist, the string
                is assumed as a prefix.
        """
        S3BaseClass.__init__(self, urls_list)
        # Initialize the handler in the worker since we want each worker to have
        # it's own handler
        self.handler = None

    def __len__(self):
        return len(self.urls_list)

    def __getitem__(self, idx):
        if self.handler == None:
            self.handler = _pywrap_s3_io.S3Init()
        filename = self.urls_list[idx]
        fileobj = self.handler.s3_read(filename)
        return filename, fileobj

class S3ImageSet(S3Dataset):
    def __init__(self, url, transform=None):
        super().__init__(url)
        self.transform = transform

    def __getitem__(self, idx) :
        img_name, img = super(S3ImageSet, self).__getitem__(idx)
        img = Image.open(io.BytesIO(img)).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img

preproc = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    transforms.Resize((100, 100))
])
dataset = S3ImageSet(url_list,transform=preproc)

dataloader = DataLoader(dataset, batch_size=2, num_workers=64)

for i in range(len(dataset)):
    print(dataset[i])