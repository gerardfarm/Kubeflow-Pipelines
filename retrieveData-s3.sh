# This command works with zipped and non-zipped data
# To download data from s3:
mkdir -p $DATA_DIR/data
aws s3 cp --recursive s3://$S3_BUCKET/$S3_PREFIX/data $DATA_DIR/data

# To upload data to s3
aws s3 cp --recursive $DATA_DIR/data s3://$S3_BUCKET/$S3_PREFIX/data
