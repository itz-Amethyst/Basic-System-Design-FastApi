import os.path

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config



# Create the specified bucket on B2
def create_bucket(name, b2, secure=False):
    try:
        b2.create_bucket(Bucket=name)
        if secure:
            # Might be an error here
            b2.prevent_public_access(name, b2)
    except ClientError as ce:
        print('error', ce)


# Delete the specified bucket from B2
def delete_bucket(bucket, b2):
    try:
        b2.Bucket(bucket).delete()
    except ClientError as ce:
        print('error', ce)

# Delete the specified objects from B2
def delete_files(bucket, keys, b2):
    objects = []
    for key in keys:
        objects.append({'Key': key})
    try:
        b2.Bucket(bucket).delete_objects(Delete={'Objects': objects})
    except ClientError as ce:
        print('error', ce)


# List the keys of the objects in the specified bucket
def list_object_keys(bucket, b2):
    try:
        response = b2.Bucket(bucket).objects.all()

        return_list = []               # create empty list
        for object in response:        # iterate over response
            return_list.append(object.key) # for each item in response append object.key to list
        return return_list             # return list of keys from response

    except ClientError as ce:
        print('error', ce)

# Download the specified object from B2 and write to local file system
def download_file(bucket, directory, local_name, key_name, b2):
    file_path = directory + '/' + local_name
    try:
        b2.Bucket(bucket).download_file(key_name, file_path)
    except ClientError as ce:
        print('error', ce)


# Return presigned URL of the object in the specified bucket - Useful for *PRIVATE* buckets
def get_object_presigned_url(bucket, key, expiration_seconds, b2):
    try:
        response = b2.meta.client.generate_presigned_url(ClientMethod='get_object',
        ExpiresIn=expiration_seconds,
        Params={
        'Bucket': bucket,
        'Key': key
        })
        return response

    except ClientError as ce:
        print('error', ce)

# List browsable URLs of the objects in the specified bucket - Useful for *PUBLIC* buckets
def list_objects_browsable_url(bucket, endpoint, b2):
    try:
        bucket_object_keys = list_object_keys(bucket, b2)

        return_list = []                # create empty list
        for key in bucket_object_keys:  # iterate bucket_objects
            url = "%s/%s/%s" % (endpoint, bucket, key) # format and concatenate strings as valid url
            return_list.append(url)     # for each item in bucket_objects append value of 'url' to list
        return return_list              # return list of keys from response

    except ClientError as ce:
        print('error', ce)


# Return a boto3 resource object for B2 service
def get_b2_resource(endpoint, key_id, application_key):
    b2 = boto3.resource(service_name='s3',
                        endpoint_url=endpoint,                # Backblaze endpoint
                        aws_access_key_id=key_id,              # Backblaze keyID
                        aws_secret_access_key=application_key, # Backblaze applicationKey
                        config = Config(
                            signature_version='s3v4',
                    ))
    return b2


# Upload specified file into the specified bucket
def upload_file(bucket, directory, file, b2, b2path=None):
    file_path = os.path.join(directory, file)
    remote_path = b2path
    if remote_path is None:
        remote_path = file
    try:
        response = b2.Bucket(bucket).upload_file(file_path, remote_path)
    except ClientError as ce:
        print('error', ce)

    return response