import io

import pytest

from .feeds import StyledAtom1Feed, StyledRss201rev2Feed, StyledRssUserland091Feed


@pytest.mark.parametrize(
    "feed_class", [StyledAtom1Feed, StyledRssUserland091Feed, StyledRss201rev2Feed]
)
def test_stylesheet_url_written_feed(feed_class):
    output = io.StringIO()
    encoding = "UTF-8"
    stylesheet_url = "https://www.example.com/feed.xsl"
    feed = feed_class(
        title="My Amazing Feed",
        link="https://www.example.com",
        description="My Cool Feed",
        stylesheet_url=stylesheet_url,
    )
    feed.write(output, encoding)
    assert (
        '<?xml-stylesheet href="https://www.example.com/feed.xsl" type="text/xsl"?>\n'
        in output.getvalue()
    )


@pytest.mark.parametrize(
    "feed_class", [StyledAtom1Feed, StyledRssUserland091Feed, StyledRss201rev2Feed]
)
def test_no_stylesheet_feed(feed_class):
    output = io.StringIO()
    encoding = "UTF-8"
    feed = feed_class(
        title="My Amazing Feed",
        link="https://www.example.com",
        description="My Cool Feed",
    )
    feed.write(output, encoding)
    assert "<?xml-stylesheet" not in output.getvalue()
