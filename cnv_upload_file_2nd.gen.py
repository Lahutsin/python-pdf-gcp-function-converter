import functions_framework
import base64

from google.cloud import storage

@functions_framework.http
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    
    bucket_name = request_json["bucket_name"]
    bucket_file_name = request_json["bucket_file_name"]
    bucket_upload_data = request_json["bucket_upload_data"]

    # Create a storage client
    storage_client = storage.Client()

    # Get a reference to the bucket
    bucket = storage_client.bucket(bucket_name)

    # Construct a blob object for the uploaded file
    blob = bucket.blob(bucket_file_name)

    # Decode base64 string
    with open(bucket_file_name, "wb") as f:
        f.write(base64.b64decode(bucket_upload_data))

    # Upload the file content to the Cloud Storage blob
    blob.upload_from_filename(bucket_file_name)   

    return f"200: File {bucket_file_name} uploaded to bucket {bucket_name}."