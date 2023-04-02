FROM python:3.11-bullseye

WORKDIR /app

## Prepare NGINX
RUN apt update
RUN apt install -y nginx

## Prepare Python environment
RUN wget -O - https://install.python-poetry.org | python3 -

ENV HOME "/root"
ENV PATH "$HOME/.local/bin:$PATH"

COPY ./server/pyproject.toml ./
COPY ./server/poetry.lock ./
RUN poetry install --no-root --without dev

## Start copying code
COPY nginx/nginx.conf /etc/nginx/
COPY deployment/entrypoint.sh ./
COPY web-ui/dist web-ui/

COPY ./server ./

RUN poetry install --only-root

ENTRYPOINT ["./entrypoint.sh"]