# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

from django.db import models
from django.contrib.auth.models import User


AGE_GROUP_CHOICES = (
    ('1', 'Preschool'),
    ('2', 'Kindergarten'),
    ('3', 'Elementary'),
    ('4', 'Middle School'),
    ('5', 'High School'),
    ('6', 'Young Adult'),
    ('7', 'Adult'),
    ('8', 'Senior'),
)

AUTHORITY_CHOICES = (
    ('1', 'Client'),
    ('2', 'Administrator'),
    ('3', 'Maintainer'),
)

GENDER_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male'),
)

TITLE_CHOICES = (
    ('M', 'Mr.'),
    ('R', 'Mrs.'),
    ('A', 'Master'),
    ('I', 'Miss'),
    ('S', 'Ms.'),
    ('D', 'Dr.'),
    ('P', 'Prof.'),
    ('K', 'Sir'),
    ('R', 'Rev.'),
)

class Address(models.Model):
    street = models.CharField(max_length=32)
    address_line2 = models.CharField(max_length=32, null=True)
    address_line3 = models.CharField(max_length=32, null=True)
    municipality = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    postcode = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, null=True)
    owner = models.IntegerField(null=True)


class Name(models.Model):
    preferred = models.CharField(max_length=32, null=True)
    first = models.CharField(max_length=32)
    middle = models.CharField(max_length=32, null=True)
    last = models.CharField(max_length=32)
    title = models.CharField(max_length=1, choices=TITLE_CHOICES, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    age_group = models.CharField(max_length=1, choices=AGE_GROUP_CHOICES, null=True)
    birthday = models.DateField(blank=True, null=True)

    cell = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=32, null=True)
    work_email = models.CharField(max_length=32, null=True)
    work_phone = models.CharField(max_length=32, null=True)

    approved = models.BooleanField()
    authority = models.IntegerField()
    picture_uploaded = models.BooleanField()
    private = models.BooleanField()
    removed = models.BooleanField()

    bad_password_attempts = models.IntegerField(null=True)
    bad_password_timeout = models.IntegerField(null=True)
    password_timeout = models.IntegerField(null=True)

    address = models.ForeignKey('Address', null=True)
    wedding = models.ForeignKey('Wedding', null=True)

    owner = models.IntegerField(null=True)
    user = models.OneToOneField(User, null=True)

class Wedding(models.Model):
    anniversary = models.DateField(null=True)
    email = models.CharField(max_length=32)
    one_tax_receipt = models.BooleanField()
    owner = models.IntegerField(null=True)
