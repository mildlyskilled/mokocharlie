BEGIN;
DROP TABLE IF EXISTS `photo`;

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
DROP TABLE IF EXISTS `album`;
CREATE TABLE IF NOT EXISTS `album` (
  `id`          INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `album_id`    MEDIUMINT(9),
  `label`       VARCHAR(150)     NOT NULL DEFAULT '',
  `description` LONGTEXT,
  `cover`       VARCHAR(15)      NULL DEFAULT NULL,
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
  `cover`,
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


# UPDATE LOOKUPS
INSERT INTO `photo_album` (`photo_id`, `album_id`)
  SELECT
    i.id AS new_photo_id,
    a.id AS new_album_id
  FROM photo AS i
    LEFT JOIN image_library AS oi ON oi.image_id = i.image_id
    LEFT JOIN album_data AS oa ON oa.album_id = oi.image_album AND `oi`.image_album
    LEFT JOIN album AS a ON a.album_id = oa.album_id
  WHERE a.id <> NULL AND i.id <> NULL;

COMMIT;