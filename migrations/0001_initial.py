# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('WhoZwho_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('address_line3', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('municipality', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('owner', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('WhoZwho', ['Address'])

        # Adding model 'Name'
        db.create_table('WhoZwho_name', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preferred', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('first', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('last', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('age_group', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('work_email', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('authority', self.gf('django.db.models.fields.IntegerField')()),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bad_password_attempts', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('bad_password_timeout', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('password_timeout', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Address'], null=True)),
            ('wedding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['WhoZwho.Wedding'], null=True)),
            ('owner', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
        ))
        db.send_create_signal('WhoZwho', ['Name'])

        # Adding model 'Wedding'
        db.create_table('WhoZwho_wedding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('anniversary', self.gf('django.db.models.fields.DateField')(null=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('one_tax_receipt', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('owner', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('WhoZwho', ['Wedding'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('WhoZwho_address')

        # Deleting model 'Name'
        db.delete_table('WhoZwho_name')

        # Deleting model 'Wedding'
        db.delete_table('WhoZwho_wedding')


    models = {
        'WhoZwho.address': {
            'Meta': {'object_name': 'Address'},
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'address_line3': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'WhoZwho.name': {
            'Meta': {'object_name': 'Name'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WhoZwho.Address']", 'null': 'True'}),
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'authority': ('django.db.models.fields.IntegerField', [], {}),
            'bad_password_attempts': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bad_password_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'first': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'password_timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'preferred': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'wedding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WhoZwho.Wedding']", 'null': 'True'}),
            'work_email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'})
        },
        'WhoZwho.wedding': {
            'Meta': {'object_name': 'Wedding'},
            'anniversary': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'one_tax_receipt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['WhoZwho']