FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# for psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*


RUN pip install uv
COPY pyproject.toml uv.lock README.md ./
RUN uv pip install --system --no-cache .

COPY . .

CMD ["python", "-V"]
