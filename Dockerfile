FROM python:3.8.3-slim
# Make a directory for application
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# Source code
COPY ./app /code/app

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]