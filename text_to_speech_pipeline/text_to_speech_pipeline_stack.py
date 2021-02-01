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

        s3_input_bucket = s3.Bucket(
            self,
            "s3-input-bucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        handler = _lambda.DockerImageFunction(
            self,
            "text-to-speech-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                "lambdas/text_to_speech"
            ),
        )

        # IAM policy to allow access to AWS Polly and KMS for AWS Lambda
        polly_and_kms_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["polly:StartSpeechSynthesisTask", "kms:*"],
        )
        polly_and_kms_statement.add_all_resources()
        handler.add_to_role_policy(polly_and_kms_statement)

        read_write_s3_objects_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:*Object"],
            resources=[
                s3_input_bucket.bucket_arn + "/*",
            ],
        )
        handler.add_to_role_policy(read_write_s3_objects_statement)

        # Solutions Constructs integration for S3 bucket to AWS Lambda
        s3_lambda.S3ToLambda(
            self,
            "s3-lambda-integration",
            existing_lambda_obj=handler,
            existing_bucket_obj=s3_input_bucket,
            s3_event_source_props=lambda_es.S3EventSourceProps(
                events=[s3.EventType.OBJECT_CREATED],
            ),
        )

        # Output bucket for dropping audio files
        s3_output_bucket = s3.Bucket.from_bucket_name(
            self, "s3-output-bucket", bucket_name="tangle-audio-output"
        )
        s3_output_bucket.grant_read_write(handler)

        # Tangle User and IAM access configuration
        iam_user = iam.User(
            self,
            "tangle-user",
            password=core.SecretValue.plain_text("IsaacSaul123"),
            password_reset_required=True,
            user_name="tangle-access",
        )
        iam_group = iam.Group(
            self, "tangle-group", group_name="tangle-access-group"
        )
        iam_group.add_user(iam_user)
        console_access_statement = iam.PolicyStatement(
            actions=[
                "s3:GetAccountPublicAccessBlock",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "s3:GetBucketPolicyStatus",
                "s3:GetBucketPublicAccessBlock",
                "s3:ListAllMyBuckets",
            ],
            resources=["*"],
        )
        s3_output_bucket.grant_read_write(iam_group)
        s3_input_bucket.grant_read_write(iam_group)
        iam_group.add_to_principal_policy(console_access_statement)
