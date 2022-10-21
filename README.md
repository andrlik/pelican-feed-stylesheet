pelican-feed-stylesheet: A Plugin for Pelican
====================================================

[![Build Status](https://img.shields.io/github/workflow/status/andrlik/pelican-feed-stylesheet/build/main)](https://github.com/andrlik/pelican-feed-stylesheet/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-feed-stylesheet)](https://pypi.org/project/pelican-feed-stylesheet/)
![License](https://img.shields.io/pypi/l/pelican-feed-stylesheet?color=blue)

Enables use of xml stylesheets for human-readable feed generation.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-feed-stylesheet

Usage
-----

Add the following to settings to enable:

```python
FEED_STYLESHEET = "/YOUR_URL_HERE.xls"

PLUGINS.append("pelican_feed_stylesheet")
```

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/andrlik/pelican-feed-stylesheet/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the BSD-3-Clause license.
