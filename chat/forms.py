from django import forms

class PostForm(forms.Form):
	roomName = forms.CharField(label='Room Name:', max_length=100)
	
	CHOICES = (('none', 'Select One'),('private', 'Private'),('public', 'Public'))
	roomType = forms.ChoiceField(label='Room Type', choices=CHOICES)