CREATE TABLE public.tramos (
    unid integer NOT NULL,
    nombre character varying,
    out_id integer,
    in_id integer,
    area_id integer,
    longitud real,
    geom public.geometry(LineString,4326),
    rio character varying
);

ALTER TABLE ONLY public.tramos
    ADD CONSTRAINT tramos_unid_key UNIQUE (unid);

ALTER TABLE ONLY public.tramos
    ADD CONSTRAINT tramos_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.areas_pluvio(unid);

ALTER TABLE ONLY public.tramos
    ADD CONSTRAINT tramos_in_id_fkey FOREIGN KEY (in_id) REFERENCES public.estaciones(unid);

ALTER TABLE ONLY public.tramos
    ADD CONSTRAINT tramos_out_id_fkey FOREIGN KEY (out_id) REFERENCES public.estaciones(unid);
