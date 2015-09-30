from django.core.management.base import BaseCommand, CommandError
from photos.service.cloudinary_service import CloudinaryService


class Command(BaseCommand):
    help = 'Run batch commands on photos for cloudinary services and others'

    def add_arguments(self, parser):
        parser.add_argument('--action')

    def handle(self, *args, **options):
        cs = CloudinaryService()
        if options["action"] == "purge":
            result = cs.purge_images()
            if "deleted" in result:
                count = len(result["deleted"])
                if result["partial"]:
                    self.stdout.write('Successfully deleted "%s"' % count)
                else:
                    self.stdout.write('Successfully purged all photos')

        if options["action"] == "upload":
            cs.batch_upload()
