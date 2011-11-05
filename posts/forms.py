from django.forms import ModelForm
from django import forms
from models import *
from django.forms.widgets import *

class CommentForm(ModelForm):
	# tags = TagField(widget=TagAutocomplete())
	class Meta:
		model=Comment
		# fields = ('title', 'description', 'tags', 'enable_comments', 'owner')#, 'first_card' )
		
		# widgets = {
		# 	'slug': HiddenInput,
		# 	'number_of_cards': HiddenInput,
		# 	}
		