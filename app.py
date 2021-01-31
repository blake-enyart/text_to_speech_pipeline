#!/usr/bin/env python3

from aws_cdk import core

from text_to_speech_pipeline.text_to_speech_pipeline_stack import (
    TextToSpeechPipelineStack,
)


app = core.App()
TextToSpeechPipelineStack(app, "text-to-speech-pipeline")

app.synth()
