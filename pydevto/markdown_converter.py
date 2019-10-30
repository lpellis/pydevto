import urllib.parse as urlparse

from bs4 import BeautifulSoup, NavigableString
import re
import six


convert_heading_re = re.compile(r"convert_h(\d+)")
line_beginning_re = re.compile(r"^", re.MULTILINE)
whitespace_re = re.compile(r"[\r\n\s\t ]+")
FRAGMENT_ID = "__MARKDOWNIFY_WRAPPER__"
wrapped = '<div id="%s">%%s</div>' % FRAGMENT_ID


# Heading styles
ATX = "atx"
ATX_CLOSED = "atx_closed"
UNDERLINED = "underlined"
SETEXT = UNDERLINED


def escape(text):
    if not text:
        return ""
    return text.replace("_", r"\_")


def _todict(obj):
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith("_"))


class MarkdownConverter(object):
    """
    This class is based on on markdownify (https://github.com/matthewwithanm/python-markdownify) but extended to
    handle dev.to specific markdown and embeds
    """
    class DefaultOptions:
        strip = None
        convert = None
        autolinks = True
        heading_style = UNDERLINED
        bullets = "*+-"  # An iterable of bullet types.

    class Options(DefaultOptions):
        pass

    def __init__(self, **options):
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))
        self.options.update(options)
        if self.options["strip"] is not None and self.options["convert"] is not None:
            raise ValueError(
                "You may specify either tags to strip or tags to"
                " convert, but not both."
            )

    def convert(self, html):
        # We want to take advantage of the html5 parsing, but we don't actually
        # want a full document. Therefore, we'll mark our fragment with an id,
        # create the document, and extract the element with the id.
        html = wrapped % html
        soup = BeautifulSoup(html, "html.parser")
        return self.process_tag(soup.find(id=FRAGMENT_ID), children_only=True)

    def process_tag(self, node, children_only=False):
        text = ""

        # Convert the children first
        for el in node.children:
            if isinstance(el, NavigableString):
                text += self.process_text(six.text_type(el))
            else:
                text += self.process_tag(el)

        if not children_only:
            convert_fn = getattr(self, "convert_%s" % node.name, None)
            if convert_fn and self.should_convert_tag(node.name):
                text = convert_fn(node, text)
            # else:
            #     text = text + node.name

        return text

    def process_text(self, text):
        return escape(whitespace_re.sub(" ", text or ""))

    def __getattr__(self, attr):
        # Handle headings
        m = convert_heading_re.match(attr)
        if m:
            n = int(m.group(1))

            def convert_tag(el, text):
                return self.convert_hn(n, el, text)

            convert_tag.__name__ = "convert_h%s" % n
            setattr(self, convert_tag.__name__, convert_tag)
            return convert_tag

        raise AttributeError(attr)

    def should_convert_tag(self, tag):
        tag = tag.lower()
        strip = self.options["strip"]
        convert = self.options["convert"]
        if strip is not None:
            return tag not in strip
        elif convert is not None:
            return tag in convert
        else:
            return True

    def indent(self, text, level):
        return line_beginning_re.sub("\t" * level, text) if text else ""

    def underline(self, text, pad_char):
        text = (text or "").rstrip()
        return "%s\n%s\n\n" % (text, pad_char * len(text)) if text else ""

    def convert_a(self, el, text):
        href = el.get("href")
        title = el.get("title")
        if self.options["autolinks"] and text == href and not title:
            # Shortcut syntax
            return "<%s>" % href
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        return "[%s](%s%s)" % (text or "", href, title_part) if href else text or ""

    def convert_b(self, el, text):
        return self.convert_strong(el, text)

    def convert_figcaption(self, el, text):
        return "\n<figcaption>" + text + "</figcaption>\n"

    def convert_blockquote(self, el, text):

        # handle twitter embeds
        if el.get("class") and el.get("class")[0] == "twitter-tweet":
            for entry in el.find_all("a"):
                if entry.get("href").startswith("https://twitter.com/"):
                    return self.pydevto_embed(entry.get("href"))

        return "\n" + line_beginning_re.sub("> ", text) if text else ""

    def convert_br(self, el, text):
        return "  \n"

    def remove_scheme(self, url):
        return (
            url.replace("https://www.", "//")
            .replace("https://", "//")
            .replace("http://www.", "//")
            .replace("http://", "//")
        )

    def convert_iframe(self, el, text):
        src = self.remove_scheme(el.attrs.get("src"))
        if src.startswith("//cdn.unfurl.dev/embed?"):
            src = urlparse.unquote(src)
            query = urlparse.urlsplit(src).query
            params = urlparse.parse_qs(query)
            if params.get("url"):
                embed = params.get("url")[0]
                return self.pydevto_embed(embed)

        if src.startswith("//cdn.embedly.com"):
            src = urlparse.unquote(src)
            query = urlparse.urlsplit(src).query
            params = urlparse.parse_qs(query)
            if params.get("src"):
                embed = params.get("src")[0]
                return self.pydevto_embed(embed)

        return self.pydevto_embed(el.attrs.get("src"))

    def pydevto_embed(self, url):
        original_url = url
        url = self.remove_scheme(url)

        if url.startswith("//twitter.com"):
            q = urlparse.urlsplit(url)
            return "\n{% twitter " + q.path.split("/")[-1] + " %}\n"

        if url.startswith("//youtube.com"):
            q = urlparse.urlsplit(url)
            if q.path.startswith("/embed/"):
                return "\n{% youtube " + q.path.replace("/embed/", "") + " %}\n"
            v = urlparse.parse_qs(q.query)["v"][0]
            return "\n{% youtube " + v + " %}\n"

        if url.startswith("//codepen.io"):
            return "\n{% codepen " + original_url + " %}\n"

        if url.startswith("//soundcloud.com"):
            return "\n{% soundcloud " + original_url + " %}\n"

        if url.startswith("//github.com"):
            return "\n{% github " + original_url + " %}\n"

        if url.startswith("//instagram.com"):
            q = urlparse.urlsplit(url)
            return (
                "\n{% instagram " + q.path.replace("/p", "").replace("/", "") + " %}\n"
            )

        if url.startswith("//repl.it"):
            q = urlparse.urlsplit(url)
            return "\n{% replit " + q.path[1:] + " %}\n"

        return "\n" + original_url + "\n"

    def convert_em(self, el, text):
        return "*%s*" % text if text else ""

    def convert_hn(self, n, el, text):
        style = self.options["heading_style"]
        text = text.rstrip()
        if style == UNDERLINED and n <= 2:
            line = "=" if n == 1 else "-"
            return self.underline(text, line)
        hashes = "#" * n
        if style == ATX_CLOSED:
            return "%s %s %s\n\n" % (hashes, text, hashes)
        return "%s %s\n\n" % (hashes, text)

    def convert_i(self, el, text):
        return self.convert_em(el, text)

    def convert_list(self, el, text):
        nested = False
        while el:
            if el.name == "li":
                nested = True
                break
            el = el.parent
        if nested:
            text = "\n" + self.indent(text, 1)
        return "\n" + text + "\n"

    convert_ul = convert_list
    convert_ol = convert_list

    def convert_li(self, el, text):
        parent = el.parent
        if parent is not None and parent.name == "ol":
            bullet = "%s." % (parent.index(el) + 1)
        else:
            depth = -1
            while el:
                if el.name == "ul":
                    depth += 1
                el = el.parent
            bullets = self.options["bullets"]
            bullet = bullets[depth % len(bullets)]
        return "%s %s\n" % (bullet, text or "")

    def convert_p(self, el, text):
        return "%s\n\n" % text if text else ""

    def convert_strong(self, el, text):
        return "**%s**" % text if text else ""

    def convert_img(self, el, text):
        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or ""
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        return "![%s](%s%s)" % (alt, src, title_part)


def html_to_markdown(html):
    html = html.replace("<hr>", "<p>---</p>")
    return MarkdownConverter(heading_style="atx").convert(html)
