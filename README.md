## CS50's Web Programming with Python and JavaScript

# Project 1 - Wikipedia-like Online Encyclopedia

This project consists of developing a Wikipedia-like online encyclopedia, in which users can browse a number of encyclopedia entries on various topics. 

1. **Entry Pages**
    
    Each encyclopedia entry can be viewed by visiting \<url\>/wiki/`TITLE`, where `TITLE` is the title of a given encyclopedia entry. 
    
    Encyclopedia entries contents are stored in Markdown `.md` files. When a user views an encyclopedia entry, the Markdown content will be converted into HTML before being displayed in the front-end.
    
    **Edit entry page**: On each entry page, there is an edit button that takes the user to a page where the entry’s Markdown content can be edited in a *textarea*. The *textarea* will be pre-populated with the existing Markdown content of the page. Once the user clicks the save button, the user should be redirected to that entry’s page, with a success message.

    **Delete entry page**: On each entry page, there is a delete button that lets the user delete an encyclopedia entry. Once the delete button clicked, the user is redirected to the home page with a success message stating that the entry was deleted successfully.

    **Recommendations to check similar entry pages**: At the end of each entry page, users can find a list of related/similar entries to visit. The listed entries are links that take the user to the appropriate entry pages. In the current implementation, two entries are considered similar if any one of them is a substring in the other.
    This section will not be present if there are no similar entries to the currently viewed entry.

2. **Side Bar**

    2.1. **Search box**: Users can type a query to search for an encyclopedia entry. If the query matches the name of an encyclopedia entry, they will be redirected to that entry’s page. Otherwise, they will instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.

    2.2. **Home page**: Consists of a listing of the titles of all entries in the encyclopedia. The user can click on any title and be taken directly to that encyclopedia entry page.

    2.3. **Create new page**: Lets users create a new encyclopedia entry. Users enter a title for the entry as well as the content of the entry using the Markdown language. After submitting the new entry page, if an encyclopedia entry already exists with the provided title, users will be presented with an error message. Otherwise, the encyclopedia entry is saved and users are redirected to the new entry’s page, with a success message.

    2.4. **Random page**: Clicking the random page link takes users to a random encyclopedia entry.
