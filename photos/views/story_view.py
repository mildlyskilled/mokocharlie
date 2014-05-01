from django.views.generic.base import TemplateView
from common.models import PhotoStory, Comment, Favourite, Photo
from ipware.ip import get_ip, get_real_ip


class StoryIndexViewTemplate(TemplateView):
    template_name = "story/index.html"

    def get_context_data(self, **kwargs):
        context = super(StoryIndexViewTemplate, self).get_context_data()
        stories = PhotoStory.objects.filter(published=True)
        albums = [a.album for a in stories]
        comments = Comment.objects.filter(image__album__in=albums).filter(comment_approved=1)[:6]
        context['stories'] = stories
        context['comments'] = comments
        return context


class StoryViewTemplate(TemplateView):
    template_name = "story/view.html"
    default_index = 0

    def get_context_data(self, **kwargs):
        context = super(StoryViewTemplate, self).get_context_data()
        story = PhotoStory.objects.get(id=kwargs['story_id'])
        images = story.album.photos.all()
        photo = images[self.default_index]
        if 'image_id' in kwargs:
            photo = Photo.objects.get(id=kwargs['image_id'])

        current = [p for p in images].index(photo)
        next_item = 0
        if current < images.count() - 1:
            next_item = current + 1

        previous_item = images.count() - 1

        if current > 0:
            previous_item = current - 1

        context['story'] = story
        context['image'] = images[current]
        context['comments'] = images[current].get_comments
        context['next_image'] = images[next_item]
        context['previous_image'] = images[previous_item]

        if self.request.user.is_authenticated():
            # get the favourite by user and image id
            context["favourited"] = Favourite.objects.filter(user_id=self.request.user.id).filter(photo=images[current])
        else:
            ip = get_real_ip(self.request) or get_ip(self.request)
            context["favourited"] = Favourite.objects.filter(client_ip=ip).filter(photo=images[current])

        return context