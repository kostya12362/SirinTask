from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class Alias(models.Model):
    alias = models.CharField(max_length=256)
    target = models.SlugField(max_length=24)
    start = models.DateTimeField()
    end = models.DateTimeField(default=None, null=True, blank=True)

    def clean(self):
        try:
            if self.start >= self.end:
                raise ValidationError({
                    'start': ValidationError(_('The start time must be less than the end time')),
                })
            if Alias.objects.filter(alias=self.alias).exclude(end=None):
                for alias in Alias.objects.filter(alias=self.alias).exclude(Q(id=self.id) & Q(end=None)).iterator():
                    if self.start <= alias.start <= alias.end <= self.end:
                        raise ValidationError(
                            _('The range fully covers: %(start)s and %(end)s'),
                            code='invalid',
                            params={'start': alias.start, 'end': alias.end}
                        )
                    elif self.start <= alias.start < self.end:
                        raise ValidationError(
                            _('Range covers the beginning: %(start)s'),
                            code='invalid',
                            params={'start': alias.start}
                        )
                    elif self.start < alias.end <= self.end:
                        raise ValidationError(
                            _('Range covers the end: %(end)s'),

                            params={'end': alias.end}
                        )
                    elif alias.start <= self.start <= self.end <= alias.end:
                        raise ValidationError(
                            _('Range covered end: %(start)s and %(end)s'),
                            code='invalid',
                            params={'start': alias.start, 'end': alias.end}
                        )
        except TypeError:
            return self.end

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)