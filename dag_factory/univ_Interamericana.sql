SELECT date_part('year', CURRENT_DATE) -  date_part('year', TO_DATE(fechas_nacimiento,'YYYY-MM-DD')) AS age,
--se divide en nombre y apellido utilizando el _ como condicional
split_part(names, ' ', 1) AS first_name,
split_part(names, ' ', 2) AS last_name,
	--(los nombres de las tablas estaban escritos asi tal cual, tienen algunos errores)
       univiersities, 
	carrera, 
       inscription_dates, 
       sexo, 
       localidad, 
       direcciones, 
       email 

FROM public.rio_cuarto_interamericana
WHERE (univiersities = 'UNIV. ABIERTA INTERAMERICANA')
-- se comprueba que sean de esas universidades y entre esas fechas.
AND (inscription_dates >= '2020-09-01') AND (inscription_dates <= '2021-02-01');