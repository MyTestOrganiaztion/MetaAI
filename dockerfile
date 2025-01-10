# Setup base image
FROM python:3.11.9

# Create work directory
ARG WORK_DIR="/src"
ARG LAYER_DIR="/layer"
RUN mkdir ${WORK_DIR} && mkdir ${LAYER_DIR}

# Copy python file
COPY ./src ${WORK_DIR}

# Copy requirements
COPY ./layer/requirements.txt ${LAYER_DIR}/requirements.txt

RUN pip install --no-cache-dir -r ${LAYER_DIR}/requirements.txt

WORKDIR ${WORK_DIR}

# Run fastapi dev
CMD ["fastapi", "dev", "app.py", "--host", "0.0.0.0", "--port", "8000"]