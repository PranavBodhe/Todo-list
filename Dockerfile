# syntax=docker/dockerfile:1

# Use official Python image
ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-slim as base

# Disable bytecode and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
# Mount pip cache and bind mount requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Copy all project files
COPY . .

# Create non-root user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# 🔑 Give write permission to appuser on /app (including database folders like /app/data or /app/instance)
RUN chown -R appuser:appuser /app && chmod -R u+w /app

# Switch to non-root user
USER appuser

# Expose app port
EXPOSE 9000

# Start the app with gunicorn
CMD gunicorn 'app:app' --bind=0.0.0.0:9000
