BEGIN;
# MIGRATE users TO DJANGO USERS

INSERT INTO photos_mokouser (password,
                             last_login,
                             is_superuser,
                             first_name,
                             last_name,
                             email,
                             is_staff,
                             is_active,
                             date_joined)

  SELECT
    user_password,
    NOW(),
    0,
    user_firstname,
    user_lastname,
    user_email,
    0,
    user_active,
    NOW()
  FROM mc_users;

DROP TABLE IF EXISTS mc_users;

# assign image ownership to images so that we can merge user contributed images to the same table
ALTER TABLE `photo`  DROP `owner`;
ALTER TABLE `photo` ADD `owner` INT(11) NOT NULL
AFTER `caption`;
UPDATE `photo`
SET owner = (SELECT
               id
             FROM photos_mokouser
             WHERE email = "kwakuchintoh@gmail.com");
ALTER TABLE `photo` ADD FOREIGN KEY (`owner`) REFERENCES `photos_mokouser` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

# CREATE AN ALBUM FOR public images

INSERT INTO album (label, description, published)
VALUES ('People and Places', "Photos uploaded by various members of the public", 1);
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
    JOIN photos_mokouser AS u ON uploader_email = u.email;

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
COMMIT;