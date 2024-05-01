import boto3

s3 = boto3.client('s3')

class S3Service:

    def does_file_exist(self, bucket, key):
        try:
            s3.head_object(Bucket="file-generations", Key=key)
            return True
        except Exception as e:
            return False
        
    def get_file_from_s3(self, bucket, key):
        response = s3.get_object(Bucket="file-generations", Key=key)
        return response['Body'].read()

    def upload_file_to_s3(self, bucket, key, data):
            s3.put_object(Bucket="file-generations", Key=key, Body=data)

    def generate_presigned_url(self, bucket, key, expiration=3600):
        return s3.generate_presigned_url('get_object',
                                      Params={'Bucket': "file-generations", 'Key': key},
                                      ExpiresIn=expiration)
