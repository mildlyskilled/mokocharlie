from common.models import Photo


def photo_count(request):
    photo_count = len(Photo.objects.filter(published=1))
    return {'photo_count': photo_count}