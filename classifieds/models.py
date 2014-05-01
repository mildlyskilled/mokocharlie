from common.models import *


class Job(models.Model):
    title = models.CharField(max_length=25)
    company = models.ForeignKey('Company')
    description = models.TextField()
    salary = models.FloatField()
    requirements = models.ForeignKey('JobRequirement')
    min_education_level = models.CharField(max_length=150)
    work_experience = models.CharField(null=True, max_length=15)
    job_location = models.CharField(null=True, max_length=50)
    contact_detail = models.ForeignKey(ContactDetail)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    remove_date = models.DateTimeField(null=True, blank=True,
                                       default=datetime.datetime.today() + datetime.timedelta(days=7))
    owner = models.ForeignKey(MokoUser)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_contact(self):
        if self.contact_email is None:
            return self.owner.email

        return self.contact_email


class JobRequirement(models.Model):
    title = models.CharField(max_length=150)

    def __unicode__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=150, default="A reputable company")
    website = models.URLField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=150)
    country = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'


def get_featured_classifieds(limit=8):
    Job.objects.filter(published=1).filter(featured=1) \
        .filter(published_date__lte=datetime.datetime.now) \
        .filter(remove_date__gte=datetime.datetime.now)[:limit]