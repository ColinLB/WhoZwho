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
    email = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=32, null=True)
    owner = models.IntegerField(null=True)

class Family(models.Model):
    anniversary = models.DateField(null=True)
    address = models.ForeignKey('Address', blank=True, null=True, on_delete=models.SET_NULL)
    one_tax_receipt = models.BooleanField(default=False)
    picture_uploaded = models.BooleanField(default=False)
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
    member_since = models.DateField(blank=True, null=True)

    cell = models.CharField(max_length=32, null=True)
    email = models.CharField(max_length=32, null=True)
    work_email = models.CharField(max_length=32, null=True)
    work_phone = models.CharField(max_length=32, null=True)

    approved = models.BooleanField(default=False)
    authority = models.IntegerField(default=False)
    out_of_town = models.BooleanField(default=False)
    picture_uploaded = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    bad_password_attempts = models.IntegerField(null=True)
    bad_password_timeout = models.IntegerField(null=True)
    password_timeout = models.IntegerField(null=True)

    address = models.ForeignKey('Address', blank=True, null=True, on_delete=models.SET_NULL)
    family = models.ForeignKey('Family', related_name='spouses', blank=True, null=True, on_delete=models.SET_NULL)
    parents = models.ForeignKey('Family', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
    wedding = models.ForeignKey('Wedding', blank=True, null=True, on_delete=models.SET_NULL)

    owner = models.IntegerField(null=True)
    user = models.OneToOneField(User, null=True)

class Wedding(models.Model):
    anniversary = models.DateField(null=True)
    email = models.CharField(max_length=32)
    one_tax_receipt = models.BooleanField(default=False)
    owner = models.IntegerField(null=True)
