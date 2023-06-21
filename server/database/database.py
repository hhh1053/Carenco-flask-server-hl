import uuid
from key import *
import boto3

class S3:
    def ImageUploadToS3(self, id):
        s3_obj = self.s3_connection()

        new_name = str(uuid.uuid4()) + '.jpg'
        print(new_name)

        self.s3_put_object(s3_obj, new_name, id)

        image_url = self.s3_get_image_url(new_name)
        return image_url

    def s3_connection(self):
        try:
            s3_obj = boto3.client(
                service_name='s3',
                region_name=REGION,
                aws_access_key_id=ACCESS_KEY_ID,
                aws_secret_access_key=ACCESS_SECRET_KEY

            )
        except Exception as e:
            print(e)
        else:
            print("s3 bucket connected!")
            return s3_obj

    def s3_put_object(self, s3_obj, new_name, id):
        s3_obj.upload_file('./foot_image.jpg'.format(id), BUCKET_NAME, new_name,
                           ExtraArgs={'ContentType': 'image/jpg'})
        return True

    def s3_get_image_url(self, filename):
        image_url = f'https://{BUCKET_NAME}.s3.{LOCATION}.amazonaws.com/{filename}'
        return image_url