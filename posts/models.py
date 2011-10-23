from django.db import models

# Create your models here.
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from autoslug import AutoSlugField

from django_mongodb_engine.contrib import MongoDBManager

# in shell
# from posts.models import *

class Comment(models.Model):
	created_on = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=250)
	text = models.TextField()
	hands = models.IntegerField() # up is 1, middle is 0, -1 is down
	comments = ListField(EmbeddedModelField('self'), editable=False)
	child_number = models.IntegerField(default=0) # 0 is attached to post, 1 is to a comment, 2 is to a comment on a comment

	def __unicode__(self):
		return self.author
	
	class Meta:
		ordering = ['-created_on']


	def cssClass(self):
		if self.hands==0:
			return 'boring'

		if self.hands==-1:
			return 'error'

		if self.hands==1:
			return 'success'

class Post(models.Model):
	title = models.CharField(max_length=250)
	slug = AutoSlugField(populate_from='title', primary_key=True)
	author = models.CharField(max_length=250)
	occupation = models.CharField(max_length=250, blank=True)
	age = models.IntegerField()
	text = models.TextField()
	
	photo = models.FileField(upload_to='photos', blank=True)
	created_on = models.DateTimeField(auto_now_add=True, null=True)

	comments = ListField(EmbeddedModelField('Comment'), editable=False)
	# objects = MongoDBManager()

	hands_up = models.IntegerField(default=1) 
	hands_middle = models.IntegerField(default=0) 
	hands_down = models.IntegerField(default=0) 

	def apply_hands_and_save(self, c,  *args, **kwargs ):
		if c.hands==0:
			self.hands_middle +=1

		if c.hands==-1:
			self.hands_down +=1

		if c.hands==1:
			self.hands_up +=1

		super(Post, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title
	
	class Meta:
		ordering = ['-created_on']





# coooool

mapfunc = """
function map() {
  /* `this` refers to the current document */
  this.comments.forEach(function(comment) {
    emit(comment.hands, 1);
  });
}
"""

reducefunc = """
function reduce(id, values) {
  /* [1, 1, ..., 1].length is the same as sum([1, 1, ..., 1]) */
  return values.length;
}
"""
	
