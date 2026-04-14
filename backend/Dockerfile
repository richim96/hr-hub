FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Install dependencies (cached layer — only re-runs when lock file changes)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy source
COPY . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
