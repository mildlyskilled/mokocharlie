BEGIN;

INSERT INTO common_photo_albums (photo_id, album_id)
  SELECT
    i.id AS new_image_id,
    a.id AS new_album_id
  FROM common_photo AS i
    LEFT JOIN image_library AS oi ON oi.image_id = i.image_id
    INNER JOIN album_data AS oa ON oa.album_id = oi.image_album
                                   AND oi.image_album != ''
    INNER JOIN common_album AS a ON a.album_id = oa.album_id;


-- POPULATE HOSPITALITY PIVOT TABLE
INSERT INTO common_hospitality_albums (album_id, hospitality_id)
  SELECT
    (SELECT id FROM common_album WHERE album_id = hospitality_album_lookup.album_id) AS album_id,
    hospitality_id FROM hospitality_album_lookup;


# put those photos in an album lookup as well
INSERT INTO common_photo_albums (photo_id, album_id)
  SELECT
    id                                  AS photo_id,
    (SELECT
    id
     FROM common_album
     WHERE label = 'People and Places') AS album_id
  FROM common_photo
  WHERE image_id IN (SELECT
                       image_id
                     FROM user_image_library);


INSERT INTO common_photo_video(photo_id, video_id)
  SELECT p.id, v.id FROM common_video AS v
    JOIN common_photo AS p ON p.yt_video = v.external_id;

COMMIT ;

