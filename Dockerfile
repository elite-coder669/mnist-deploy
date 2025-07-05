FROM python:3.10-slim

WORKDIR /app

# Install git and system dependencies
RUN apt-get update && \
    apt-get install -y git libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Install Python separately; requirements will be installed after cloning
RUN pip install --upgrade pip

# Expose port
EXPOSE 7860

# Clone and run on container start
CMD bash -c "\
    git clone https://github.com/elite-coder669/mnist-deploy.git /app && \
    cd /app && \
    pip install --no-cache-dir -r requirements.txt && \
    uvicorn app:app --host 0.0.0.0 --port 7860"
