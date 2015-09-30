import urllib2

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from common.models import Photo
import sys


class CloudinaryService:
    """
    Wrapper class around the cloudinary API for mokocharlie specific
    operations
    """

    def __init__(self):
        pass

    def upload_image(self, image_path, image_id):
        """ Upload an image to cloudinary
        :param image_path: Relative or absolute path to image
        :param image_id: This will be used as the public id for
        reference to the image from cloudinary's CDN
        """
        return cloudinary.uploader.upload(image_path, public_id=image_id)

    def batch_upload(self):
        """
        Upload images that are not in the cloudinary bucket there using the
        images from the mokocharlie library. Once an upload is complete write
        the data to the image_library table
        :param image_set: Which table to batch upload from so this could be the
        image library or the user images
        """
        _images = Photo.objects.all()
        path = "static/photos"

        for image in _images:
            print "[INFO] Uploading cloud image for {0}/{1}".format(path, image.path)
            file_path = os.path.join(path, image.path)
            if os.path.exists(file_path):
                try:
                    if not image.cloud_image:
                        self.upload_image(file_path, image.image_id)
                        image.cloud_image = image.image_id
                        image.save()
                    else:
                        print "[INFO] skipping {0} cloud_image entry {1} exists".format(image.name, image.cloud_image)
                    print "[INFO] Cloud Image data saved {0} {1}".format(image.image_id, image.name)
                except cloudinary.api.Error, e:
                    print "[ERROR] Failed to upload image to the cloud {0}".format(str(e))
                except urllib2.URLError, e:
                    print "[ERROR] Failed to upload image to the cloud {0}".format(str(e))
                except UnicodeEncodeError, e:
                    print "[WARN] encountered an encoding error switching to UTF 8 {0}".format(str(e))
                    reload(sys)
                    sys.setdefaultencoding("utf-8")
                    print "[INFO] Cloud Image data saved {0} {1}".format(image.image_id, image.name)

        print "[INFO] Image upload complete"

    def resource_list(self):
        image_list = cloudinary.api.resources()
        return image_list['resources']

    def purge_images(self):
        confirm = raw_input("Are you sure?[y/n] ")
        if confirm.lower() == 'y':
            return cloudinary.api.delete_all_resources()
        else:
            return "Aborting purge operation..."

    def delete_image(self, public_id):
        return cloudinary.api.delete_resources([public_id])
