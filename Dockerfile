FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Use the lock file for exact versions
RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "python", "main.py"]