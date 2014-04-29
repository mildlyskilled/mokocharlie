BEGIN;

# USERS
INSERT INTO common_mokouser (password,
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


# PHOTOS - Populate our photo table with old images
INSERT INTO `common_photo` (`image_id`,
                            `name`,
                            `path`,
                            `caption`,
                            `video`,
                            `times_viewed`,
                            `created_at`,
                            `updated_at`,
                            `owner`,
                            `total_rating`,
                            `times_rated`,
                            `published`,
                            `deleted_at`
)
  SELECT
    `image_id`,
    `image_name`,
    `image_path`,
    `image_caption`,
    (SELECT video_id FROM video_library WHERE video_id = `image_video`),
    `times_viewed`,
    `date_added`,
    `date_added`,
    (SELECT cu.id FROM common_mokouser AS cu LEFT JOIN mc_users AS u ON cu.email = u.email  LEFT JOIN image_library AS i ON i.added_by = u.user_id),
    `total_rating`,
    `times_rated`,
    `published`,
    `date_deleted`
  FROM image_library;


# Merge user images in
INSERT INTO common_photo (image_id,
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



# ALBUMS - Populate our new album table with old album data
INSERT INTO `common_album` (
  `album_id`,
  `label`,
  `description`,
  `cover_id`,
  `created_at`,
  `updated_at`,
  `published`
)
  SELECT
    album_id,
    album_label,
    album_description,
    album_cover,
    date_added,
    date_added,
    published
  FROM album_data;

# CREATE AN ALBUM FOR public images

INSERT INTO common_album (label, description, published)
VALUES ('People and Places', "Photos uploaded by various members of the public", 1);

# HOTELS AND RESORTS - Populate hospitality table with old hospitality data
INSERT INTO common_hospitality (
  featured, name, hospitality_type, description, address, telephone, website, date_added, published
)
  SELECT
    featured,
    name,
    hospitality_type,
    description,
    address,
    telephone,
    website,
    date_added,
    published
  FROM hospitality;

# purge comments where we do not have images
DELETE FROM image_comments
WHERE image_id NOT IN (SELECT
                         id
                       FROM common_photo) OR image_id = '';


#COMMENTS
INSERT INTO common_comment (comment_id, image_id, image_comment, comment_author, comment_date, comment_approved)
  SELECT
    comment_id,
    (SELECT
       id
     FROM common_photo
     WHERE image_id = image_comments.image_id),
    image_comment,
    comment_author,
    comment_date,
    comment_approved
  FROM image_comments;


# PHOTO STORIES
INSERT INTO common_photostory (id, `name`, description, album, created_at, published)
  SELECT
    story_id,
    story_name,
    story_description,
    (SELECT id FROM album WHERE album_id = story_album),
    date_added,
    published
  FROM photo_stories;


# PROMOTIONS
INSERT INTO common_promotion (id, promo_handle, promo_type, promo_name, promo_instructions, promo_album, static_image_path, start_date, end_date, featured, published)
  SELECT
    promo_id,
    promo_handle,
    promo_type,
    promo_name,
    promo_instructions,
    promo_album,
    static_image_path,
    start_date,
    end_date,
    featured,
    published
  FROM promotions;


# VIDEOS
INSERT INTO common_video (id, external_id, external_source)
  SELECT
    video_id,
    external_id,
    'YOUTUBE'
  FROM video_library;

COMMIT;