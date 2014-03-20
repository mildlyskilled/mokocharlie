BEGIN;

CREATE TABLE IF NOT EXISTS `photo` (
  `id`           INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `image_id`     VARCHAR(20)      NOT NULL,
  `name`         VARCHAR(250)     NOT NULL DEFAULT '',
  `path`         VARCHAR(150)     NOT NULL DEFAULT '',
  `caption`      MEDIUMTEXT       NOT NULL,
  `video`        VARCHAR(15)      NULL DEFAULT NULL,
  `times_viewed` INT(30)          NOT NULL,
  `created_at`   TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   TIMESTAMP        NOT NULL,
  `owner`        VARCHAR(41)      NOT NULL DEFAULT 'admin',
  `total_rating` BIGINT(20)       NOT NULL DEFAULT '0',
  `times_rated`  MEDIUMINT(9)     NOT NULL DEFAULT '0',
  `published`    TINYINT(1)       NOT NULL DEFAULT '0',
  `deleted_at`   DATETIME         NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

INSERT INTO `photo` (`image_id`,
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
    `image_video`,
    `times_viewed`,
    `date_added`,
    `date_added`,
    `added_by`,
    `total_rating`,
    `times_rated`,
    `published`,
    `date_deleted`
  FROM image_library;


# albums
CREATE TABLE IF NOT EXISTS `album` (
  `id`          INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `album_id`    MEDIUMINT(9),
  `label`       VARCHAR(150)     NOT NULL DEFAULT '',
  `description` LONGTEXT,
  `cover_id`    VARCHAR(15)      NULL DEFAULT NULL,
  `created_at`  TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`  TIMESTAMP        NOT NULL,
  `published`   TINYINT(1)       NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`))
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


INSERT INTO `album` (
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


# Many to many pivot
DROP TABLE IF EXISTS `photo_album`;
CREATE TABLE `photo_album` (
  `id`       INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `photo_id` INT(11) UNSIGNED NOT NULL,
  `album_id` INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`photo_id`) REFERENCES `photo` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  FOREIGN KEY (`album_id`) REFERENCES `album` (`id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

#fix album covers
UPDATE album
SET cover_id = (SELECT
                  id
                FROM photo
                WHERE image_id = cover_id);
ALTER TABLE `album` CHANGE `cover_id` `cover_id` INT(11) UNSIGNED NULL;

ALTER TABLE `album` ADD FOREIGN KEY (`cover_id`) REFERENCES `photo` (`id`)
  ON DELETE SET NULL
  ON UPDATE SET NULL;

#CREATE LOOKUPS

INSERT INTO photo_album (photo_id, album_id)
  SELECT
    i.id AS new_image_id,
    a.id AS new_album_id
  FROM photo AS i
    LEFT JOIN image_library AS oi ON oi.image_id = i.image_id
    INNER JOIN album_data AS oa ON oa.album_id = oi.image_album
                                   AND oi.image_album != ''
    INNER JOIN album AS a ON a.album_id = oa.album_id;

# FIX IMAGE COMMENTS
DELETE FROM image_comments
WHERE image_comments.image_id NOT IN (SELECT
                                        photo.image_id
                                      FROM photo);

UPDATE image_comments
SET image_comments.image_id = (SELECT
                                 id
                               FROM photo
                               WHERE image_comments.image_id = photo.image_id);


DELETE FROM image_comments
WHERE image_id NOT IN (SELECT
                         id
                       FROM photo) OR image_id = '';
ALTER TABLE `image_comments` CHANGE `image_id`  `image_id` INT(11) UNSIGNED NOT NULL;
ALTER TABLE `image_comments` ENGINE = INNODB
DEFAULT CHARACTER SET utf8
COLLATE utf8_general_ci;

ALTER TABLE `image_comments` ADD FOREIGN KEY (`image_id`) REFERENCES `photo` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE `image_comments` CHANGE `comment_report_type`  `comment_report_type` TINYINT(1) NULL DEFAULT '0';
ALTER TABLE `image_comments` CHANGE `comment_reported`  `comment_reported` TINYINT(1) NULL DEFAULT '0';


# UPDATE HOSPITALITY TABLE




ALTER TABLE `hospitality` CHANGE `id`  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT;
ALTER TABLE `hospitality_album_lookup` CHANGE `hospitality_id`  `hospitality_id` INT(11) UNSIGNED NOT NULL;
ALTER TABLE `hospitality_album_lookup` CHANGE `album_id`  `album_id` INT(11) UNSIGNED NOT NULL;

UPDATE hospitality_album_lookup
SET album_id = (SELECT
                  album.id
                FROM album
                WHERE album.album_id = hospitality_album_lookup.album_id);

ALTER TABLE `hospitality_album_lookup` ADD FOREIGN KEY (`hospitality_id`) REFERENCES `hospitality` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
ALTER TABLE `hospitality_album_lookup` ADD FOREIGN KEY (`album_id`) REFERENCES `album` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;


# UPDATE photo story lookup
ALTER TABLE `photo_stories` ENGINE = INNODB;
ALTER TABLE `photo_stories` CHANGE `story_album`  `story_album` INT(11) UNSIGNED NOT NULL;
UPDATE photo_stories
SET story_album = (SELECT
                     album.id
                   FROM album
                   WHERE album.album_id = story_album);

ALTER TABLE `photo_stories` ADD FOREIGN KEY (`story_album`) REFERENCES `album` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;


# Finally user image library
ALTER TABLE user_image_library DROP INDEX image_name;
ALTER TABLE `user_image_library` ENGINE = INNODB;
ALTER TABLE user_image_library DROP PRIMARY KEY;
ALTER TABLE `user_image_library` ADD `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY
FIRST;

# START CLEAN UP

# REMOVE CONNECT table
DROP TABLE IF EXISTS connect;
DROP TABLE IF EXISTS story_comments;
DROP TABLE IF EXISTS taxonomy;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS message_user_lookup;
DROP TABLE IF EXISTS moko_log_data;
DROP TABLE IF EXISTS reported_images;
DROP TABLE IF EXISTS upload_log;
DROP TABLE IF EXISTS album_data;
DROP TABLE IF EXISTS image_library;
DROP TABLE IF EXISTS play_evolutions;

COMMIT;