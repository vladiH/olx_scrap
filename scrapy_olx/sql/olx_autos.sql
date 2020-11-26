create extension IF NOT EXISTS "uuid-ossp" schema pg_catalog version "1.1"; 
CREATE TABLE IF NOT EXISTS autos (
	auto_id uuid DEFAULT uuid_generate_v4 (),
	marca varchar(60),
	modelo varchar(30),
	anno integer,
	kilometraje varchar(20),
	condicion varchar(30),
	combustible varchar(30),
	color varchar(30),
	transmision varchar(30),
	tipo_vendedor varchar(60),
	precio real check(precio>=0),
	lugar varchar(60),
	dia_publicacion varchar(30),
	imagen varchar(42),
	primary key(auto_id)
)