function addListener(element, type, func)
{
	if(window.addEventListener)
		element.addEventListener(type, func, false);
	else
		element.attachEvent('on'+type, func);
}

var autocompletion_field = document.getElementById("autocompletion_field");
var suggests = new Array();      // ensemble des suggestions
var suggests_noms = new Array(); // ensemble des noms relatifs aux suggestions
var selected = -1;

function autocompletion_reset_suggests()
{
	if(!autocompletion_field)
		autocompletion_field = document.getElementById("autocompletion_field");
	suggests = new Array();
	suggests_noms = new Array();
	selected = -1;
	autocompletion_field.innerHTML = "";
	autocompletion_field.style.display = "none";
}

function autocompletion_add_suggest(suggest, nom)
{
	autocompletion_field.style.display = "block";
	autocompletion_field.appendChild(suggest);
	
	var pos = suggests.length;
	suggest.rel = pos;
	suggests.push(suggest);
	suggests_noms.push(nom);
	
	if(navigator.appName == "Microsoft Internet Explorer")
	{
		addListener(suggest, 'mouseover', function(){ autocompletion_mouseover(pos); });
		addListener(suggest, 'mouseout', function(){ autocompletion_mouseout(pos); });
		addListener(suggest, 'click', function(){ autocompletion_click(pos); });
	}
	else
	{
		addListener(suggest, 'mouseover', function(){ autocompletion_mouseover(this.rel); });
		addListener(suggest, 'mouseout', function(){ autocompletion_mouseout(this.rel); });
		addListener(suggest, 'click', function(){ autocompletion_click(this.rel); });
	}
}

function autocompletion_mouseover(pos)
{
	for(var i=0 ; i<suggests.length ; i++)
	{
		if(navigator.appName == "Microsoft Internet Explorer")
			suggests[i].setAttribute('className', 'suggest_out') || suggests[i].setAttribute('class', 'suggest_out');
		else
			suggests[i].className = 'suggest_out';
	}
	if(navigator.appName == "Microsoft Internet Explorer")
		suggests[pos].setAttribute('className', 'suggest_over') || suggests[pos].setAttribute('class', 'suggest_over');
	else
		suggests[pos].className = 'suggest_over';
}

function autocompletion_mouseout(pos)
{
	if(navigator.appName == "Microsoft Internet Explorer")
		suggests[pos].setAttribute('className', 'suggest_out') || suggests[pos].setAttribute('class', 'suggest_out');
	else
		suggests[pos].className = 'suggest_out';
}

function autocompletion_click(pos)
{
	window.location = "/?q="+encodeURI(suggests_noms[pos]);
}

function autocompletion_select()
{
	for(var i=0 ; i<suggests.length ; i++)
	{
		if(navigator.appName == "Microsoft Internet Explorer")
			suggests[i].setAttribute('className', 'suggest_out') || suggests[i].setAttribute('class', 'suggest_out');
		else
			suggests[i].className = 'suggest_out';
	}
	if(selected >= 0 && selected < suggests.length)
	{
		if(navigator.appName == "Microsoft Internet Explorer")
			suggests[selected].setAttribute('className', 'suggest_over') || suggests[selected].setAttribute('class', 'suggest_over');
		else
			suggests[selected].className = 'suggest_over';
	}
}


function autocompletion_hook_clavier(event)
{
	switch(event.keyCode)
	{
		case 40: // down
			selected += 1;
			if(selected >= suggests.length)
				selected = suggests.length -1;
			autocompletion_select();
			break;
		case 38: // up
			selected -= 1;
			if(selected < -1)
				selected = -1;
			autocompletion_select();
			break;
		case 13: // enter
			var autocompletion_query = document.getElementById("autocompletion_query");
			if(selected >= 0 && selected < suggests.length)
			{
				autocompletion_query.value = suggests_noms[selected];
				/*search_autocompletion(autocompletion_query.value);*/
				selected = -1;
				autocompletion_field.innerHTML = "";
				autocompletion_field.style.display = "none";
			}
			else
				window.location = "/?q="+encodeURI(autocompletion_query.value);
			break;
		default:
			return true;
	}
	return true;
}

