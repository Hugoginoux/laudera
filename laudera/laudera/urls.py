from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'searchengine.views.accueil'),
	url(r'^ajax/autocompletion/', 'searchengine.views.search_autocompletion_xml'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<rubrique_nom>.[^/]+)/$', 'searchengine.views.parcourir_rubrique'),
        url(r'^(?P<rubrique_nom>.[^/]+)/(?P<sous_rubrique_nom>.[^/]+)/$', 'searchengine.views.parcourir_sous_rubrique'),
)

if settings.DEBUG:
	''' Permet de servir les medias avec le serveur de dev '''
	from django.views.static import serve
	_media_url = settings.MEDIA_URL
	if _media_url.startswith('/'):
		_media_url = _media_url[1:]
		urlpatterns += patterns('',
			(r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT}),
		)
	del(_media_url, serve)
