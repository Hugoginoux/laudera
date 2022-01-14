# -*- coding: utf-8 -*-
from django.db import models
import re

RUBRIQUE_CHOICES = (
	('1', 'Au dessus de la barre de recherche'),
	('2', 'En dessous de la barre de recherche'),
)
class Rubrique(models.Model):
	"""
	Permet de créer facilement de
	nouvelles rubriques sans avoir à passer par le code source
	"""
	nom = models.CharField(max_length=40, help_text=u"Ne doit pas contenir le caractère '/'")
	
	# Champ relatif au positionnement par rapport à la barre de recherche
	position = models.CharField(max_length=1, choices=RUBRIQUE_CHOICES)
	priorite = models.IntegerField(help_text=u"L'élément dont la priorité est la plus basse sera positionné à gauche")
		
	def __unicode__(self):
		return u"%s" % self.nom
	
	class Meta:
		unique_together = (("nom",), ("position", "priorite",))
		ordering = ["nom",]

class SousRubrique(models.Model):
	"""
	Permet d'ajouter de nouvelles sous-catégories pour une catégorie
	donnée
	"""
	rubrique = models.ForeignKey(Rubrique)
	nom = models.CharField(max_length=40, help_text=u"Ne doit pas contenir le caractère '/'")
	priorite = models.IntegerField(help_text=u"L'élément dont la priorité est la plus basse sera positionné à gauche")
	
	def __unicode__(self):
		return u"%s > %s" % (self.rubrique.nom, self.nom)
	
	class Meta:
		unique_together = (("rubrique", "nom",), ("rubrique", "priorite",))
		ordering = ["rubrique", "nom",]

class Element(models.Model):
	"""
	Chacune des entités stockées et consultables sur l'applicatif
	sont des Element
	"""
	sous_rubrique = models.ForeignKey(SousRubrique)
	nom = models.CharField(max_length=200, help_text=u"Nom de l'artiste ou de l'oeuvre (max. 200 caractères)")
	
	def __unicode__(self):
		return u"%s [%s]" % (self.nom, self.sous_rubrique)
	
	def get_sous_rubriques_attachees(self):
		return SousRubrique.objects.filter(rubrique__sousrubrique=self.sous_rubrique).order_by('priorite')
	
	class Meta:
		ordering = ["nom",]

class Url(models.Model):
	"""
	Les objets disposant d'url héritent de cette classe.
	Ceci est prévu afin d'uniformiser le système de notation de vidéos,
	liens et blogs
	"""
	url = models.URLField()
	
	def __unicode__(self):
		return u"%s" % self.url
	
	class Meta:
		abstract = True

class Lien(Url):
	"""
	Ensemble des liens reliés à un Element
	"""
	element = models.ForeignKey(Element)
	titre = models.CharField(max_length=80, blank=True, null=True, help_text=u"Titre de la page (max. 80 caractères)")
	description = models.TextField(blank=True, null=True, help_text=u"Description de la page (conseillé 200 caractères max)")

class Blog(Url):
	"""
	Ensemble des blogs reliés à un Element
	"""
	element = models.ForeignKey(Element)
	image = models.ImageField(upload_to="media/img/blog", blank=True, null=True, help_text=u"Si ce champ est renseigné, le champ url_image sera ignoré")
	url_image = models.URLField(blank=True, null=True, help_text=u"Lien vers une image disponible sur internet")

class Video(Url):
	"""
	Ensemble des vidéos reliées à un Element
	"""
	element = models.ForeignKey(Element)
	image = models.ImageField(upload_to="media/img/video", blank=True, null=True, help_text=u"Si ce champ est renseigné, le champ url_image sera ignoré")
	url_image = models.URLField(blank=True, null=True, help_text=u"Lien vers une image disponible sur internet")

