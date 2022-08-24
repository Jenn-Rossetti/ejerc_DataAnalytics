SELECT date_part('year', CURRENT_DATE) -  date_part('year', TO_DATE(nacimiento,'YYYY-MM-DD')) AS age,
--se divide en nombre y apellido utilizando el _ como condicional
split_part(nombrre, ' ', 1) AS first_name,
split_part(nombrre, ' ', 2) AS last_name,
	--(los nombre de las tablas estaban escritos asi tal cual, tienen algunos errores)
       universidad, 
	   carrerra, 
       fechaiscripccion, 
       sexo, 
       codgoposstal, 
       direccion, 
       eemail 

FROM public.moron_nacional_pampa
WHERE (universidad = 'UNIV. NACIONAL DE LA PAMPA')
-- se comprueba que sean de esas universidades y entre esas fechas.
AND (fechaiscripccion >= '2020-09-01') AND (fechaiscripccion <= '2021-02-01');