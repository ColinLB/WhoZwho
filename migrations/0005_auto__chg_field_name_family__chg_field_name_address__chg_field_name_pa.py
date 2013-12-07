# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Name.family'
        db.alter_column(u'WhoZwho_name', 'family_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['WhoZwho.Family']))

        # Changing field 'Name.address'
        db.alter_column(u'WhoZwho_name', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Address'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Name.parents'
        db.alter_column(u'WhoZwho_name', 'parents_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['WhoZwho.Family']))

        # Changing field 'Name.wedding'
        db.alter_column(u'WhoZwho_name', 'wedding_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Wedding'], null=True, on_delete=models.SET_NULL))
        # Deleting field 'Family.email'
        db.delete_column(u'WhoZwho_family', 'email')

        # Adding field 'Family.address'
        db.add_column(u'WhoZwho_family', 'address',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='family_address', null=True, on_delete=models.SET_NULL, to=orm['WhoZwho.Address']),
                      keep_default=False)

        # Adding field 'Address.email'
        db.add_column(u'WhoZwho_address', 'email',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Name.family'
        db.alter_column(u'WhoZwho_name', 'family_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['WhoZwho.Family']))

        # Changing field 'Name.address'
        db.alter_column(u'WhoZwho_name', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Address'], null=True))

        # Changing field 'Name.parents'
        db.alter_column(u'WhoZwho_name', 'parents_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['WhoZwho.Family']))

        # Changing field 'Name.wedding'
        db.alter_column(u'WhoZwho_name', 'wedding_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Wedding'], null=True))
        # Adding field 'Family.email'
        db.add_column(u'WhoZwho_family', 'email',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True),
                      keep_default=False)

        # Deleting field 'Family.address'
        db.delete_column(u'WhoZwho_family', 'address_id')

        # Deleting field 'Address.email'
        db.delete_column(u'WhoZwho_address', 'email')


    models = {
        u'WhoZwho.address': {
            'Meta': {'object_name': 'Address'},
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'address_line3': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'WhoZwho.family': {
            'Meta': {'object_name': 'Family'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'family_address'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['WhoZwho.Address']"}),
            'anniversary': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'one_tax_receipt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'picture_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'WhoZwho.name': {
            'Meta': {'object_name': 'Name'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['WhoZwho.Address']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authority': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'bad_password_attempts': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bad_password_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'spouses'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['WhoZwho.Family']"}),
            'first': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'member_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'middle': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'out_of_town': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parents': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['WhoZwho.Family']"}),
            'password_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'picture_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'preferred': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'wedding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['WhoZwho.Wedding']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'work_email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'})
        },
        u'WhoZwho.wedding': {
            'Meta': {'object_name': 'Wedding'},
            'anniversary': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'one_tax_receipt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['WhoZwho']