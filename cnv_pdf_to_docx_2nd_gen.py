import pdf2docx
from google.cloud import storage
import datetime
import functions_framework

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
    bucket_file_docx_name = str(bucket_file_name.rsplit(".", 1)[0] + ".docx")

    # Access the Storage client
    storage_client = storage.Client()

    # Download the PDF file from the source bucket
    source_blob = storage_client.bucket(bucket_name).blob(bucket_file_name)
    source_blob.download_to_filename(bucket_file_name)

    # Convert PDF to DOCX using pdf2docx
    cv = pdf2docx.Converter(bucket_file_name)
    cv.convert(bucket_file_docx_name)
    cv.close()

    # Save the DOCX file to the destination bucket
    destination_blob = storage_client.bucket(bucket_name).blob(bucket_file_docx_name)
    destination_blob.upload_from_filename(bucket_file_docx_name)

    return f"200: PDF file {bucket_file_docx_name} converted to DOCX and saved to {bucket_name}."