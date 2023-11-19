FROM alpine:3.18.4

LABEL author="Arnaud ANDRIANOMANANA"

RUN apk -U add \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        openssl-dev \
        python3-dev \
        py-pip \
        curl \
        ca-certificates \
    && update-ca-certificates \
    && pip install --upgrade pip \
    && pip install Scrapy \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]