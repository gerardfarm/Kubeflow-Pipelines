import kfp
from kfp.components import create_component_from_func
from typing import NamedTuple
import boto3

AWS_REGION='region-name'
AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')

REPO_NAME = 'repository-name'
BUCKET_NAME = 'bucket-name'
DOCKER_REGISTRY = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(AWS_ACCOUNT_ID, 
                                                            AWS_REGION, 
                                                            REPO_NAME)



def add(a: float, b: float) -> float:
  '''Calculates sum of two arguments'''
  return a + b

def my_divmod(
  dividend: float,
  divisor: float) -> NamedTuple(
    'MyDivmodOutput',
    [
      ('quotient', float),
      ('remainder', float)
    ]):
    '''Divides two numbers and calculate  the quotient and remainder'''

    # Import the numpy package inside the component function
    import numpy as np

    # Define a helper function
    def divmod_helper(dividend, divisor):
        return np.divmod(dividend, divisor)

    (quotient, remainder) = divmod_helper(dividend, divisor)

    from collections import namedtuple
    divmod_output = namedtuple('MyDivmodOutput',
        ['quotient', 'remainder'])
    return divmod_output(quotient, remainder)


add_op = create_component_from_func( add,
                      base_image=DOCKER_REGISTRY,
                      output_component_file='add_component.yaml')


divmod_op = create_component_from_func(my_divmod, 
                      base_image=DOCKER_REGISTRY,
                      output_component_file='div_component.yaml')
