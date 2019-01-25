BEGIN;
--
-- Create model auth_user
--

CREATE TABLE auth_user
(
  id           serial                   NOT NULL PRIMARY KEY,
  password     CHARACTER VARYING(128)   NOT NULL,
  last_login   TIMESTAMP WITH TIME ZONE,
  is_superuser BOOLEAN                  NOT NULL,
  username     CHARACTER VARYING(150)   NOT NULL,
  email        CHARACTER VARYING(254)   NOT NULL,
  date_joined  TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE UNIQUE INDEX auth_user_username_unique_key ON auth_user USING BTREE (username);
CREATE INDEX auth_user_username_index ON auth_user USING BTREE (username);


CREATE TABLE message
(
  id        serial                   NOT NULL PRIMARY KEY,
  message   TEXT                     NOT NULL,
  created   TIMESTAMP WITH TIME ZONE NOT NULL,
  author_id INTEGER                  NOT NULL,
  room_id   INTEGER                  NOT NULL,
  CONSTRAINT message__auth_user_fk FOREIGN KEY (author_id) REFERENCES auth_user (id)
    MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT message__room_fk FOREIGN KEY (room_id) REFERENCES room (id)
    MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX chat_message_created_index ON message USING BTREE (created);
CREATE INDEX chat_message_author_index ON message USING BTREE (author_id);


CREATE TABLE room
(
  id      serial                   NOT NULL PRIMARY KEY,
  name    character(128)           NOT NULL,
  created timestamp WITH TIME ZONE NOT NULL
);
CREATE UNIQUE INDEX room_name_index_unique__key ON room USING BTREE (name);


CREATE TABLE users_to_rooms
(
  user_id integer NOT NULL,
  room_id integer NOT NULL,
  CONSTRAINT users_to_rooms__pk PRIMARY KEY (user_id, room_id),
  CONSTRAINT users_to_rooms__auth_user__fk FOREIGN KEY (user_id) REFERENCES auth_user (id)
    MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT users_to_rooms__room__fk FOREIGN KEY (room_id) REFERENCES room (id)
    MATCH SIMPLE ON UPDATE CASCADE ON DELETE CASCADE
);

COMMIT;