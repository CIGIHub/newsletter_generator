from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^$', 'basic_newsletter.views.home', name='home'),
   url(r'^create/issue/$', 'basic_newsletter.views.create_issue', name='create_issue'),
   url(r'^edit/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.edit_issue', name='edit_issue'),
   url(r'^preview/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.preview_issue', name='preview_issue'),
   url(r'^preview/issue/(?P<issue_id>\d+)/message/$', 'basic_newsletter.views.preview_issue_html', name='preview_issue_html'),
   url(r'^delete/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.delete_issue', name='delete_issue'),
   url(r'^test/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.test_issue', name='test_issue'),
   url(r'^publish/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.publish_issue', name='publish_issue'),
   url(r'^edit_for_web/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.edit_issue', {'template': 'issue_edit.html'}, name='edit_issue_for_web'),
   url(r'^republish/issue/(?P<issue_id>\d+)/$', 'basic_newsletter.views.reupload_issue', name='reupload_issue'),
)