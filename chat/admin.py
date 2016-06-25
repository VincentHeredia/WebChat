from django.contrib import admin

# Register your models here.

from .models import Room, Message

class MessageInline(admin.StackedInline):
	model = Message
	extra = 0
	list_display = ('timestamp','handle','message')
	list_filter = ['timestamp']
	search_fields = ['handle']
	list_per_page = 20

class RoomAdmin(admin.ModelAdmin):
	inlines = [MessageInline]
	
admin.site.register(Room, RoomAdmin)