FROM php:7.4-apache

WORKDIR /var/www/html

COPY index.php .

COPY main.py .
