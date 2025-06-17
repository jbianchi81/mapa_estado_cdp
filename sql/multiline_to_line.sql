WITH selection AS (
    SELECT DISTINCT ON (estacion_id)
        estacion_id,
        tramos,
        (dumped.geom)::geometry(LineString, 4326) AS longest_line,
        ST_Length(dumped.geom::geography) AS length_meters
    FROM (
        SELECT 
            estacion_id,
            tramos,
            (ST_Dump(geom)).geom AS geom
        FROM 
            tramos_import
        WHERE 
            GeometryType(geom) = 'MULTILINESTRING'
    ) AS dumped
    ORDER BY estacion_id, ST_Length(dumped.geom::geography) DESC
)
insert into tramos (unid, nombre, geom)
select estacion_id as unid, tramos as nombre, longest_line as geom from selection;