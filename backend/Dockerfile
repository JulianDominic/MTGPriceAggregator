FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

WORKDIR /backend
COPY /backend ./

RUN uv venv
RUN uv pip install -r requirements_app.txt

FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /backend
COPY --from=builder /backend /backend
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

EXPOSE 10016
ENTRYPOINT ["uv", "run", "app.py"]
