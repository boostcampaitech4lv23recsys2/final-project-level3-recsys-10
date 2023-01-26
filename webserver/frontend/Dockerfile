FROM ubuntu:bionic

RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.9-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

COPY . /frontend

WORKDIR /frontend

RUN python3.9 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN pip install -r requirements.txt

CMD ["streamlit", "run","app.py", "--server.port", "80"]
