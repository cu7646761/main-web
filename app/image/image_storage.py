from google.cloud import storage


def upload_image_gc(bucket_name, image_file):
    # https://storage.googleapis.com/
    # https://storage.googleapis.com/bloganuong_images/D8DC1BEF-96EB-4351-A06B-B3BF88004371.JPG

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Upload file to Google Bucket
    blob = bucket.blob(image_file.filename)
    blob.upload_from_string(image_file.read())

    public_link = blob.public_url
    link = public_link.replace("https://storage.googleapis.com/", "https://storage.googleapis.com/")
    return link


def delete_image_gc(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        return True
    except:
        return False


def get_size(fobj):
    if fobj.content_length:
        return fobj.content_length
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  # seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass
    # in-memory file object that doesn't support seeking or tell
    return 0  # assume small enough
