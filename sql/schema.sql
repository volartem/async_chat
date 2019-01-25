--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Debian 10.6-1.pgdg90+1)
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: chat_db; Type: DATABASE; Schema: -; Owner: chat_user
--

CREATE DATABASE chat_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE chat_db OWNER TO chat_user;

\connect chat_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: chat_user
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    room_id integer
);


ALTER TABLE public.auth_user OWNER TO chat_user;

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: chat_user
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO chat_user;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: chat_user
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: chat_user
--

CREATE TABLE public.message (
    id integer NOT NULL,
    message text NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    author_id integer NOT NULL,
    room_id integer
);


ALTER TABLE public.message OWNER TO chat_user;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: chat_user
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO chat_user;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: chat_user
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- Name: room; Type: TABLE; Schema: public; Owner: chat_user
--

CREATE TABLE public.room (
    id integer NOT NULL,
    name character(1) NOT NULL,
    created timestamp without time zone NOT NULL
);


ALTER TABLE public.room OWNER TO chat_user;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: chat_user
--

CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_id_seq OWNER TO chat_user;

--
-- Name: room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: chat_user
--

ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: message id; Type: DEFAULT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- Name: room id; Type: DEFAULT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: chat_user
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, date_joined, room_id) FROM stdin;
\.


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: chat_user
--

COPY public.message (id, message, "timestamp", author_id, room_id) FROM stdin;
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: chat_user
--

COPY public.room (id, name, created) FROM stdin;
\.


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chat_user
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chat_user
--

SELECT pg_catalog.setval('public.message_id_seq', 1, false);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: chat_user
--

SELECT pg_catalog.setval('public.room_id_seq', 1, false);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: room room_pk; Type: CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pk PRIMARY KEY (id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: chat_user
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username);


--
-- Name: auth_user_username_key; Type: INDEX; Schema: public; Owner: chat_user
--

CREATE UNIQUE INDEX auth_user_username_key ON public.auth_user USING btree (username);


--
-- Name: chat_message_4f331e2f; Type: INDEX; Schema: public; Owner: chat_user
--

CREATE INDEX chat_message_4f331e2f ON public.message USING btree (author_id);


--
-- Name: chat_message_d7e6d55b; Type: INDEX; Schema: public; Owner: chat_user
--

CREATE INDEX chat_message_d7e6d55b ON public.message USING btree ("timestamp");


--
-- Name: room_name_uindex; Type: INDEX; Schema: public; Owner: chat_user
--

CREATE UNIQUE INDEX room_name_uindex ON public.room USING btree (name);


--
-- Name: auth_user auth_user__room_fk; Type: FK CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user__room_fk FOREIGN KEY (room_id) REFERENCES public.room(id) ON UPDATE SET NULL ON DELETE SET NULL;


--
-- Name: message message__room_fk; Type: FK CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message__room_fk FOREIGN KEY (room_id) REFERENCES public.room(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: message message_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chat_user
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.auth_user(id);


--
-- PostgreSQL database dump complete
--

