create database scrable;
use scrable;

create table palabras
(
    id integer unsigned not null primary key auto_increment,
    palabra varchar(100) not null

)
;


create table usuario
(
    id integer unsigned not null primary key  auto_increment,
    usuario varchar(50) not null,
    password varchar(50) not null,
    email varchar(50) not null unique,
    activo tinyint not null default 1

)
;

create table puntuacion
(
    id integer unsigned not null primary key  auto_increment,
    ultima_puntuacion integer unsigned default 0,
    record_puntuacion integer unsigned default 0

)
;

create table palabras as
select palabras_4.palabra
from palabras_4
limit 500

