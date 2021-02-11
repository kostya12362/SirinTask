from Alias.models import Alias
from django.db.models import Q, Max, Min
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class GetAlias(object):
    @classmethod
    def get_alias(cls, **kwargs):
        cls.target = kwargs.get('target')
        cls.start = kwargs.get('start')
        cls.end = kwargs.get('end')
        if cls.target:
            filter_date = Alias.objects.filter(Q(target__icontains=cls.target)).exclude(end=None)
            if not filter_date:
                raise ValidationError(
                    _('Required argument "target"'),
                    code='invalid',
                    params={'target': cls.target}
                )
            if not cls.start:
                cls.start = filter_date.aggregate(Min('start'))['start__min']
            if not cls.end:
                cls.end = filter_date.aggregate(Max('end'))['end__max']

            return filter_date.filter(Q(start__gte=cls.start) & Q(end__lte=cls.end))
        else:
            raise ValidationError(
                _('Required argument "target"'),
                code='invalid',
                params={'target': cls.target}
            )

    @staticmethod
    def get_raplace_aliace(**kwargs):
        alias = kwargs.get('alias')
        new_alias_value = kwargs.get('new_alias_value')
        start = kwargs.get('start')
        end = kwargs.get('end')
        if not alias or not new_alias_value:
            raise ValidationError(
                _('Required argument "alias" and "new_alias_value"'),
                code='invalid',
            )
        filter_date = Alias.objects.filter(Q(alias=alias)).exclude(end=None)
        if len(filter_date) == 0:
            raise ValidationError(
                _('Change nothing on this range'),
                code='invalid',
            )
        if not start:
            start = filter_date.aggregate(Min('start'))['start__min']
        if not end:
            end = filter_date.aggregate(Max('end'))['end__max']
        for obj in filter_date.filter(Q(start__gte=start) & Q(end__lte=end)):
            obj.alias = new_alias_value
            try:
                obj.save()
                continue
            except ValidationError as error:
                return error
        return Alias.objects.filter(alias=new_alias_value)

    @staticmethod
    def get_alais_end_none():
        return Alias.objects.filter(end=None)
