import json
import pytest

from py_event_mocks import create_event
from lambdas.text_to_speech.main import handler


@pytest.fixture
def s3_create_event():
    return create_event("aws:s3")


def test_text_to_speech_processes_event(s3_create_event):
    assert handler(s3_create_event, None) == "object"
