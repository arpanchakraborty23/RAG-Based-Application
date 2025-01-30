import boto3
import os
import logging
from botocore.exceptions import ClientError

class S3Storage:
    def __init__(self):
        # Load AWS credentials and bucket name
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.bucket = os.getenv("AWS_BUCKET_NAME")

        # Validate environment variables
        if not self.aws_access_key or not self.aws_secret_key or not self.bucket:
            raise ValueError("AWS credentials or bucket name are missing. Check environment variables.")

        # Initialize S3 client
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def upload_file(self,file_obj, filename):
        try:
            self.s3.upload_fileobj(file_obj, self.bucket, filename)
            logging.info(f"File '{filename}' uploaded successfully to S3.")
            return True
        except ClientError as e:
            logging.error(f"Error uploading file to S3: {e}")
            return False
        
    def upload_folder(self, folder_path, s3_folder):
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, folder_path)
                    s3_path = os.path.join(s3_folder, relative_path)

                    with open(local_path, 'rb') as file_obj:
                        self.upload_file(file_obj, s3_path)
                        logging.info(f"Uploaded '{local_path}' to 's3://{self.bucket}/{s3_path}'")
                        print((f"Uploaded '{local_path}' to 's3://{self.bucket}/{s3_path}'"))
        except Exception as e:
            print(e)