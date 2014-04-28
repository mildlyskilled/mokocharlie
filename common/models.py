from __future__ import unicode_literals
import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    album_id = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover = models.ForeignKey('Photo', blank=True, null=True, related_name='cover_photo')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    published = models.BooleanField()
    featured = models.BooleanField(default=False)
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

    def album_images(self):
        return self.photos.count()

    album_images.short_description = "Images in Album"


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=150)
    caption = models.TextField()
    video = models.CharField(max_length=15, blank=True)
    times_viewed = models.IntegerField()
    created_at = models.DateTimeField(verbose_name="Date Uploaded")
    updated_at = models.DateTimeField(verbose_name="Date Modified")
    owner = models.ForeignKey('MokoUser', related_name='photo_owner', db_column='owner')
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    albums = models.ManyToManyField('Album', through='PhotoAlbum', related_name='photo_albums')
    cloud_image = CloudinaryField('image')

    class Meta:
        db_table = 'photo'
        ordering = ('-created_at', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo_view', args=[str(self.id)])

    def get_albums(self):
        return "<br />".join([a.label for a in self.albums.all()])

    @property
    def get_comments(self):
        return Comment.objects.filter(image=self)

    get_albums.short_description = 'Image Appears In'


class Hotel(models.Model):
    HOTEL = 'HOTEL'
    RESORT = 'RESORT'

    HOTEL_TYPE_CHOICES = (
        (HOTEL, 'Hotel'),
        (RESORT, 'Resort')
    )

    id = models.IntegerField(primary_key=True)
    featured = models.BooleanField()
    hospitality_type = models.CharField(max_length=20, choices=HOTEL_TYPE_CHOICES, default=HOTEL)
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    telephone = models.TextField()
    website = models.TextField()
    contact_email = models.EmailField(default="hotelinquiry@mokocharlie.com")
    date_added = models.DateTimeField()
    published = models.BooleanField(default=False)
    albums = models.ManyToManyField('Album', through='HospitalityAlbum', related_name='hotel_album')

    class Meta:
        db_table = 'hospitality'
        ordering = ['-featured', '-date_added']

    def __unicode__(self):
        return self.name

    def get_albums(self):
        return "<br />".join([a.label for a in self.albums.all()])

    get_albums.short_description = 'Album(s)'

    @property
    def all_albums(self):
        return self.albums.all()

    @property
    def get_album(self):
        if len(self.albums.all()) > 0:
            return self.albums.all()[0]

        return None

    def get_absolute_url(self):
        return reverse('hospitality_view', args=[str(self.id)])


class HospitalityAlbum(models.Model):
    id = models.BigIntegerField(primary_key=True)
    hospitality = models.ForeignKey(Hotel)
    album = models.ForeignKey(Album)

    class Meta:
        db_table = 'hospitality_album'


class Comment(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
    image = models.ForeignKey('Photo')
    image_comment = models.TextField()
    comment_author = models.CharField(max_length=150)
    comment_date = models.DateTimeField()
    comment_approved = models.BooleanField()
    comment_reported = models.BooleanField()
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
    published = models.BooleanField()

    class Meta:
        db_table = 'photo_stories'
        ordering = ('-date_added', )
        verbose_name_plural = "Photo Stories"

    def __unicode__(self):
        return self.story_name

    def get_absolute_url(self):
        return reverse('story_view', args=[str(self.story_id)])


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


class VideoLibrary(models.Model):
    video_id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'video_library'
        verbose_name_plural = "Video Library"


class MokoUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class MokoUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MokoUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_photos(self):
        return Photo.objects.filter(owner=self.id)

    def social_accounts(self):
        """ Returns the social accounts the user is authorised with """
        social_accounts = {}
        for social in self.social_auth.all():
            social_accounts[social.provider.replace('-', '_')] = social
        return social_accounts

    @property
    def favourite_photos(self):
        return Photo.favourites.objects.filter(user_id=self.id)

    def __unicode__(self):
        return self.get_full_name()


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MokoUser)
    client_ip = models.CharField(max_length=13, null=True)
    created_at = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'favourite'


class Collections(models.Model):
    name = models.CharField(max_length=25, default='Collection')
    albums = models.ManyToManyField('Album')
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    description = models.TextField(null=True)
    cover_album = models.ForeignKey('Album', related_name='cover_album', null=True)

    def get_albums(self):
        return "<br />".join([a.label for a in self.albums.all()])

    get_albums.short_description = 'Album(s)'
    get_albums.allow_tags = True

    class Meta:
        db_table = 'collection'
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection_view', args=[str(self.id)])


class ClassifiedType(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name


class Classified(models.Model):
    title = models.CharField(max_length=25)
    types = models.ManyToManyField('ClassifiedType')
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    unpublish_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.today()+datetime.timedelta(days=7))
    owner = models.ForeignKey('MokoUser')
    featured = models.BooleanField(default=False)
    contact_email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_contact(self):
        if self.contact_email is None:
            return self.owner.email

        return self.contact_email
