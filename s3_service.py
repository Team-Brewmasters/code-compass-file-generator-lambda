import boto3

s3 = boto3.client('s3')

class S3Service:

    def upload_file_to_s3(self, bucket, key, data):
            s3.put_object(Bucket=bucket, Key=key, Body=data)

    def generate_presigned_url(self, bucket, key, expiration=3600):
        return s3.generate_presigned_url('get_object',
                                      Params={'Bucket': bucket, 'Key': key},
                                      ExpiresIn=expiration)
