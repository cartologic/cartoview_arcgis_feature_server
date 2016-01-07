# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Datastore'
        db.create_table(u'cartoserver_datastore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(default='loacalhost', max_length=100)),
            ('port', self.gf('django.db.models.fields.IntegerField')()),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'cartoserver', ['Datastore'])

        # Adding unique constraint on 'Datastore', fields ['name', 'user', 'host', 'port']
        db.create_unique(u'cartoserver_datastore', ['name', 'user', 'host', 'port'])

        # Adding model 'GeoTable'
        db.create_table(u'cartoserver_geotable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('table_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'cartoserver_geotable', to=orm['contenttypes.ContentType'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'cartoserver_geotable', null=True, to=orm['people.Profile'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('datastore', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'cartoserver_geotable', null=True, to=orm['cartoserver.Datastore'])),
        ))
        db.send_create_signal(u'cartoserver', ['GeoTable'])

        # Adding model 'FeatureLayer'
        db.create_table(u'cartoserver_featurelayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'cartoserver_featurelayer', to=orm['contenttypes.ContentType'])),
            ('service_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('copyright_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('max_records', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('included_fields_names', self.gf('django.db.models.fields.CharField')(default='*', max_length=1000, null=True, blank=True)),
            ('display_field_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('drawing_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('popup', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('initial_query', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'cartoserver_featurelayer', null=True, to=orm['people.Profile'])),
            ('has_attachments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'cartoserver', ['FeatureLayer'])

        # Adding model 'Attachment'
        db.create_table(u'cartoserver_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('feature_layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartoserver.FeatureLayer'])),
            ('feature_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cartoserver', ['Attachment'])

        # Adding model 'TileService'
        db.create_table(u'cartoserver_tileservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('copyright_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('background_color', self.gf('cartoview.apps.cartoview_arcgis_feature_server.cartoserver.fields.ColorField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'cartoserver', ['TileService'])

        # Adding model 'TilesLayer'
        db.create_table(u'cartoserver_tileslayer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cartoserver_layers', to=orm['contenttypes.ContentType'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='layers', to=orm['cartoserver.TileService'])),
            ('style', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('filter', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'cartoserver', ['TilesLayer'])


    def backwards(self, orm):
        # Removing unique constraint on 'Datastore', fields ['name', 'user', 'host', 'port']
        db.delete_unique(u'cartoserver_datastore', ['name', 'user', 'host', 'port'])

        # Deleting model 'Datastore'
        db.delete_table(u'cartoserver_datastore')

        # Deleting model 'GeoTable'
        db.delete_table(u'cartoserver_geotable')

        # Deleting model 'FeatureLayer'
        db.delete_table(u'cartoserver_featurelayer')

        # Deleting model 'Attachment'
        db.delete_table(u'cartoserver_attachment')

        # Deleting model 'TileService'
        db.delete_table(u'cartoserver_tileservice')

        # Deleting model 'TilesLayer'
        db.delete_table(u'cartoserver_tileslayer')


    models = {
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
        u'cartoserver.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'feature_layer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartoserver.FeatureLayer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cartoserver.datastore': {
            'Meta': {'unique_together': "(('name', 'user', 'host', 'port'),)", 'object_name': 'Datastore'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'default': "'loacalhost'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        u'cartoserver.datastore_admb_vil': {
            u'DIST_CODE': ('django.db.models.fields.IntegerField', [], {'db_column': "u'DIST_CODE'"}),
            'Meta': {'object_name': 'datastore_admb_vil', 'db_table': "'admb_vil'", 'managed': 'False'},
            u'OBJECTID': ('django.db.models.fields.BigIntegerField', [], {'db_column': "u'OBJECTID'"}),
            u'SHAPE_AREA': ('django.db.models.fields.FloatField', [], {'db_column': "u'SHAPE_AREA'"}),
            u'SHAPE_LEN': ('django.db.models.fields.FloatField', [], {'db_column': "u'SHAPE_LEN'"}),
            u'VIL_CCD': ('django.db.models.fields.IntegerField', [], {'db_column': "u'VIL_CCD'"}),
            u'VIL_CODE': ('django.db.models.fields.IntegerField', [], {'db_column': "u'VIL_CODE'"}),
            u'VIL_NM_E': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'VIL_NM_E'"}),
            u'VIL_NM_G': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'VIL_NM_G'"}),
            u'fid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'fid'"}),
            u'the_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'db_column': "u'the_geom'", 'blank': 'True'})
        },
        u'cartoserver.default_arcportal_item': {
            'Meta': {'object_name': 'default_arcportal_item', 'db_table': "'arcportal_item'", 'managed': 'False'},
            u'created': ('django.db.models.fields.DateTimeField', [], {'db_column': "u'created'"}),
            u'description': ('django.db.models.fields.TextField', [], {'db_column': "u'description'"}),
            u'extent': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'db_column': "u'extent'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "u'id'"}),
            u'license_info': ('django.db.models.fields.TextField', [], {'db_column': "u'license_info'"}),
            u'modified': ('django.db.models.fields.DateTimeField', [], {'db_column': "u'modified'"}),
            u'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'name'"}),
            u'owner_id': ('django.db.models.fields.IntegerField', [], {'db_column': "u'owner_id'"}),
            u'snippet': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "u'snippet'"}),
            u'tags': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "u'tags'"}),
            u'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'db_column': "u'thumbnail'"}),
            u'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'title'"}),
            u'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'type'"}),
            u'type_keywords': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "u'type_keywords'"}),
            u'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "u'url'"})
        },
        u'cartoserver.featurelayer': {
            'Meta': {'object_name': 'FeatureLayer'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cartoserver_featurelayer'", 'to': u"orm['contenttypes.ContentType']"}),
            'copyright_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_field_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'drawing_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attachments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_fields_names': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'initial_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'max_records': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cartoserver_featurelayer'", 'null': 'True', 'to': u"orm['people.Profile']"}),
            'popup': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'service_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cartoserver.geotable': {
            'Meta': {'object_name': 'GeoTable'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cartoserver_geotable'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datastore': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cartoserver_geotable'", 'null': 'True', 'to': u"orm['cartoserver.Datastore']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cartoserver_geotable'", 'null': 'True', 'to': u"orm['people.Profile']"}),
            'table_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cartoserver.tileservice': {
            'Meta': {'object_name': 'TileService'},
            'background_color': ('cartoview.apps.cartoview_arcgis_feature_server.cartoserver.fields.ColorField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'copyright_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'cartoserver.tileslayer': {
            'Meta': {'ordering': "['order']", 'object_name': 'TilesLayer'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cartoserver_layers'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filter': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'layers'", 'to': u"orm['cartoserver.TileService']"}),
            'style': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'people.profile': {
            'Meta': {'object_name': 'Profile'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivery': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'voice': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cartoserver']