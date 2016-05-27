from django.db import models
from django.utils import timezone

from __future__ import unicode_literals


# Create your models here.

"""
Helpful info on this model: 

https://blog.heroku.com/archives/2016/3/17/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
https://github.com/jacobian/channels-example/blob/master/chat/models.py
http://www.programiz.com/python-programming/property
"""

class Room(models.Model):
	name = models.TextField()
	label = models.SlugField(unique=True)
	
	def __str__(self):
		return self.label
	
class Message(models.Model):
	room = models.ForeignKey(Room, related_name='messages')
	handle = models.TextField()
	message = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)
	
	def __str__(self):
		return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())
	
	@property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
	
	def as_dict(self):
		return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}