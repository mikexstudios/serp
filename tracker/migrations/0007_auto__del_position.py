# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Position'
        db.delete_table('tracker_position')
    
    
    def backwards(self, orm):
        
        # Adding model 'Position'
        db.create_table('tracker_position', (
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Track'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tracker', ['Position'])
    
    
    models = {
        'tracker.check': {
            'Meta': {'object_name': 'Check'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pagerank': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Track']"})
        },
        'tracker.track': {
            'Meta': {'object_name': 'Track'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'search_engine': ('django.db.models.fields.CharField', [], {'default': "'google'", 'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }
    
    complete_apps = ['tracker']
