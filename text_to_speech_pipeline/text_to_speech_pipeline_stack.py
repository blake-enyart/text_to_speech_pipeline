import os

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_lambda_event_sources as lambda_es,
    aws_iam as iam,
)

from aws_solutions_constructs import aws_s3_lambda as s3_lambda


class TextToSpeechPipelineStack(core.Stack):
    def __init__(
        self, scope: core.Construct, construct_id: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(
            self,
            "test-bucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        handler = _lambda.DockerImageFunction(
            self,
            "test-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                "lambdas/text_to_speech"
            ),
        )

        # IAM policy to allow access to AWS Polly and KMS
        statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW, actions=["polly:SynthesizeSpeech", "kms:*"]
        )
        statement.add_all_resources()
        handler.add_to_role_policy(statement)

        s3_lambda.S3ToLambda(
            self,
            "test-s3-lambda",
            existing_lambda_obj=handler,
            existing_bucket_obj=s3_bucket,
            s3_event_source_props=lambda_es.S3EventSourceProps(
                events=[s3.EventType.OBJECT_CREATED],
            ),
        )

        s3_output_bucket = s3.Bucket.from_bucket_name(
            self, "tangle-audio-output", bucket_name="tangle-audio-output"
        )
        s3_output_bucket.grant_read_write(handler)
