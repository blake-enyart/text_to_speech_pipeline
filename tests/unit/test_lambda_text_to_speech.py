# WIP For future testing

# import json
# import pytest

# from py_event_mocks import create_event
# from moto import mock_s3, mock_polly
# from lambdas.text_to_speech.main import handler

# @pytest.fixture(scope='function')
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
#     os.environ['AWS_SECURITY_TOKEN'] = 'testing'
#     os.environ['AWS_SESSION_TOKEN'] = 'testing'

# @pytest.fixture(scope='function')
# def s3(aws_credentials):
#     with mock_s3():
#         yield boto3.client('s3', region_name='us-east-1')

# @pytest.fixture(scope='function')
# def polly(aws_credentials):
#     with mock_polly():
#         yield boto3.client('polly', region_name='us-east-1')

# @pytest.fixture
# def s3_create_event():
#     return create_event("aws:s3")

# def test_text_to_speech_processes_event(s3_create_event, s3, polly):
#     assert handler(s3_create_event, None) == "object"
