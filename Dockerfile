FROM httpd:alpine

WORKDIR /usr/local/apache2/htdocs

COPY index.html .

COPY main.py .
