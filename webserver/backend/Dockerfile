FROM ubuntu:bionic

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.8-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

COPY . /backend

WORKDIR /backend

RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install -r requirements.txt

WORKDIR /backend/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


