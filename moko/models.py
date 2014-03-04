# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth import login, authenticate

class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    album_id = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover = models.ForeignKey('Photo', blank=True, null=True, related_name='cover_photo')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    published = models.IntegerField()
    photos = models.ManyToManyField('Photo', through='PhotoAlbum')

    class Meta:
        db_table = 'album'
        ordering = ('-created_at', )

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('album_view', args=[str(self.id)])

    @property
    def album_cover(self):
        if self.cover:
            return self.cover

        return self.photos.order_by('?')[0]



class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=150)
    caption = models.TextField()
    video = models.CharField(max_length=15, blank=True)
    times_viewed = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.CharField(max_length=41)
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    albums = models.ManyToManyField('Album', through='PhotoAlbum', related_name='photo_albums')

    class Meta:
        db_table = 'photo'
        ordering = ('-created_at', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('photo_view', args=[str(self.id)])



class AppData(models.Model):
    id = models.IntegerField(primary_key=True)
    app_name = models.TextField()
    app_description = models.TextField()
    app_key = models.TextField()
    date_created = models.DateTimeField()
    created_by = models.CharField(max_length=41)
    enabled = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    deleted_by = models.CharField(max_length=41, blank=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_data'


class AppProperties(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.ForeignKey(AppData)
    definition = models.ForeignKey('AppPropertyDefinitions')
    property_data = models.TextField()

    class Meta:
        db_table = 'app_properties'


class AppPropertyDefinitions(models.Model):
    id = models.IntegerField(primary_key=True)
    prop_handle = models.CharField(max_length=150)
    prop_name = models.CharField(max_length=250)
    prop_type = models.CharField(max_length=150)
    prop_required = models.IntegerField()
    prop_protected = models.IntegerField()

    class Meta:
        db_table = 'app_property_definitions'


class Hotel(models.Model):
    id = models.IntegerField(primary_key=True)
    featured = models.IntegerField()
    hospitality_type = models.CharField(max_length=20)
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    telephone = models.TextField()
    website = models.TextField()
    date_added = models.DateTimeField()
    published = models.IntegerField()

    class Meta:
        db_table = 'hospitality'

    def __unicode__(self):
        return self.name


class HospitalityAlbumLookup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    hospitality = models.ForeignKey(Hotel)
    album = models.ForeignKey(Album)

    class Meta:
        db_table = 'hospitality_album_lookup'


class Comment(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
    image = models.ForeignKey('Photo')
    image_comment = models.TextField()
    comment_author = models.CharField(max_length=150)
    comment_date = models.DateTimeField()
    comment_approved = models.IntegerField()
    comment_reported = models.IntegerField()
    comment_report_type = models.IntegerField()
    report_comments = models.TextField(blank=True)

    class Meta:
        db_table = 'image_comments'
        ordering = ('-comment_date',)

    def __unicode__(self):
        return self.image_comment

    def get_absolute_url(self):
        return '/photos/view/{0}/#comment_{1}'.format(self.image.id, self.comment_id)


class PhotoAlbum(models.Model):
    id = models.IntegerField(primary_key=True)
    photo = models.ForeignKey(Photo)
    album = models.ForeignKey(Album)

    class Meta:
        managed = False
        db_table = 'photo_album'


class PhotoStory(models.Model):
    story_id = models.IntegerField(primary_key=True)
    story_name = models.CharField(max_length=150)
    story_description = models.TextField()
    story_album = models.ForeignKey(Album, db_column='story_album')
    date_added = models.DateTimeField()
    published = models.IntegerField()

    class Meta:
        db_table = 'photo_stories'
        ordering = ('-date_added', )
        verbose_name_plural = "Photo Stories"

    def __unicode__(self):
        return self.story_name

    def get_absolute_url(self):
        #TODO: use reverse url lookup for this
        return "/stories/view/{0}".format(self.story_id)


class Promotion(models.Model):
    promo_id = models.IntegerField(primary_key=True)
    promo_handle = models.CharField(max_length=50, blank=True)
    promo_type = models.CharField(max_length=20)
    promo_name = models.CharField(max_length=150)
    promo_instructions = models.TextField()
    promo_album = models.IntegerField(blank=True, null=True)
    static_image_path = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    featured = models.IntegerField()
    published = models.IntegerField()

    class Meta:
        db_table = 'promotions'


class SearchData(models.Model):
    search_id = models.CharField(primary_key=True, max_length=15)
    keywords = models.TextField()
    searcher_ip_address = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'search_data'
        verbose_name_plural = "Search Data"


class UserPhoto(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=15)
    image_name = models.CharField(max_length=250)
    image_path = models.CharField(max_length=150)
    image_album = models.CharField(max_length=150)
    image_caption = models.TextField()
    image_source = models.CharField(max_length=11)
    times_viewed = models.IntegerField()
    date_added = models.DateTimeField()
    image_uploader = models.CharField(max_length=150)
    uploader_email = models.CharField(max_length=150)
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.IntegerField()

    class Meta:
        db_table = 'user_image_library'


class VideoLibrary(models.Model):
    video_id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'video_library'
        verbose_name_plural = "Video Library"


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """ Creates and saves a User with the given email and password.  """
        now = timezone.now()
        user = self.model(username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username,  password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Custom user model extendable to include any additional data we want
    to collect about a user.

    """
    username = models.CharField(_('username'), max_length=245, unique=True)
    email = models.EmailField(_('email address'), max_length=254, blank=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    first_name = models.CharField(_('first name'), max_length=60, blank=True)
    last_name = models.CharField(_('last name'), max_length=60, blank=True)
    job_title = models.CharField(_('job title'), max_length=254, blank=True)

    activation_key = models.CharField(_('activation key'), max_length=254, blank=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user."""
        return self.first_name

    def social_accounts(self):
        """ Returns the social accounts the user is authorised with """
        social_accounts = {}
        for social in self.social_auth.all():
            social_accounts[social.provider.replace('-', '_')] = social
        return social_accounts

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())
        super(CustomUser, self).save(*args, **kwargs)
        if not self.openid_set.exists():
            self.openid_set.create()

    def email_user(self, subject, message, from_email=None):
        """ Sends an email to this User.  """
        send_mail(subject, message, from_email, [self.email])

    def login(self, request):
        """ Login as this User. """
        self.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, self)

    def send_activation_email(self):
        self.activated = False
        domain = Site.objects.get_current().domain
        context = {
            'activation_key': self.activation_key,
            'first_name': self.first_name,
            'domain': domain,
        }
        subject = render_to_string(
            'emails/activation_email_subject.txt', context
        )
        subject = ''.join(subject.splitlines())
        body = render_to_string(
            'emails/activation_email_body.txt', context
        )
        self.email_user(subject, body, settings.EMAIL_FROM)

    @property
    def activated(self):
        if self.activation_key == "ACTIVATED":
            return True
        return False

    @activated.setter
    def activated(self, value):
        if value:
            self.activation_key = "ACTIVATED"
        else:
            self.activation_key = str(uuid.uuid4())
        self.save()