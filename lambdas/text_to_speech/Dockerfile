FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY main.py ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.handler" ]
