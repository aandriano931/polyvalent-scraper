FROM python:3.10.6-slim-bullseye

LABEL author="Arnaud ANDRIANOMANANA"
LABEL org.opencontainers.image.source=https://github.com/aandriano931/polyvalent-scraper
LABEL org.opencontainers.image.description="Python image for scraping and llm"

COPY requirements.txt ./

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ca-certificates \
        curl \
		iputils-ping \
        libxml2-dev \
        libxslt-dev \
		netbase \
		tzdata \
    && pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	; \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]