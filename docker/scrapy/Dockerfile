FROM python:3.12-slim-bullseye

LABEL author="Arnaud ANDRIANOMANANA"

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ca-certificates \
        curl \
        libxml2-dev \
        libxslt-dev \
		netbase \
		tzdata \
    && pip install --upgrade pip \
    && pip install Scrapy===2.11.0 \
    && pip install scrapy-playwright===0.0.33 \
	; \
	rm -rf /var/lib/apt/lists/*

RUN playwright install chromium

WORKDIR /app

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]