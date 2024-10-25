from django.conf import settings
from django.contrib.gis.db import models

User = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    def save(self, *args, full_clean=True, **kwargs):
        if full_clean:
            self.full_clean()
            super().save(*args, **kwargs)

    class Meta(object):
        abstract = True

class Worker(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.PROTECT,
        verbose_name="Related user",
        help_text="User linked to this profile")
    firstname = models.CharField(verbose_name="firstname",blank=True, null=True, max_length=256)
    lastname = models.CharField(verbose_name="lastname",blank=True, null=True, max_length=256)
    permission = models.BooleanField(default=False)

    status_worker = (
        ('null', "Noma'lum"),
        ('0', 'Admin'),
        ('1', 'Leader'),
        ('2', 'HeadLeader'),
    )
    status = models.CharField(verbose_name='Nomalum', default='null', max_length=10, choices=status_worker)

    live_admin = (
        ('0', 'Faol emas'),
        ('1', 'Faol'),
    )


    live = models.CharField(verbose_name='faol', default='0', max_length=10, choices=live_admin)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta(object):
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return self.lastname +' '+ self.firstname

class Certificate(models.Model):
    seria = models.CharField(verbose_name="seria", blank=True, null=True, max_length=256)
    number = models.CharField(verbose_name="number", blank=True, null=True, max_length=256)
    name = models.CharField(verbose_name="name",blank=True, null=True, max_length=256)
    hours = models.CharField(verbose_name="hours",blank=True, null=True, max_length=256)
    teacher = models.CharField(verbose_name="teacher",blank=True, null=True, max_length=256)
    user_firstname = models.CharField(verbose_name="firstname",blank=True, null=True, max_length=256)
    user_lastname = models.CharField(verbose_name="lastname",blank=True, null=True, max_length=256)
    user_fathername = models.CharField(verbose_name="fathername",blank=True, null=True, max_length=256)
    issue_date = models.DateField(blank=True)
    expiry_date = models.DateField(blank=True)
    permission = models.BooleanField(default=False)

    file = models.FileField("Files", upload_to='data/certificates/', blank=True, null=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        if self.number:
            return self.seria + ' - ' + self.number
        else:
            return self.seria

    class Meta:
        verbose_name_plural = "Certificates"