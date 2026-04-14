SELECT "Creando usuario..." AS "";

CREATE USER IF NOT EXISTS 'USUARIO'@'localhost' IDENTIFIED BY 'CONTRA'; 

SELECT "Creando la base de datos..." AS "";

CREATE DATABASE IF NOT EXISTS recortes;

GRANT ALL PRIVILEGES ON recortes.* to 'USUARIO'@'localhost';

SELECT "Creando tabla" AS "";

USE recortes;

CREATE TABLE IF NOT EXISTS `urls` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `URL_ORG` varchar(512) NOT NULL,
  `MOMENTO` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
);

SELECT "Añadiendo URL de ejemplo (1) => example.com" AS "";


INSERT INTO `urls` (URL_ORG) VALUES ('https://example.com');
