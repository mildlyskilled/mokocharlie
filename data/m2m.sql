BEGIN;

INSERT INTO common_album_photos (photo_id, album_id)
  SELECT
    i.id AS new_image_id,
    a.id AS new_album_id
  FROM common_photo AS i
    LEFT JOIN image_library AS oi ON oi.image_id = i.image_id
    INNER JOIN album_data AS oa ON oa.album_id = oi.image_album
                                   AND oi.image_album != ''
    INNER JOIN common_album AS a ON a.album_id = oa.album_id;

#fix album covers
UPDATE common_album
SET cover_id = (SELECT
                  id
                FROM common_photo
                WHERE image_id = cover_id);


-- POPULATE HOSPITALITY PIVOT TABLE
INSERT INTO common_hospitality_albums (album_id, hospitality_id)
  SELECT
    (
      (SELECT
         id
       FROM common_album
       WHERE album_id = hospitality_album_lookup.album_id),
      (SELECT
         id
       FROM hospitality)
    );


UPDATE common_photostory
SET album = (SELECT
               album.id
             FROM album
             WHERE album.album_id = story_album);


# Merge user images in
INSERT INTO photo (image_id,
                   name,
                   path,
                   caption,
                   owner,
                   times_viewed,
                   created_at,
                   updated_at,
                   total_rating,
                   times_rated,
                   published
)

  SELECT
    image_id,
    image_name,
    image_path,
    image_caption,
    u.id,
    times_viewed,
    date_added,
    date_added,
    total_rating,
    times_rated,
    published
  FROM user_image_library
    JOIN common_mokouser AS u ON uploader_email = u.email;


# put those photos in an album lookup as well
INSERT INTO photo_album (photo_id, album_id)
  SELECT
    id                                  AS photo_id,
    (SELECT
    id
     FROM album
     WHERE label = 'People and Places') AS album_id
  FROM photo
  WHERE image_id IN (SELECT
                       image_id
                     FROM user_image_library);


# assign image ownership to images so that we can merge user contributed images to the same table
UPDATE `common_photo`
SET owner = (SELECT
               id
             FROM common_mokouser
             WHERE email = "kwakuchintoh@gmail.com");


COMMIT ;

