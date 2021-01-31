import boto3
import json
import io


def handler(event, context):
    # Modify the text file to prepare for upload to S3 bucket
    prefix = '<speak><amazon:domain name="conversational">'
    suffix = "</amazon:domain></speak>"
    newsletter_text_edit = prefix + s3_download_text(event) + suffix

    # Upload text to AWS Polly as task for processing
    client = boto3.client("polly")
    response = client.start_speech_synthesis_task(
        Engine="neural",
        OutputFormat="mp3",
        OutputS3BucketName="tangle-audio-output",
        Text=newsletter_text_edit,
        TextType="ssml",
        VoiceId="Matthew",
    )
    return str(response)


def s3_download_text(event):
    """
    Download S3 text into Lambda memory
    """
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]

    s3 = boto3.resource("s3", region_name="us-east-1")
    bucket = s3.Bucket(bucket_name)

    object_name = event["Records"][0]["s3"]["object"]["key"]
    s3_object = bucket.Object(object_name)

    newsletter_text = io.BytesIO()
    s3_object.download_fileobj(newsletter_text)
    bytes_str = newsletter_text.getvalue()
    return bytes_str.decode("utf-8")
