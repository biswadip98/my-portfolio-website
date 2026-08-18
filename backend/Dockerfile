# ---------- Stage 1: builder ----------
# This stage installs dependencies into a virtual environment.
# Build tools live here and are NOT carried into the final image.
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and buffering stdout.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an isolated virtual environment for our dependencies.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies first (better layer caching:
# this layer is reused unless requirements.txt changes).
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==24.2 \
    && pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: final runtime ----------
# A clean, minimal image with only the runtime + installed packages.
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Create a non-root user to run the app (security best practice).
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --no-create-home appuser

WORKDIR /app

# Copy the ready-made virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code.
COPY app ./app

# Drop root privileges.
USER appuser

# Document the port the app listens on.
EXPOSE 8000

# Container-level healthcheck hitting our /health endpoint.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the application.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
