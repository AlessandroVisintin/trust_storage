FROM python:3.12-alpine

WORKDIR /src

COPY . .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -e . \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

CMD ["python", "tests/keepalive.py"]