from django.db import models


class Topic(models.Model):
    display_name = models.CharField(max_length=50)
    internal_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{} <{}>'.format(self.display_name, self.internal_name)


class DiveSite(models.Model):
    display_name = models.CharField(max_length=50)
    url_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{} <{}>'.format(self.display_name, self.full_url)

    @property
    def full_url(self):
        return 'https://{}.com'.format(self.url_name)
