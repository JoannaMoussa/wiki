## CS50's Web Programming with Python and JavaScript

# Project 1 - Wikipedia-like online encyclopedia

This project consists of developing a Wikipedia-like online encyclopedia. It consists of a number of encyclopedia entries on various topics. 

1. **Entry Pages**
    
    Each encyclopedia entry can be viewed by visiting \<url\>/wiki/`TITLE`, where `TITLE` is the title of an encyclopedia entry. 
    
    Encyclopedia entries are stored using the Markdown language. When a user views an encyclopedia entry, the Markdown will be converted into HTML before displaying it to the user.
    
    **Edit entry page**: On each entry page, there is an edit button that takes the user to a page where the entry’s Markdown content can be edited in a *textarea*. The *textarea* will be pre-populated with the existing Markdown content of the page. Once the user clicks the save button, the user should be redirected to that entry’s page, with a success message.

2. **Side Bar**

    2.1. **search box**: Users can type a query to search for an encyclopedia entry. If the query matches the name of an encyclopedia entry, they will be redirected to that entry’s page. Otherwise, they will instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.

    2.2. **Home page**: consists of a listing of the names of all pages in the encyclopedia. The user can click on any name and be taken directly to that encyclopedia page.

    2.3. **Create new page**: lets users create a new encyclopedia entry. They choose a title for the page, and write the content of the page using the Markdown language. After submitting the new entry page, if an encyclopedia entry already exists with the provided title, users will be presented with an error message. Otherwise, the encyclopedia entry is saved and users should be taken to the new entry’s page, with a success message.

    2.4. **Random Page**: Clicking the random page link takes users to a random encyclopedia entry.


