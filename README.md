
# Welcome to the Text-to-Speech Pipeline project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`text_to_speech_pipeline_stack`)
which contains an Amazon S3 bucket that triggers an AWS Lambda to send `.txt` style content to AWS Polly for conversion to `.mp3` that is landed in another S3 bucket.

## Reference Architecture
<p align="center">
    <img src=static/images/Reference%20Architectures%20-%20Text-to-Speech%20Pipeline%20-%20Architecture.jpg  width="300" height="300" alt="Reference Architecture">
</p>

## Instructions for Usage
* To upload content, you must be logged into AWS through the console which can be done [here][aws-console]

* Once logged in, you can access the S3 bucket for uploading `.txt` files from [here][s3-input-bucket] and `Upload` the file.

* After the `.txt` file has been uploaded, the Lambda function will automagically pickup the file and upload it to AWS Polly which will then output the `.mp3` file to another S3 bucket seen [here][s3-output-bucket].

## Project Overview

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To setup this project, manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
$ poetry install
```
Configure pre-commit hooks prior to development:
```
$ inv install-hooks
```
Note: this workflow will now looks something like:
* `git add <file>`
* `git commit`
* `git add .` -- if there are code corrections
* `git cz` -- to make a descriptive commit to the repo

At this point you can now synthesize the CloudFormation template for this code.

```
$ inv synth
```

You can now begin exploring the source code, contained in the text_to_speech directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just run the `poetry add <library>`
command.

## Useful commands

 * `inv ls`          list all stacks in the app
 * `inv synth`       emits the synthesized CloudFormation template
 * `inv deploy`      deploy this stack to your default AWS account/region
 * `inv diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

[aws-console]: https://us-east-1.signin.aws.amazon.com/oauth?SignatureVersion=4&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJMOATPLHVSJ563XQ&X-Amz-Date=2021-01-12T00%3A05%3A11.345Z&X-Amz-Signature=1920433fc369ab91254fbb511f7c8f527c4b81071306397f7297641622807f3c&X-Amz-SignedHeaders=host&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fhomepage&code_challenge=-0knKPwL3IU1WyWO1DiPbxS7WuUBHhIxFRcmYoOciNI&code_challenge_method=SHA-256&redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue&response_type=code&state=hashArgs%23
[s3-input-bucket]: https://s3.console.aws.amazon.com/s3/buckets/text-to-speech-pipeline-s3inputbucket5b674094-1j7kl0t3tprdz
[s3-output-bucket]: https://s3.console.aws.amazon.com/s3/buckets/tangle-audio-output
