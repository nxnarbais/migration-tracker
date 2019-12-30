FROM python:3-alpine
# FROM python:3

LABEL maintainer="Nicolas Narbais"

RUN pip install flask
RUN pip install datadog
RUN pip install python-dotenv
RUN pip install pytz

COPY ./ /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/app.py"]