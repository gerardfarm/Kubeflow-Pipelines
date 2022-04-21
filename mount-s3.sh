# ===========================================================
#               Mounting S3 into your machine
# ===========================================================

# Install package
sudo apt install s3fs

# Configure credientials
echo ACCESS_KEY_ID:SECRET_ACCESS_KEY > ${HOME}/.passwd-s3fs
chmod 600 ${HOME}/.passwd-s3fs

# To mount
s3fs bucket-name /path/to/mountpoint -o passwd_file=${HOME}/.passwd-s3fs

# To un-mount s3
sudo umount /path/to/mountpoint
