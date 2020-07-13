from django.shortcuts import render

from . import util
import markdown2
from django import forms
from django.core.files.storage import default_storage

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from django.contrib import messages
import random as rand

class NewWikiForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    markdown = forms.CharField(widget=forms.Textarea, required=True)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random(request):
    wiki_name = rand.choice(util.list_entries())


    return render(request, "encyclopedia/wiki.html", {
        "entry": markdown2.markdown(util.get_entry(wiki_name)),
        "entry_name": wiki_name })




def wiki(request, wiki_name):
    entry = util.get_entry(wiki_name)

    if entry: 

        return render(request, "encyclopedia/wiki.html", {
            "entry": markdown2.markdown(entry),
            "entry_name": wiki_name

        })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    query = request.GET.get('q','')
    entry = util.get_entry(query)

    if entry: 

        return render(request, "encyclopedia/wiki.html", {
            "entry": markdown2.markdown(entry)
        })
    else:
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)

        # if not results:
        #     results = ["Sorry, the entry you requested does not exist."]
        
        return render(request, "encyclopedia/search.html" , {
            "results": results
        })

def new(request):


    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]
            
            try: 
                with open("./entries/" + title +".md", 'x') as f:
                    myfile = File(f)
                    myfile.write(markdown)
                return HttpResponseRedirect(reverse("index"))

            except FileExistsError:
                messages.info(request, 'An entry with this name exists!')
                return render(request, "encyclopedia/new.html", {
                "form": form
            })
    
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewWikiForm()
        })

def edit(request, wiki_name):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]
                        
            with open("./entries/" + title +".md", 'w') as f:
                myfile = File(f)
                myfile.write(markdown)

            return HttpResponseRedirect(reverse("wiki", args=[wiki_name]))
  
    entry = util.get_entry(wiki_name)
    form = NewWikiForm(initial={'title': wiki_name, 'markdown': entry})

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "entry_name": wiki_name


    })


