drop database DBturismo;
create database DBturismo;
use  DBturismo;


create table tbCategorias(
cod int primary key auto_increment,
nome varchar(50)
)auto_increment = 1;


Create table tbUsuario(
email varchar(100) primary key,
senha varchar(200)
);

create table tbPontoTuristico(
nome varchar(30) primary key,
categoria int,
latitude double,
longitude double,
criador_ponto varchar(100),
foreign key(criador_ponto) references tbUsuario(email),
foreign key(categoria) references tbCategorias(cod)
);

create table tbImagem_ponto(
cod int PRIMARY KEY auto_increment,
foto BLOB,
nome varchar(30),
email varchar(100),
foreign key (email)references tbUsuario(email),
foreign key (nome) references tbPontoTuristico(nome)
)auto_increment = 1;


create table tbPontoFavoritado(
nome varchar(30),
email varchar(100),
foreign key(nome) references tbPontoTuristico(nome),
foreign key(email) references tbUsuario(email)
);

create table tbComentario(
email varchar(100),
nome varchar(30),
descricao varchar(50),
foreign key (nome) references tbPontoTuristico(nome),
foreign key (email) references tbUsuario(email)

);

create table tbUpvote(
nome varchar(30),
quantidade_upvote int,
foreign key (nome) references tbPontoTuristico(nome)
);

insert into tbCategorias(nome) values ("Parque");
insert into tbCategorias(nome) values ("Museu");
insert into tbCategorias(nome) values ("Teatro");
insert into tbCategorias(nome) values ("Monumento");



insert into tbPontoTuristico(nome,categoria,latitude,longitude,criador_ponto) values ("parque zumbi",1,-25.511144,-49.307653,"johnny_boy");
insert into tbPontoTuristico(nome,categoria,latitude,longitude,criador_ponto) values ("Passeio Público",1,-25.511144,-49.307653,"johnny_boy");
insert into tbPontoTuristico(nome,categoria,latitude,longitude,criador_ponto) values ("parque barigui",1,30,40,"lucas_giovanini");

insert into  tbPontoFavoritado (email,nome) values("lucas_giovanini","parque barigui");

insert into tbComentario (email,nome,descricao) values ("johnny_boy","parque barigui","um parque muito bonito e agradavel");
insert into tbComentario (email,nome,descricao) values ("lucas_giovanini","parque barigui","legal e divertido");

insert into tbUpvote(nome,quantidade_upvote) VALUES ("parque barigui",0);
insert into tbUpvote(nome,quantidade_upvote) VALUES ("parque zumbi",0);

delete from tbUsuario WHERE email = "lucas_giovanini11";



select * from tbUsuario;
select * from tbPontoTuristico;
select * from tbPontoFavoritado;
select * from tbCategorias;
select * from tbComentario;
select*from tbUpvote;
select * from tbImagem_ponto;
select * from tbPontoFavoritado;