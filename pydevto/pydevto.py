import requests


class PyDevTo:
    def __init__(self, api_key=None, timeout=None):
        """

        :param api_key:  Your dev.to api key (https://dev.to/settings/account)
        :param timeout: Timeout period for http requests
        """
        self.api_key = api_key
        self.timeout = timeout

    def public_articles(self, page=None, tag=None, username=None, state=None, top=None):
        """Return a list of public (published) articles

        :param page: pagination page
        :param tag: articles that contain the requested tag.
        :param username: articles belonging to a User or Organization ordered by descending published_at
        :param state: "fresh" or "rising".  check which articles are fresh or rising.
        :param top: (int) most popular articles in the last N days
        :return:
        """
        return requests.get(
            "https://dev.to/api/articles",
            params={
                "page": page,
                "tag": tag,
                "username": username,
                "state": state,
                "top": top,
            },
        ).json()

    def public_article(self, id):
        """Return a single public (published) article given its id

        :param id: id of the article
        :return: article
        """
        return requests.get(
            "https://dev.to/api/articles/{id}".format(id=id), timeout=self.timeout
        ).json()

    def articles(self, page=None, per_page=None, state="published"):
        """Return a list of user articles

        :param page: pagination page
        :param per_page: page size
        :param state: "published", "unpublished" or "all
        :return: list of articles
        """
        url = "https://dev.to/api/articles/me"
        if state == "published":
            url = "https://dev.to/api/articles/me"
        elif state == "unpublished":
            url = "https://dev.to/api/articles/me/unpublished"
        elif state == "all":
            url = "https://dev.to/api/articles/me/all"

        return requests.get(
            url,
            params={"page": page, "per_page": per_page},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def create_article(
        self,
        title,
        body_markdown="",  # must default to empty string instead of None otherwise dev.to raises error on edit
        published=None,
        series=None,
        main_image=None,
        canonical_url=None,
        description=None,
        tags=None,
        organization_id=None,
    ):
        """Create an article

        :param title: Title
        :param body_markdown: Article Markdown content
        :param published: True to create published article, false otherwise
        :param series: Article series name
        :param main_image: Main image (or cover image)
        :param canonical_url: Canonical Url
        :param description: Article Description
        :param tags: List of article tags
        :param organization_id: Organization id
        :return: newly created article
        """
        url = "https://dev.to/api/articles"

        data = {
            "title": title,
            "body_markdown": body_markdown,
            "series": series,
            "published": published,
            "main_image": main_image,
            "canonical_url": canonical_url,
            "description": description,
            "tags": tags,
            "organization_id": organization_id,
        }
        # remove None keys from dict
        data = {k: v for k, v in data.items() if v is not None}

        return requests.post(
            url, json=data, headers={"api-key": self.api_key}, timeout=self.timeout
        ).json()

    def update_article(
        self,
        id,
        title=None,
        body_markdown=None,
        published=None,
        series=None,
        main_image=None,
        canonical_url=None,
        description=None,
        tags=None,
        organization_id=None,
    ):
        """Update an article

        :param id: id of article to update
        :param title: Title
        :param body_markdown: Article Markdown content
        :param published: True to create published article, false otherwise
        :param series: Article series name
        :param main_image: Main image (or cover image)
        :param canonical_url: Canonical Url
        :param description: Article Description
        :param tags: List of article tags
        :param organization_id: Organization id
        :return: updated article
        """
        url = "https://dev.to/api/articles/{id}".format(id=id)

        data = {
            "title": title,
            "body_markdown": body_markdown,
            "series": series,
            "published": published,
            "main_image": main_image,
            "canonical_url": canonical_url,
            "description": description,
            "tags": tags,
            "organization_id": organization_id,
        }
        # remove None keys from dict
        data = {k: v for k, v in data.items() if v is not None}

        return requests.put(
            url, json=data, headers={"api-key": self.api_key}, timeout=self.timeout
        ).json()

    def user(self, id=None, username=None):
        """Return user information

        If both id and username is None then information for user with the api_key (me) is returned

        :param id: (optional) id of user
        :param username: (optional) username of user
        :return: user object
        """
        url = "https://dev.to/api/users/me"
        if id:
            url = "https://dev.to/api/users/{id}".format(id=id)
        elif username:
            url = "https://dev.to/api/users/by_username"

        return requests.get(
            url,
            params={"url": username},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def follow_suggestions(self, page=None):
        """Return list of follow suggestions

        :param page: pagination page
        :return: list of follow suggestions
        """
        return requests.get(
            "https://dev.to/api/users/?state=follow_suggestions",
            params={"page": page},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def tags(self, page=None):
        """Return list of tags

        :param page: pagination page
        :return:
        """
        return requests.get(
            "https://dev.to/api/tags",
            params={"page": page},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def webhooks(self):
        """Return list of webhooks

        :return: list of webhooks
        """
        return requests.get(
            "https://dev.to/api/webhooks",
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def webhook(self, id):
        """Return single webhook with id

        :param id: id of webhook
        :return: webhook object
        """
        return requests.get(
            "https://dev.to/api/webhooks/{id}".format(id=id),
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def create_webhook(self, source, target_url, events):
        """Create a new webhook

        :param source: The name of the requester, eg. "DEV"
        :param target_url: Target Url
        :param events: List of event identifiers
        :return:
        """
        return requests.post(
            "https://dev.to/api/webhooks",
            headers={"api-key": self.api_key},
            json={"source": source, "target_url": target_url, "events": events},
            timeout=self.timeout,
        ).json()

    def delete_webhook(self, id):
        """Delete  a webhook with id

        :param id: id of webhook
        :return:
        """
        return requests.delete(
            "https://dev.to/api/webhooks/{id}".format(id=id),
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()
