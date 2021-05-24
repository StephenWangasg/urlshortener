CREATE USER 'testuser'@'%' IDENTIFIED BY 'testpassword';
GRANT ALL PRIVILEGES ON *.* TO 'testuser'@'%';

CREATE DATABASE `urlshortener` DEFAULT CHARACTER SET utf8;