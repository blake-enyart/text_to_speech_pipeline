import json
import pytest

from aws_cdk import core
from text_to_speech_pipeline.text_to_speech_pipeline_stack import (
    TextToSpeechPipelineStack,
)


def get_template():
    app = core.App()
    TextToSpeechPipelineStack(app, "text-to-speech-pipeline")
    return json.dumps(app.synth().get_stack("text-to-speech-pipeline").template)


def test_sqs_queue_created():
    assert "AWS::SQS::Queue" in get_template()


def test_sns_topic_created():
    assert "AWS::SNS::Topic" in get_template()
