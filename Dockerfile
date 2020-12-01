FROM python:3.7

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN pip install cython
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y \
    google-cloud-sdk \
    apt-transport-https \ 
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/rkern/line_profiler.git
RUN find line_profiler -name '*.pyx' -exec cython {} \;
RUN cd line_profiler && pip install . --user 
RUN cd ..

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY app/* ./
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["python", "app/app.py"]
