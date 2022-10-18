from feedgenerator import get_tag_uri
from markupsafe import Markup

from pelican import signals
from pelican.utils import set_date_tzinfo
from pelican.writers import Writer

from .feeds import StyledAtom1Feed, StyledRss201rev2Feed


class StyledFeedWriter(Writer):
    def _create_new_feed(self, feed_type, feed_title, context):
        feed_class = StyledRss201rev2Feed if feed_type == "rss" else StyledAtom1Feed
        if feed_title:
            feed_title = context["SITENAME"] + " - " + feed_title
        else:
            feed_title = context["SITENAME"]
        stylesheet = self.settings.get("FEED_STYLESHEET", None)
        feed = feed_class(
            title=Markup(feed_title).striptags(),
            link=(self.site_url + "/"),
            feed_url=self.feed_url,
            description=context.get("SITESUBTITLE", ""),
            subtitle=context.get("SITESUBTITLE", None),
            stylesheet_url=stylesheet,
        )
        return feed

    def _add_item_to_the_feed(self, feed, item):
        title = Markup(item.title).striptags()
        link = self.urljoiner(self.site_url, item.url)

        if isinstance(feed, StyledRss201rev2Feed):
            # RSS feeds use a single tag called 'description' for both the full
            # content and the summary
            content = None
            if self.settings.get("RSS_FEED_SUMMARY_ONLY"):
                description = item.summary
            else:
                description = item.get_content(self.site_url)

        else:
            # Atom feeds have two different tags for full content (called
            # 'content' by feedgenerator) and summary (called 'description' by
            # feedgenerator).
            #
            # It does not make sense to have the summary be the
            # exact same thing as the full content. If we detect that
            # they are we just remove the summary.
            content = item.get_content(self.site_url)
            description = item.summary
            if description == content:
                description = None

        categories = list()
        if hasattr(item, "category"):
            categories.append(item.category)
        if hasattr(item, "tags"):
            categories.extend(item.tags)

        feed.add_item(
            title=title,
            link=link,
            unique_id=get_tag_uri(link, item.date),
            description=description,
            content=content,
            categories=categories if categories else None,
            author_name=getattr(item, "author", ""),
            pubdate=set_date_tzinfo(item.date, self.settings.get("TIMEZONE", None)),
            updateddate=set_date_tzinfo(
                item.modified, self.settings.get("TIMEZONE", None)
            )
            if hasattr(item, "modified")
            else None,
        )


def add_writer(pelican_object):
    return StyledFeedWriter


def register():
    signals.get_writer.connect(add_writer)
