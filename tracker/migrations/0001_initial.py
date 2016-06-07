# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Track'
        db.create_table('tracker_track', (
            ('search_engine', self.gf('django.db.models.fields.CharField')(default='google', max_length=20)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tracker', ['Track'])

        # Adding model 'Position'
        db.create_table('tracker_position', (
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Track'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tracker', ['Position'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Track'
        db.delete_table('tracker_track')

        # Deleting model 'Position'
        db.delete_table('tracker_position')
    
    
    models = {
        'tracker.position': {
            'Meta': {'object_name': 'Position'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Track']"})
        },
        'tracker.track': {
            'Meta': {'object_name': 'Track'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'search_engine': ('django.db.models.fields.CharField', [], {'default': "'google'", 'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }
    
    complete_apps = ['tracker']
