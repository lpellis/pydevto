import requests
from typing import Optional,List


class PyDevTo:
    def __init__(self, api_key:Optional[str]=None, timeout:Optional[float]=None):
        """

        Args:
          api_key: Your dev.to api key (https://dev.to/settings/account)
          timeout: Timeout period for http requests

        Returns:

        """
        self.api_key = api_key
        self.timeout = timeout

    def public_articles(self, page:Optional[int]=None, tag:Optional[str]=None, username:Optional[str]=None, state:Optional[str]=None, top:Optional[int]=None):
        """Return a list of public (published) articles

        Args:
          page: pagination page (Default value = None)
          tag: articles that contain the requested tag. (Default value = None)
          username: articles belonging to a User or Organization ordered by descending published_at (Default value = None)
          state: fresh" or "rising".  check which articles are fresh or rising. (Default value = None)
          top: int) most popular articles in the last N days (Default value = None)

        Returns:

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

    def public_article(self, id:int):
        """Return a single public (published) article given its id

        Args:
          id: id of the article

        Returns:
          article

        """
        return requests.get(
            "https://dev.to/api/articles/{id}".format(id=id), timeout=self.timeout
        ).json()

    def articles(self, page:Optional[int]=None, per_page:Optional[int]=None, state:str="published"):
        """Return a list of user articles

        Args:
          page: pagination page (Default value = None)
          per_page: page size (Default value = None)
          state: published", "unpublished" or "all (Default value = "published")

        Returns:
          list of articles

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
        title:str,
        # must default to empty string instead of None otherwise dev.to raises error on edit
        body_markdown:str="",
        published:Optional[bool]=None,
        series:str=None,
        main_image:str=None,
        canonical_url:str=None,
        description:str=None,
        tags:Optional[List[str]]=None,
        organization_id:Optional[int]=None,
    ):
        """Create an article

        Args:
          title: Title
          body_markdown: Article Markdown content (Default value = "")
          published: True to create published article, false otherwise
          series: Article series name (Default value = None)
          main_image: Main image (or cover image) (Default value = None)
          canonical_url: Canonical Url (Default value = None)
          description: Article Description (Default value = None)
          tags: List of article tags (Default value = None)
          organization_id: Organization id (Default value = None)
          # must default to empty string instead of None otherwise dev.to raises error on editpublished:  (Default value = None)

        Returns:
          newly created article

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
        id:int,
        title:Optional[str]=None,
        body_markdown:Optional
        [str]=None,
        published:Optional[bool]=None,
        series:Optional[str]=None,
        main_image:Optional[str]=None,
        canonical_url:Optional[str]=None,
        description:Optional[str]=None,
        tags:Optional[List[str]]=None,
        organization_id:Optional[int]=None,
    ):
        """Update an article

        Args:
          id: id of article to update
          title: Title (Default value = None)
          body_markdown: Article Markdown content (Default value = None)
          published: True to create published article, false otherwise (Default value = None)
          series: Article series name (Default value = None)
          main_image: Main image (or cover image) (Default value = None)
          canonical_url: Canonical Url (Default value = None)
          description: Article Description (Default value = None)
          tags: List of article tags (Default value = None)
          organization_id: Organization id (Default value = None)

        Returns:
          updated article

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

    def user(self, id:Optional[int]=None, username:Optional[str]=None):
        """Return user information

        If both id and username is None then information for user with the api_key (me) is returned

        Args:
          id: optional) id of user (Default value = None)
          username: optional) username of user (Default value = None)

        Returns:
          user object

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

        Args:
          page: pagination page (Default value = None)

        Returns:
          list of follow suggestions

        """
        return requests.get(
            "https://dev.to/api/users/?state=follow_suggestions",
            params={"page": page},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def tags(self, page=None):
        """Return list of tags

        Args:
          page: pagination page (Default value = None)

        Returns:

        """
        return requests.get(
            "https://dev.to/api/tags",
            params={"page": page},
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def webhooks(self):
        """

        Args:

        Returns:
          :return: list of webhooks

        """
        return requests.get(
            "https://dev.to/api/webhooks",
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def webhook(self, id:int):
        """Return single webhook with id

        Args:
          id: id of webhook

        Returns:
          webhook object

        """
        return requests.get(
            "https://dev.to/api/webhooks/{id}".format(id=id),
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()

    def create_webhook(self, source:str, target_url:str, events:List[str]):
        """Create a new webhook

        Args:
          source: The name of the requester, eg. "DEV"
          target_url: Target Url
          events: List of event identifiers

        Returns:

        """
        return requests.post(
            "https://dev.to/api/webhooks",
            headers={"api-key": self.api_key},
            json={"source": source, "target_url": target_url, "events": events},
            timeout=self.timeout,
        ).json()

    def delete_webhook(self, id:int):
        """Delete  a webhook with id

        Args:
          id: id of webhook

        Returns:

        """
        return requests.delete(
            "https://dev.to/api/webhooks/{id}".format(id=id),
            headers={"api-key": self.api_key},
            timeout=self.timeout,
        ).json()
