FROM httpd:alpine

WORKDIR /usr/local/apache2/htdocs

COPY shared/index.html .