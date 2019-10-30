# PyDevTo

Unofficial dev.to api for python.

### Features
* Implements all endpoints from https://docs.dev.to/api/
* Implements a few other api endpoints not documented but available in the source, such as users and follow_suggestions
* Includes a helper method to convert html to dev.to specific markdown, including support for dev.to specific embeds such as YouTube.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pydevto.

```bash
pip install pydevto
```

## Usage

Make sure you have an api key to use the authenticated endpoints.  You can get your key from https://dev.to/settings/account
(You can use pydevto without an api key for some functions, such as the public articles)

```python
import pydevto
api = pydevto.PyDevTo(api_key='MY_KEY')
api.articles()  # returns list of your own published articles
```

## Methods
```python
import pydevto
api = pydevto.PyDevTo(api_key='MY_KEY')
api.public_articles(page=None, tag=None, username=None, state=None, top=None)  # Return list of public (published) articles
api.public_article(id)  # Return a single public (published) article given its id
api.articles(page=None, per_page=None, state="published")  # Return a list of user articles
api.create_article(...)  # Create an article
api.update_article(id, ...)  # Update an article
api.user(id=None, username=None)  # Return user information
api.follow_suggestions(page=None)  # Return list of follow suggestions
api.tags(page=None)  # Return list of tags
api.webhooks()  # Return list of webhooks
api.webhook(id)  # Return single webhook with id
api.create_webhook(source, target_url, events)  # Create a new webhook
api.delete_webhook(id)  # Delete  a webhook with id
```

## Html to Markdown
PyDevTo contains a helper function to convert html to dev.to specific markdown (https://dev.to/p/editor_guide)
It supports images with captions using the HTML figcaption tag, and converts embeds such as YouTube to dev.to specific liquid tags.
```python
>>> import pydevto
>>> pydevto.html_to_markdown('<h1>Heading</h1') 
>>> '# Heading\n\n'
>>> pydevto.html_to_markdown('<iframe src="https://www.youtube.com/embed/kmjiUVEMvI4"></iframe>') 
>>> '\n{% youtube kmjiUVEMvI4 %}\n'  
```

## Known issues
* The tags property does not currently work correctly when creating/updating an article.  There is an open issue report on dev.to for this.
* The html to markdown only caters for a subset of embeds (YouTube, Twitter, repl.it, soundcloud and a few more), more will be added over time.

## Contributing
Pull requests and issue reports are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
