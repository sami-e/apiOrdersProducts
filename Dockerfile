FROM python:3.7-buster

COPY . /projet-de-session-ocean
WORKDIR projet-de-session-ocean/
RUN pip install --no-cache-dir -r /projet-de-session-ocean/requirements.txt
EXPOSE 5000
ENV REDIS_URL redis://localhost
ENV DB_HOST localhost
ENV DB_USER user
ENV DB_PASSWORD pass
ENV DB_PORT 5432
ENV DB_NAME inf519
CMD FLASK_DEBUG=True FLASK_APP=inf5190 flask run --host=0.0.0.0
