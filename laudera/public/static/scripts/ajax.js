/* Algorithme de recherche par autocomplétion */

var last_search_request = ""
function search_autocompletion(requete)
{
	var xmlhttp;
	if(window.XMLHttpRequest)
		xmlhttp = new XMLHttpRequest();
	else
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	
	last_search_request = requete;
	var search_results_loading = document.getElementById("search_results_loading");
	search_results_loading.style.display = "block";
	xmlhttp.onreadystatechange = function()
  	{
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
		{
			search_results_loading.style.display = "none";
			if(last_search_request == requete)
			{
				var query = requete.split(" ");
				var xmlDoc = xmlhttp.responseXML;
				var elements = xmlDoc.getElementsByTagName("element");
				
				autocompletion_reset_suggests();
				for(i = 0 ; i < elements.length ; i++)
				{
					var nom = elements[i].getElementsByTagName("nom")[0].firstChild.data;
					var rubrique = elements[i].getElementsByTagName("rub")[0];
					var rubrique_nom = rubrique.getElementsByTagName("nom")[0].firstChild.data;
					var rubrique_url = rubrique.getElementsByTagName("url")[0].firstChild.data;
					var sous_rubrique = elements[i].getElementsByTagName("srub")[0];
                                        var sous_rubrique_nom = sous_rubrique.getElementsByTagName("nom")[0].firstChild.data;
                                        var sous_rubrique_url = sous_rubrique.getElementsByTagName("url")[0].firstChild.data;
					var suggest = document.createElement("div");
					suggest.innerHTML = nom+"<br /><span class=\"details\">"+rubrique_nom+" &gt; "+sous_rubrique_nom+"</span>";
					autocompletion_add_suggest(suggest, nom);
				}
			}
		}
	}
	xmlhttp.open("GET", "/ajax/autocompletion/?q="+encodeURI(requete), true);
	xmlhttp.send();
}

