BEGIN;
-- Move hotel_album lookups AND DELETE old TABLE

ALTER TABLE hospitality_albums ADD FOREIGN KEY (hospitality_id) REFERENCES hospitality (id)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE hospitality_albums ADD FOREIGN KEY (album_id) REFERENCES album (id)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

INSERT INTO hospitality_albums (album_id, hospitality_id)
  SELECT
    album_id,
    hospitality_id
  FROM hospitality_album_lookup;

COMMIT;