# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from searchengine.models import Element, Rubrique, SousRubrique
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

def accueil(request):
	query = None
	try:
		query = request.GET["q"]
	except:
		pass
	
	rubriques_haut = Rubrique.objects.filter(position='1').order_by('priorite')
	rubriques_bas = Rubrique.objects.filter(position='2').order_by('priorite')
	
	# En l'absence de requête, on affiche la page d'accueil classique
	
	if query:
		elements = Element.objects.filter(nom__iexact=query)
		if len(elements) == 0:
			return render_to_response('recherche_google.html', {
				'query_': query,
				'rubriques_haut_': rubriques_haut,
				'rubriques_bas_': rubriques_bas,
			})
		else:
			paginator = Paginator(elements, 5) # Show 10 results per page

			page = request.GET.get('page')
			try:
				results = paginator.page(page)
		
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				results = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				results = paginator.page(paginator.num_pages)
			return render_to_response('element.html', {
				'query_': query,
				'selection_rubriques_': [elt.sous_rubrique.rubrique.id for elt in elements],
				'rubrique_': elements[0].sous_rubrique.rubrique,
				'sous_rubrique_': elements[0].sous_rubrique,
				'rubriques_haut_': rubriques_haut,
				'rubriques_bas_': rubriques_bas,
				'elements_': results,
			})
	else:
		return render_to_response('accueil.html', {
			'rubriques_haut_': rubriques_haut,
			'rubriques_bas_': rubriques_bas,
		})

def parcourir_rubrique(request, rubrique_nom):
	rubriques_haut = Rubrique.objects.filter(position='1').order_by('priorite')
	rubriques_bas = Rubrique.objects.filter(position='2').order_by('priorite')
	
	rubrique = get_object_or_404(Rubrique, nom=rubrique_nom)
	sous_rubriques = SousRubrique.objects.filter(rubrique=rubrique).order_by('priorite')
	
	return render_to_response('parcourir_rubrique.html', {
		'selection_rubriques_': [rubrique.id],
		'rubriques_haut_': rubriques_haut,
		'rubriques_bas_': rubriques_bas,
		'rubrique_': rubrique,
		'sous_rubriques_': sous_rubriques,
        })

def parcourir_sous_rubrique(request, rubrique_nom, sous_rubrique_nom):
	rubriques_haut = Rubrique.objects.filter(position='1').order_by('priorite')
	rubriques_bas = Rubrique.objects.filter(position='2').order_by('priorite')
	
	sous_rubrique = get_object_or_404(SousRubrique, nom=sous_rubrique_nom, rubrique__nom=rubrique_nom)
	sous_rubriques = SousRubrique.objects.filter(rubrique=sous_rubrique.rubrique).order_by('priorite')
	
	return render_to_response('parcourir_sous_rubrique.html', {
		'selection_rubriques_': [sous_rubrique.rubrique.id],
		'rubriques_haut_': rubriques_haut,
		'rubriques_bas_': rubriques_bas,
		'rubrique_': sous_rubrique.rubrique,
		'sous_rubriques_': sous_rubriques,
		'sous_rubrique_': sous_rubrique,
		'elements_': Element.objects.filter(sous_rubrique=sous_rubrique),
	})
	
def search_autocompletion_xml(request):
	"""
	Sélectionne les résultats fournis par l'autocomplétion
	dans la limite de 5
	"""
	elts = list()
	query = None
	
	# On teste si la méthode employée est de type GET
	if request.method == "GET":
		try:
			query = request.GET["q"].split(" ")
		except KeyError as e:
			pass
	
	# On applique les différents filtres
	if query and len(query) > 0:
		noneQuery = True
		elts = Element.objects.all()
		for q in query:
			if len(q) > 0:
				noneQuery = False
			filtre = Q(nom__istartswith=q)
			for beginning in [" ", "/", ".", "-", ",", "(", "[", "{", "~", "+"]:
				filtre.add(Q(nom__icontains=beginning+q), Q.OR)
			elts = elts.filter(filtre)#.distinct()
		if noneQuery:
			elts = list()
	
	return render_to_response('search_autocompletion.xml', {
		'elts_': elts[:5],
	}, mimetype="text/xml")

