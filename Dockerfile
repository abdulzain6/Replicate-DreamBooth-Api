# Use Python 3.11 slim-buster image as a parent image
FROM python:3.11-slim-buster

# Set environment variables to non-interactive (this prevents some prompts)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
EXPOSE 80

# Command to run the application
CMD ["sh", "-c", "uvicorn api.api:app --host 0.0.0.0 --port ${PORT:-80}"]