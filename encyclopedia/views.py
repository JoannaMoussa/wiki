from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
import re
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    """ 
    If the user typed an existing entry title, the markdown content
    of the appropriate entry page will be converted to html and 
    displayed to the user. Otherwise an error will be raised.
    """
    if util.get_entry(title) != None:
        markdowner = Markdown()
        html = markdowner.convert(util.get_entry(title))
        html = f"<head><title>{title}</title></head>\n" + html
        return HttpResponse(html)
    else:
        raise Http404("The requested page was not found")


def search(request):
    """
    If the search query exists, the appropriate page will be displayed. 
    Otherwise the user should be taken to a search results 
    page that displays a list of all encyclopedia entries that have 
    the query as a substring. 
    In both cases, it's case insensitive.
    """
    q = request.GET.get("q", "")
    if util.get_entry(q) != None:
        return HttpResponseRedirect(f"/wiki/{q}")
    else:
        _, filenames = default_storage.listdir("entries")
        filtered_list = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if f"{q.lower()}" in filename.lower())) 
        return render(request, "encyclopedia/results.html", {
        "entries": filtered_list,
        "q": q
        })


# Creating a django form that allows the user to create a new page.
class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", required=True, widget=forms.TextInput(attrs={'class': 'form-control col-2 mb-3'}))
    content = forms.CharField(label="Page Content", required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': '20'}))

def new_page(request):
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })


def submit_newpage(request):
    if request.method == "POST":
        # Take in the data the user submitted and save it as form.
        form = NewPageForm(request.POST)
        # Check if form data is valid (server-side).
        if form.is_valid():
            # form.cleaned_data returns a dictionary of validated form input fields and their values.
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # TODO: take into account .strip(), possibly affecting code in other places.
            # Convert both the title and all the file names to lowercase to make the comparision case insensitive.
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                # re-render the page with existing information, with an error message.
                error_message = "This title already exists. Please choose another one."
                return render(request, "encyclopedia/new_page.html", {
                "form": form, 'error_message': error_message
                })
            else:
                util.save_entry(title, content)
                # If the url doesn't start with a slash, it will be treated as a relative url.
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            # If the form is invalid, re-render the page with existing information, with an error message.
            error_message = "The form is invalid. Please make sure you filled it correctly."
            return render(request, "encyclopedia/new_page.html", {
                "form": form, "error_message": error_message
            })
    # if the user typed the url path (request.method=get).
    else:
        return HttpResponseRedirect(reverse("wiki:new_page"))
        # The reverse function allows to retrieve url details from urls.py file through the name value provided there.
    