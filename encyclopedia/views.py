from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import default_storage
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    if util.get_entry(title) != None:
        markdowner = Markdown()
        html = markdowner.convert(util.get_entry(title))
        html = f"<head><title>{title}</title></head>\n" + html
        return HttpResponse(html)
    else:
        raise Http404("The requested page was not found")


def search(request):
    q = request.GET.get("q", "")
    if util.get_entry(q) != None:
        return HttpResponseRedirect(f"wiki/{q}")
    else:
        _, filenames = default_storage.listdir("entries")
        filtered_list = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if f"{q}" in filename)) 
        return render(request, "encyclopedia/results.html", {
        "entries": filtered_list,
        "q": q
        })
        

   
    