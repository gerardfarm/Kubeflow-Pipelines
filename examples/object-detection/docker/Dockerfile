FROM ubuntu:20.04

WORKDIR /home

# Install linux packages
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install -y tzdata
RUN apt install -y python3-pip git zip curl htop screen libgl1-mesa-glx libglib2.0-0
RUN alias python=python3

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy scikit-learn pandas boto3
RUN pip install --no-cache -r requirements.txt albumentations gsutil notebook \
    coremltools onnx onnx-simplifier onnxruntime openvino-dev tensorflow-cpu tensorflowjs \
    torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY upsampling.py /usr/local/lib/python3.8/dist-packages/torch/nn/modules/upsampling.py

# RUN apt-get update && apt-get install -y python3-pip
# RUN ln -s /usr/bin/python3
# RUN pip3 install numpy scikit-learn pandas boto3
# RUN pip3 install -r requirements.txt

# RUN apt-get update && apt-get install -y --no-install-recommends \
#         libgl1 \
#         libglib2.0-0 

# RUN apt-get update
# RUN apt-get install -y git

#ARG username=$Ali-Sahili
#ARG password=$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
#RUN git clone https://username:password@github.com:Ali-Sahili/Object_Detection.git
RUN mkdir /home/my_work
#RUN cd /home/my_work
WORKDIR /home/my_work

COPY datasets/ /home/my_work/datasets/

RUN git clone https://github.com/Ali-Sahili/Object_Detection.git

#RUN cd Object_Detection
WORKDIR /home/my_work/Object_Detection