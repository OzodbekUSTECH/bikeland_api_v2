# pull the official docker image
FROM python:3.13.0a3-slim

# Set the timezone to Asia/Tashkent
ENV TZ=Asia/Tashkent

# set work directory
WORKDIR /project

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update package repositories
RUN apt-get update

# Install curl
RUN apt-get install -y curl

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /etc/nginx/sites-enabled/default

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx and Gunicorn when the container runs
CMD service nginx start && alembic upgrade head && gunicorn -b 0.0.0.0:8000 -w 2 -k uvicorn.workers.UvicornWorker main:app
