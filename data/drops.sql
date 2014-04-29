BEGIN;
# START CLEAN UP
DROP TABLE IF EXISTS mc_users;
DROP TABLE IF EXISTS user_image_library;
DROP TABLE IF EXISTS connect;
DROP TABLE IF EXISTS story_comments;
DROP TABLE IF EXISTS taxonomy;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS message_user_lookup;
DROP TABLE IF EXISTS moko_log_data;
DROP TABLE IF EXISTS reported_images;
DROP TABLE IF EXISTS upload_log;
DROP TABLE IF EXISTS play_evolutions;
DROP TABLE IF EXISTS search_data;
DROP TABLE IF EXISTS image_library;
DROP TABLE IF EXISTS album_data;
COMMIT;