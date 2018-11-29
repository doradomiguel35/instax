# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from .models import FeedModel,CommentModel
from feed.models import AccountsModel

from django.shortcuts import render

class FeedsView(View):
	template_name = 'feed/users_page.html'
	feed_data = FeedModel.objects.all()
	comment_data = CommentModel.objects.all()

	def get(self, *args, **kwargs):
		return render(self.request, self.template_name,
			{'feed_data': self.feed_data,
			'comment_data':self.comment_data}
			)
