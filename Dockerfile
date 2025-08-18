FROM python:3.13.6-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --upgrade "uv==0.8.5"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

FROM builder AS test

RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

CMD ["pytest"]

FROM python:3.13.6-slim AS production

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "main.py"]