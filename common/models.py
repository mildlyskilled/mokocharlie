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
import uuid


class Album(models.Model):
    album_id = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover = models.ForeignKey('Photo', blank=True, null=True, related_name='cover_photo')
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now(), null=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    photos = models.ManyToManyField('Photo')

    class Meta:
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
    image_id = models.CharField(max_length=40, default=uuid.uuid1())
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=150, null=True, blank=True)
    caption = models.TextField()
    video = models.ManyToManyField('Video')
    yt_video = models.CharField(max_length=15, null=True)
    times_viewed = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name="Date Uploaded")
    updated_at = models.DateTimeField(verbose_name="Date Modified")
    owner = models.ForeignKey('MokoUser', related_name='photo_owner', db_column='owner')
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    cloud_image = CloudinaryField(null=True)

    class Meta:
        ordering = ('-created_at', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('photo_view', args=[str(self.id)])

    def get_albums(self):
        return "<br />".join([a.label for a in Album.objects.filter(photos=self.id)])

    @property
    def get_comments(self):
        return Comment.objects.filter(image=self)

    get_albums.short_description = 'Image Appears In'


class Hospitality(models.Model):
    HOTEL = 'HOTEL'
    RESORT = 'RESORT'

    HOTEL_TYPE_CHOICES = (
        (HOTEL, 'Hotel'),
        (RESORT, 'Resort')
    )

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
    albums = models.ManyToManyField('Album')

    class Meta:
        ordering = ['-featured', '-date_added']
        verbose_name_plural = 'Hospitality Provider'
        verbose_name_plural = 'Hospitality Providers'

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


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    image = models.ForeignKey('Photo')
    image_comment = models.TextField()
    comment_author = models.CharField(max_length=150)
    comment_date = models.DateTimeField()
    comment_approved = models.BooleanField()

    class Meta:
        ordering = ('-comment_date',)

    def __unicode__(self):
        return self.image_comment

    def get_absolute_url(self):
        return '/photos/view/{0}/#comment_{1}'.format(self.image.id, self.comment_id)


class PhotoStory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    album = models.ForeignKey(Album)
    created_at = models.DateTimeField(default=timezone.now())
    published = models.BooleanField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name_plural = "Photo Stories"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('story_view', args=[str(self.id)])


class Promotion(models.Model):
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


class Video(models.Model):
    YT = 'YOUTUBE'
    V = 'VIMEO'

    SERVICE_CHOICES = (
        (YT, 'Youtube Video'),
        (V, 'Vimeo Video')
    )
    external_id = models.CharField(max_length=150, blank=True)
    external_source = models.CharField(max_length=25, default=YT)

    def __unicode__(self):
        return "{0} {1}".format(self.external_source, self.external_id)


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


class Collection(models.Model):
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
        verbose_name_plural = _('collections')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection_view', args=[str(self.id)])


class ContactDetail(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    telephone = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)