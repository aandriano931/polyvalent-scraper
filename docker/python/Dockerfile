FROM python:3.12-slim-bullseye

LABEL author="Arnaud ANDRIANOMANANA"

COPY requirements.txt ./

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
	&& pip install --no-cache-dir -r requirements.txt \
	; \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]