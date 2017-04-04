SET ROLE 'chat_admin';

BEGIN;
--
-- Create model auth_user
--

CREATE TABLE auth_user (
  id serial NOT NULL PRIMARY KEY,
  password CHARACTER VARYING(128) NOT NULL,
  last_login TIMESTAMP WITH TIME ZONE,
  is_superuser BOOLEAN NOT NULL,
  username CHARACTER VARYING(150) NOT NULL,
  first_name CHARACTER VARYING(30) NOT NULL,
  last_name CHARACTER VARYING(30) NOT NULL,
  email CHARACTER VARYING(254) NOT NULL,
  date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE UNIQUE INDEX auth_user_username_key ON auth_user USING BTREE (username);
CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING BTREE (username);


CREATE TABLE message (
  id serial NOT NULL PRIMARY KEY,
  message TEXT NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  author_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES auth_user (id)
  MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX chat_message_d7e6d55b ON message USING BTREE (timestamp);
CREATE INDEX chat_message_4f331e2f ON message USING BTREE (author_id);

COMMIT;