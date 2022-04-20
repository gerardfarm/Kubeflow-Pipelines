# =========================================================================
#                       Create Clusters with kubectl
# =========================================================================
# we need to specify cluster name, region, version (default: 1.21) and node-type
export CLUSTER_NAME=<YOUR_CLUSTER_NAME>
export CLUSTER_REGION=<YOUR_CLUSTER_REGION>

# to delete a cluster
kubectl config delete-cluster my-cluster

# see ~/.kube/config

# Create default cluster
eksctl create cluster  # default parameters

# create cluster
eksctl create cluster --name ${CLUSTER_NAME} --version 1.22 --region ${CLUSTER_REGION} --nodegroup-name linux-nodes --node-type  m5.xlarge --nodes 5 --nodes-min 1 --nodes-max 10 --managed
