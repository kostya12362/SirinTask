from django.test import TestCase
from Alias.models import Alias
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import datetime
from Alias.views import GetAlias


class AliasTestCase(TestCase):
    # pacific = pytz.timezone(TIME_ZONE)

    def setUp(self):
        Alias.objects.create(alias='3',
                             target='3',
                             start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
                             end=datetime.datetime(2021, 1, 5, 0, 0, 0, 0))
        Alias.objects.create(alias='4',
                             target='3',
                             start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
                             end=None)

    # Checking when start and end times are the same
    def test_create_alias_start_equal_to_end(self):
        with self.assertRaises(ValidationError):
            enquiry = Alias(start=datetime.datetime(2020, 12, 31, 17, 0, 0, 999999),
                            end=datetime.datetime(2020, 12, 31, 17, 0, 0, 999999))
            enquiry.clean()

    # Check when the start time is greater than the end
    def test_create_alis_start_is_greater_than_end(self):
        with self.assertRaises(ValidationError):
            enquiry = Alias(start=datetime.datetime(2020, 12, 31, 18, 0, 0, 999999),
                            end=datetime.datetime(2020, 12, 31, 17, 0, 0, 999999))
            enquiry.clean()

    # Checking when the beginning of the created one intersects with the existing one enquiry3
    # Check the start of the created is equal to the end of the existing enquiry4
    def test_create_alis_start_is_included(self):
        with self.assertRaises(ValidationError):
            enquiry1 = Alias(alias='3',
                             target='3',
                             start=datetime.datetime(2021, 1, 2, 0, 0, 0, 0, ),
                             end=datetime.datetime(2021, 12, 31, 23, 59, 59, 999999))
            enquiry2 = Alias(alias='3',
                             target='3',
                             start=datetime.datetime(2021, 1, 5, 0, 0, 0, 0),
                             end=datetime.datetime(2021, 12, 31, 23, 59, 59, 999999))
            enquiry1.clean()
            enquiry2.clean()

    # Check start of an existing entry in the created check start enquiry5
    # Checking existing is equal to the end of existing enquiry6
    def test_create_alis_end_is_included(self):
        with self.assertRaises(ValidationError):
            enquiry1 = Alias(alias='3',
                             target='3',
                             start=datetime.datetime(2021, 1, 2, 0, 0, 0, 0),
                             end=datetime.datetime(2021, 1, 1, 0, 0, 0, 1))
            enquiry2 = Alias(alias='3',
                             target='3',
                             start=datetime.datetime(2021, 1, 5, 0, 0, 0, 0),
                             end=datetime.datetime(2021, 1, 1, 0, 0, 0, 0))
            enquiry1.clean()
            enquiry2.clean()

    # Checking the coverage of the existing
    def test_create_alis_covering_the_existing(self):
        with self.assertRaises(ValidationError):
            enquiry = Alias(alias='3',
                            target='3',
                            start=datetime.datetime(2020, 1, 2, 0, 0, 0, 0),
                            end=datetime.datetime(2022, 1, 1, 0, 0, 0, 1))
            enquiry.clean()

    # Checking the coverage of the created
    def test_create_alis_coverage__created(self):
        with self.assertRaises(ValidationError):
            enquiry = Alias(alias='3',
                            target='3',
                            start=datetime.datetime(2021, 1, 3, 0, 0, 0, 0),
                            end=datetime.datetime(2021, 1, 4, 0, 0, 0, 0))
            enquiry.clean()

    # Cheking if "end"= None
    def test_end_None(self):
        with self.assertRaises(IntegrityError):
            enquiry = Alias(alias=None,
                            target=1,
                            start=None,
                            end=datetime.datetime(2021, 1, 4, 0, 0, 0, 0))
            enquiry.save()

    # Check input date time field
    def test_input_date_time(self):
        with self.assertRaises(ValidationError):
            enquiry1 = Alias(alias=None,
                             target=1,
                             start='02-20-2043 01:59:00',
                             end=datetime.datetime(2021, 1, 4, 0, 0, 0, 0))
            enquiry2 = Alias(alias=None,
                             target=1,
                             start='',
                             end=datetime.datetime(2021, 1, 4, 0, 0, 0, 0))
            enquiry1.save()
            enquiry2.save()


class AliasViewsTestCase(TestCase):
    def setUp(self):
        Alias(alias='3',
              target='3',
              start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
              end=datetime.datetime(2021, 1, 5, 0, 0, 0, 0)).save()
        Alias(alias='4',
              target='3',
              start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
              end=datetime.datetime(2021, 1, 5, 0, 0, 0, 0)).save()
        Alias(alias='10',
              target='3',
              start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
              end=datetime.datetime(2021, 1, 5, 0, 0, 0, 0)).save()
        Alias(alias='10',
              target='3',
              start=datetime.datetime(2021, 1, 1, 0, 0, 0, 0),
              end=None).save()
        Alias(alias='10',
              target='3',
              start=datetime.datetime(2030, 1, 1, 0, 0, 0, 0),
              end=datetime.datetime(2034, 1, 1, 0, 0, 0, 0)).save()

    #
    def test_get_alias(self):
        with self.assertRaisesMessage(ValidationError, 'Required argument "target"'):
            GetAlias.get_alias()
            GetAlias.get_alias(target=10)
        self.assertEqual(len(GetAlias.get_alias(target='3')), 4)
        self.assertEqual(len(GetAlias.get_alias(target='3', start='2025-01-01')), 1)
        with self.assertRaises(ValidationError):
            GetAlias.get_alias(target='3', start='01-01')
        self.assertEqual(len(GetAlias.get_alias(target='3', end='2025-01-01')), 3)
        self.assertEqual(len(GetAlias.get_alias(target='3', end='2036-01-01')), 4)
        self.assertEqual(len(GetAlias.get_alias(target='3', end='2034-01-01')), 4)
        self.assertEqual(len(GetAlias.get_alias(target='3', start='2000-01-01', end='2034-01-01')), 4)
        self.assertEqual(len(GetAlias.get_alias(target='3', start='2034-01-01', end='2000-01-01')), 0)
        with self.assertRaises(ValidationError):
            GetAlias.get_alias(target='3', end='fdssdf')

    def test_get_raplace_aliace(self):
        with self.assertRaisesMessage(ValidationError, 'Required argument "alias" and "new_alias_value"'):
            GetAlias.get_raplace_aliace()
            GetAlias.get_raplace_aliace(alias='10')
            GetAlias.get_raplace_aliace(alias='fffff')
            GetAlias.get_raplace_aliace(new_alias_value='10')

        self.assertEquals(len(GetAlias.get_raplace_aliace(alias='10', new_alias_value='44')), 2)
        self.assertEquals(len(GetAlias.get_raplace_aliace(alias='44', new_alias_value='8', start='2003-01-01')), 2)
        self.assertEquals(len(GetAlias.get_raplace_aliace(alias='8', new_alias_value='77',
                                                          end='2070-02-20 1:59:00.33333')), 2)
        with self.assertRaisesMessage(ValidationError, 'Change nothing on this range'):
            GetAlias.get_raplace_aliace(alias='2', new_alias_value='77', end='2070-02-20 1:59:00.33333')
            GetAlias.get_raplace_aliace(alias='77', new_alias_value='74', start='2070-02-20 1:59:00.33333',
                                        end='2003-01-01')
        self.assertEquals(len(GetAlias.get_raplace_aliace(alias='77', new_alias_value='74', start='2003-01-01',
                                                          end='2070-02-20 1:59:00.33333')), 2)
        self.assertEquals(len(GetAlias.get_alais_end_none()), 1)
