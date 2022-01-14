from searchengine.models import Rubrique, SousRubrique, Element, Lien, Video, Blog
from django.contrib import admin

class SousCategorieInline(admin.StackedInline):
	model = SousRubrique
	extra = 3

class RubriqueAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,           {'fields': ['nom',]}),
		('Mise en page', {'fields': ['position', 'priorite',]}),
	]
	inlines = [SousCategorieInline]
	
	list_display = ('nom', 'position', 'priorite')
	list_filter = ['position',]
	search_fields = ['nom',]
	ordering = ["position", "priorite",]

class SousRubriqueAdmin(admin.ModelAdmin):
	fields = ['rubrique', 'nom', 'priorite']
	
	list_display = ('nom', 'rubrique', 'priorite')
	list_filter = ['rubrique',]
	search_fields = ['rubrique', 'nom',]
	ordering = ['rubrique', 'priorite',]

class LienInline(admin.StackedInline):
	model = Lien
	extra = 1

class VideoInline(admin.StackedInline):
	model = Video
	extra = 1

class BlogInline(admin.StackedInline):
	model = Blog
	extra = 1

class ElementAdmin(admin.ModelAdmin):
	fields = ['nom', 'sous_rubrique']
	inlines = [LienInline, VideoInline, BlogInline]
	
	list_display = ('nom', 'sous_rubrique')
	list_filter = ['sous_rubrique',]
	search_fields = ['nom',]
	ordering = ['nom',]

admin.site.register(Rubrique, RubriqueAdmin)
admin.site.register(SousRubrique, SousRubriqueAdmin)
admin.site.register(Element, ElementAdmin)

