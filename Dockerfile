FROM python:3.13-slim

WORKDIR /project

# Install uv for dependency management
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv sync

# Expose ports if needed (optional, since docker-compose handles it)
EXPOSE 3000

# Default command (overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
