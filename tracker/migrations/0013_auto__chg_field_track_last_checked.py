# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Track.last_checked'
        db.alter_column('tracker_track', 'last_checked', self.gf('django.db.models.fields.DateTimeField')())
    
    
    def backwards(self, orm):
        
        # Changing field 'Track.last_checked'
        db.alter_column('tracker_track', 'last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))
    
    
    models = {
        'tracker.check': {
            'Meta': {'object_name': 'Check'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'pagerank': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.Track']"})
        },
        'tracker.track': {
            'Meta': {'object_name': 'Track'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)'}),
            'search_engine': ('django.db.models.fields.CharField', [], {'default': "'google'", 'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }
    
    complete_apps = ['tracker']
