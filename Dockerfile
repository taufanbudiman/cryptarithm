FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy only pyproject.toml first (for better caching)
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system -e .

# Copy the rest of the project
COPY . .

# Run the main application
CMD ["python", "main.py"]