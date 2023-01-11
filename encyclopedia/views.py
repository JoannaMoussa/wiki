from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
import re
from django import forms
import random
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages


# Creating a django form that allows the user to create a new page.
class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", required=True, widget=forms.TextInput(attrs={'class': 'form-control col-2 mb-3'}))
    content = forms.CharField(label="Page Content", required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': '20'}))


# Creating a django form that allows the user to edit a page.
class EditPageForm(forms.Form):
    content = forms.CharField(label = "Page content", required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': '20'}))


def index(request):
    """ Home page listing all names of encyclopedia entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    """ 
    If the user typed wiki/an existing entry title, the markdown content
    of the appropriate entry page will be converted to html and 
    displayed to the user. Otherwise an error will be raised.
    """
    if util.get_entry(title) != None:
        markdowner = Markdown()
        html = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/entry_page_layout.html", {
            "html": html, "title": title
        })
    else:
        raise Http404("The requested page was not found.")


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
        return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={"title":q}))
        # The reverse function allows to retrieve url details from urls.py file 
        # through the name value provided there.
    else:
        _, filenames = default_storage.listdir("entries")
        filtered_list = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if f"{q.lower()}" in filename.lower())) 
        return render(request, "encyclopedia/results.html", {
        "entries": filtered_list,
        "q": q
        })


def new_page(request):
    """ returns new_page.html containing a form 
    that enables the user to add a new entry.
    """
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })


def submit_newpage(request):
    """
    This function is called when the user clicks the submit button,
    on new_page.html. If the title of the new entry to be submitted 
    already exists, an error message will appear and the submission 
    will not take effect. Otherwise the entry will be saved and the 
    user will be redirected to the new entry page.
    """
    if request.method == "POST":
        # Take in the data the user submitted and save it as form.
        form = NewPageForm(request.POST)
        # Check if form data is valid (server-side).
        if form.is_valid():
            # form.cleaned_data returns a dictionary of validated form input fields 
            # and their values.
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # Convert both the title and all the file names to lowercase 
            # to make the comparision case insensitive.
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                # re-render the page with existing information, with an error message.
                #form['title'].label_tag(attrs={'class': 'is-invalid'})
                messages.error(request, 'This title already exists. Please choose another one.')
                return render(request, "encyclopedia/new_page.html", {
                    "form": form
                })
            else:
                util.save_entry(title, content)
                messages.success(request, 'Your entry was created successfully.')
                return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={"title":title}))
        else:
            # If the form is invalid, re-render the page with existing information, 
            # with an error message.
            messages.error(request, 'The form is invalid. Please make sure you filled it correctly.')
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    # if the user typed the url path (request.method=get).
    else:
        return HttpResponseRedirect(reverse("wiki:new_page"))
    


def edit_page(request, title):
    """
    Returns a form to let the user edit the content of a given page.
    The content field is pre-populated with the existing 
    Markdown content of the page.
    """
    current_content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": EditPageForm(initial={"content": current_content})
    })


def save_changes(request, title):
    """
    This function is called when the user clicks the save button,
    on edit_page.html.
    """
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, bytes(content, 'utf-8'))
            messages.success(request, 'The page was edited successfully.')
            return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title': title}))
        else:
            messages.error(request, 'The changes are not valid.')
            return render(request, "encyclopedia/edit_page.html", {
                "form": form
            })
    else:
        # if the user typed the url path (request.method=get).
        return HttpResponseRedirect(reverse("wiki:index"))


def random_page(request):
    """ Returns a random entry page."""
    entry_page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry_page", kwargs={'title': entry_page}))


#def error_404(request, exception):
#   return render(request, '404.html')
     
