FROM python:3.7

RUN git clone https://github.com/rkern/line_profiler.git
RUN find line_profiler -name '*.pyx' -exec cython {} \;
RUN cd line_profiler && pip install . --user 
RUN cd ..

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY app/* ./
CMD ["python", "/app/app.py"]
