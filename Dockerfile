# pull the official docker image
FROM python:3.13.0b4

# Set the timezone to Asia/Tashkent
ENV TZ=Asia/Tashkent

# set work directory
WORKDIR /project

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update package repositories
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
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
