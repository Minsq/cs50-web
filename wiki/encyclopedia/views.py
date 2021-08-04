from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
	entry = util.get_entry(title)
	
	if entry==None:
		return render(request, "encyclopedia/error.html",{
			"title": title,
			})

	return render(request, "encyclopedia/title.html",{
		"title": title,
		"entry": markdown2.markdown(entry)
		})


def search(request):

	q = request.GET['q']

	entries = util.list_entries()
	possible_entries = []

	for entry in entries:
		if q.lower() == entry.lower():
			return HttpResponseRedirect(reverse('title',args=[entry])) 
			#redirect('',)
		elif q.lower() in entry.lower():
			possible_entries.append({
				"query" : q,
				"entry" : entry 
				})
	return render(request, "encyclopedia/search.html", 
		{"possible_entries": possible_entries, "query": q}) 

def create(request):
	if request.method == "POST":
		#add to folder
		title = request.POST['page_title']
		text_markdown = request.POST['page_markdown']
		if util.get_entry(title) != None:
			# Throw an error
			pass
		util.save_entry(title, text_markdown)
		return HttpResponseRedirect(reverse('title',args=[title]))


	return render(request, "encyclopedia/create.html")

def edit(request, title):
	if request.method == "POST": 
		# save page
		title = request.POST['page_title']
		text_markdown = request.POST['page_markdown']

		# save the page
		util.save_entry(title, text_markdown)
		return HttpResponseRedirect(reverse('title', args=[title]))
	
	# not needed since get request.
	# btn = request.POST.get('submit-button') #.get(name_of_button); variable stores the value attribute of button
	
	# render the edit page
	entry = util.get_entry(title)

	return render(request, "encyclopedia/edit.html", {
		"title": title,
		"markup": entry
		})
def random(request):
	import random
	entries = util.list_entries()
	random_entry = random.choice(entries)
	return HttpResponseRedirect(reverse('title', args=[random_entry]))
