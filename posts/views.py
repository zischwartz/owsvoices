# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime


from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse

import logging
import settings

from forms import CommentForm
from django.contrib import messages



def Home (request): 
	return render_to_response("posts/home.html", locals(), context_instance=RequestContext(request))

def Comment(request, slug):
	if request.method == 'POST':
		if request.session.get(slug, False):
			messages.error(request, 'You already weighed in on this. Sorry!')
			return HttpResponseRedirect(reverse('post_detail', kwargs={'slug':slug}))

		form = CommentForm(request.POST)
		if form.is_valid():
			c =form.save() #commit=False would avoid an extra db hit... 
			# c.created_on= datetime.now()
			post =get_object_or_404(Post, slug=slug)
			post.comments.append(c)
			post.apply_hands_and_save(c)
			request.session[slug] = 'True'
			return HttpResponseRedirect(reverse('post_detail', kwargs={'slug':slug}))
		else:
			# return HttpResponse(form.errors)
			messages.error(request, 'You need to fill out the whole comment form before weighing in.')
			return HttpResponseRedirect(reverse('post_detail', kwargs={'slug':slug}))
	else:
		return HttpResponse('huh?')

