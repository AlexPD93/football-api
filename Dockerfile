FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy all code files
COPY . ${LAMBDA_TASK_ROOT}

# Set the handler (matches app/main.py handler)
CMD [ "app.main.handler" ]