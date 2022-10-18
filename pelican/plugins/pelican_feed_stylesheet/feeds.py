from feedgenerator import (
    Atom1Feed,
    RssFeed,
)
from feedgenerator.django.utils.xmlutils import SimplerXMLGenerator
from feedgenerator.django.utils.feedgenerator import rfc2822_date


class StyledSimplerXMLGenerator(SimplerXMLGenerator):
    def add_stylesheet(self, stylesheet_url):
        self._write(f'<?xml-stylesheet href="{stylesheet_url}" type="text/xsl"?>\n')


class StyledRssFeed(RssFeed):
    """
    Takes the base syndication feed but adds an option to specify
    stylesheet URL.
    """

    def __init__(
        self,
        title,
        link,
        description,
        language=None,
        author_email=None,
        author_name=None,
        author_link=None,
        subtitle=None,
        categories=None,
        feed_url=None,
        feed_copyright=None,
        image=None,
        feed_guid=None,
        ttl=None,
        **kwargs,
    ):
        stylesheet_url = kwargs.pop("stylesheet_url", None)
        super().__init__(
            title,
            link,
            description,
            language=None,
            author_email=None,
            author_name=None,
            author_link=None,
            subtitle=None,
            categories=None,
            feed_url=None,
            feed_copyright=None,
            image=None,
            feed_guid=None,
            ttl=None,
            **kwargs,
        )
        if stylesheet_url is not None:
            self.feed["stylesheet_url"] = stylesheet_url

    def write(self, outfile, encoding):
        handler = StyledSimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        stylesheet_url = self.feed.get("stylesheet_url", None)
        if stylesheet_url is not None:
            handler.add_stylesheet(stylesheet_url)
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")


class StyledRssUserland091Feed(StyledRssFeed):
    _version = "0.91"

    def add_item_elements(self, handler, item):
        handler.addQuickElement("title", item["title"])
        handler.addQuickElement("link", item["link"])
        if item["description"] is not None:
            handler.addQuickElement("description", item["description"])


class StyledRss201rev2Feed(StyledRssFeed):
    # Spec: http://blogs.law.harvard.edu/tech/rss
    _version = "2.0"

    def add_item_elements(self, handler, item):
        handler.addQuickElement("title", item["title"])
        handler.addQuickElement("link", item["link"])
        if item["description"] is not None:
            handler.addQuickElement("description", item["description"])

        # Author information.
        if item["author_name"] and item["author_email"]:
            handler.addQuickElement(
                "author", "%s (%s)" % (item["author_email"], item["author_name"])
            )
        elif item["author_email"]:
            handler.addQuickElement("author", item["author_email"])
        elif item["author_name"]:
            handler.addQuickElement(
                "dc:creator",
                item["author_name"],
                {"xmlns:dc": "http://purl.org/dc/elements/1.1/"},
            )

        if item["pubdate"] is not None:
            handler.addQuickElement("pubDate", rfc2822_date(item["pubdate"]))
        if item["comments"] is not None:
            handler.addQuickElement("comments", item["comments"])
        if item["unique_id"] is not None:
            handler.addQuickElement(
                "guid", item["unique_id"], attrs={"isPermaLink": "false"}
            )
        if item["ttl"] is not None:
            handler.addQuickElement("ttl", item["ttl"])

        # Enclosure.
        if item["enclosure"] is not None:
            handler.addQuickElement(
                "enclosure",
                "",
                {
                    "url": item["enclosure"].url,
                    "length": item["enclosure"].length,
                    "type": item["enclosure"].mime_type,
                },
            )

        # Categories.
        for cat in item["categories"]:
            handler.addQuickElement("category", cat)


class StyledAtom1Feed(Atom1Feed):
    """
    Allows for receiving an optional stylesheet url.
    """

    def __init__(
        self,
        title,
        link,
        description,
        language=None,
        author_email=None,
        author_name=None,
        author_link=None,
        subtitle=None,
        categories=None,
        feed_url=None,
        feed_copyright=None,
        image=None,
        feed_guid=None,
        ttl=None,
        **kwargs,
    ):
        stylesheet_url = kwargs.pop("stylesheet_url", None)
        super().__init__(
            title,
            link,
            description,
            language=None,
            author_email=None,
            author_name=None,
            author_link=None,
            subtitle=None,
            categories=None,
            feed_url=None,
            feed_copyright=None,
            image=None,
            feed_guid=None,
            ttl=None,
            **kwargs,
        )
        if stylesheet_url is not None:
            self.feed["stylesheet_url"] = stylesheet_url

    def write(self, outfile, encoding):
        handler = StyledSimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        stylesheet_url = self.feed.get("stylesheet_url", None)
        if stylesheet_url is not None:
            handler.add_stylesheet(stylesheet_url)
        handler.startElement("feed", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        handler.endElement("feed")

    DefaultFeed = StyledRss201rev2Feed
