BEGIN;

ALTER TABLE echonest_response_json
  ADD CONSTRAINT echonest_response_json_fk_echonest_response
  FOREIGN KEY (id)
  REFERENCES echonest_response (id);

COMMIT;
