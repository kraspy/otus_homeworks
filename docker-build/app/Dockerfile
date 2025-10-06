FROM astral/uv:python3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync

COPY app .

ENV PATH="/app/.venv/bin:$PATH"

COPY docker-build/app/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]