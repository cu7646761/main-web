# Imports the Google Cloud client library
from google.cloud import storage
from werkzeug.datastructures import FileStorage
import uuid


def upload_image(bucket_name='image-storage-bucket-8419', image_file=None):

    image_ext = image_file.format
    if not image_ext:
        image_ext = "PNG"

    # Instantiates a client
    storage_client = storage.Client()

    # The name for the new bucket
    bucket_name = 'image-storage-bucket-8419'

    # Get created bucket
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(str(uuid.uuid4()))
    blob.content_type = 'image/'+image_ext

    if not image_file:
        return None

    fs = FileStorage()
    # image_file = image_file.convert("RGB")
    image_file.save(fs, format=image_ext)

    fs.seek(0)
    blob.upload_from_file(fs)

    return blob.public_url
