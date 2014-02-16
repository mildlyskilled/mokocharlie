import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import urllib2
from photos.models import Photo, UserImage


def upload_image(image_path, image_id):
    return cloudinary.uploader.upload(image_path, public_id=image_id)


def batch_upload(image_set="moko"):
    """
    Upload images that are not in the cloudinary bucket there using the images
    from the mokocharlie library. Once an upload is complete write the data to
    the image_library table
    :param image_set: Which table to batch upload from so this could be the
    image library or the user images
    """
    _model = Photo
    if image_set.lower() == "user_images":
        _model = UserImage

    _images = _model.objects.all()
    path = "static/photos"

    for image in _images:
        print "[INFO] Uploading cloud image for {0}/{1}".format(path, image.image_path)
        file_path = os.path.join(path, image.image_path)
        if os.path.exists(file_path):
            try:
                upload_image(file_path, image.image_id)
                print "[INFO] Cloud Image data saved {0}".format(image.image_id)
            except cloudinary.api.Error, e:
                print "[ERROR] Failed to upload image to the cloud {0}".format(str(e))
            except urllib2.URLError, e:
                print "[ERROR] Failed to upload image to the cloud {0}".format(str(e))


def purge_images():
    confirm = raw_input("Are you sure?[y/n] ")
    if confirm.lower() == 'y':
        return cloudinary.api.delete_all_resources()
    else:
        print "Aborting purge operation..."


def resource_list():
    image_list = cloudinary.api.resources();
    return image_list['resources']