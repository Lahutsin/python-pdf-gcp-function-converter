import datetime

from google.cloud import storage
from google.auth import default, compute_engine
from google.auth.transport.requests import Request

def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()

    bucket_name         = request_json['bucket_name']
    bucket_file_name    = request_json['bucket_file_name']
    bucket_access_email = request_json['bucket_access_email']

    try:
        return get_signed_url(bucket_name, bucket_file_name, bucket_access_email)
    except NameError:
        print("Someting wrong!")
        return "500"

def get_signed_url(bucket_name, bucket_file_name, bucket_access_email):
    # Create an authentication request
    auth_request = Request()
    
    # Instantiates a client
    storage_client = storage.Client()

    # Generate blob
    source_blob = storage_client.bucket(bucket_name).blob(bucket_file_name)

    # Generate temporary URL (modify expiration time as needed)
    signing_credentials = compute_engine.IDTokenCredentials(
        auth_request,
        "",
        service_account_email=bucket_access_email
    )
    signed_url = source_blob.generate_signed_url(
        version="v4",
        credentials=signing_credentials,
        method="GET",
        expiration=datetime.timedelta(minutes=5)
    )

    return signed_url