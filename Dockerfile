FROM python:3.13-slim

WORKDIR /project

# Install uv
RUN pip install uv

# Copy pyproject.toml, uv.lock, and README.md first for caching and metadata
COPY pyproject.toml uv.lock README.md ./

# Create venv and install deps
RUN uv venv .venv && \
    uv sync --frozen

# Copy rest of code
COPY . .

# Activate venv in entrypoint
ENTRYPOINT ["/bin/bash", "-c", "source .venv/bin/activate && exec \"$@\"", "--"]

# Expose port
EXPOSE 3000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
