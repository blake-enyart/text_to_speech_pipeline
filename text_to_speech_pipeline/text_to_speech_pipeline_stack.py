from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_lambda_event_sources as lambda_es,
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
        )

        s3_lambda.S3ToLambda(
            self,
            "test-s3-lambda",
            lambda_function_props=_lambda.FunctionProps(
                code=_lambda.Code.asset("lambdas"),
                runtime=_lambda.Runtime.PYTHON_3_8,
                handler="main.handler",
            ),
            existing_bucket_obj=s3_bucket,
            s3_event_source_props=lambda_es.S3EventSourceProps(
                events=[s3.EventType.OBJECT_CREATED],
            ),
        )
