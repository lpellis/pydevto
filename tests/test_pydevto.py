import pytest

import pydevto
from pydevto import __version__


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "html,result",
    [
        ("<h1>heading</h1>", "# heading\n\n"),
        ("<h2>heading</h2>", "## heading\n\n"),
        ("<h3>heading</h3>", "### heading\n\n"),
        ("<h4>heading</h4>", "#### heading\n\n"),
        ("<h5>heading</h5>", "##### heading\n\n"),
        ("<h6>heading</h6>", "###### heading\n\n"),
        ("<strong>strong</strong>", "**strong**"),
        ("<b>bold</b>", "**bold**"),
        ("<em>em</em>", "*em*"),
        ("<hr>", "---\n\n"),
        ("<i>italic</i>", "*italic*"),
        ("<blockquote>quote</blockquote>", "\n> quote"),
        ("<ul><li>item1</li><li>item2</li></ul>", "\n* item1\n* item2\n\n"),
    ],
)
def test_html_to_markdown_basic(html, result):
    assert pydevto.html_to_markdown(html) == result


@pytest.mark.parametrize(
    "html,result",
    [
        ("<b>bold<i>and italic</i></b>", "**bold*and italic***"),
        ("<i>italic</i><b>bold</b>", "*italic***bold**"),
    ],
)
def test_html_to_markdown_nested(html, result):
    assert pydevto.html_to_markdown(html) == result


@pytest.mark.parametrize(
    "html,result",
    [
        (
            '<p><a href="https://example.com">example link</a></p>',
            "[example link](https://example.com)\n\n",
        ),
        (
            "<p><a href='https://example.com'>example link</a></p>",
            "[example link](https://example.com)\n\n",
        ),
        (
            '<p><a target="_blank" href="https://example.com">example link</a></p>',
            "[example link](https://example.com)\n\n",
        ),
        (
            '<p><a target="_blank" title="the title" href="https://example.com">example link</a></p>',
            '[example link](https://example.com "the title")\n\n',
        ),
        (
            '<p><a href="http://test.com/x/d/?a=b&c=d">the link text!</a></p>',
            "[the link text!](http://test.com/x/d/?a=b&c=d)\n\n",
        ),
    ],
)
def test_html_to_markdown_links(html, result):
    assert pydevto.html_to_markdown(html) == result


@pytest.mark.parametrize(
    "html,result",
    [
        (
            '<img src="http://example.com/favicon.png">',
            "![](http://example.com/favicon.png)",
        ),
        (
            '<img alt="alt image" src="http://example.com/favicon.png">',
            "![alt image](http://example.com/favicon.png)",
        ),
        (
            '<img src="http://placekitten.com/200/300" alt="Small picture of a cat" /><figcaption>small caption</figcaption>',
            "![Small picture of a cat](http://placekitten.com/200/300)\n<figcaption>small caption</figcaption>\n",
        ),
    ],
)
def test_html_to_markdown_images(html, result):
    assert pydevto.html_to_markdown(html) == result


@pytest.mark.parametrize(
    "html,result",
    [
        (
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/kmjiUVEMvI4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            "\n{% youtube kmjiUVEMvI4 %}\n",
        ),
        (
               """<iframe height="400px" width="100%" src="https://repl.it/@WigWog/Practice-Problem-8?lite=true" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" sandbox="allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals"></iframe>""",
                "\n{% replit @WigWog/Practice-Problem-8 %}\n",
        ),
        (
            """<blockquote class="twitter-tweet"><p lang="en" dir="ltr">“That&#39;s here. That&#39;s home. That&#39;s us.” <br> <br>Observing Earth from space can alter an astronaut&#39;s perspective, a shift known as the “Overview Effect.” Described as a feeling of awe &amp; responsibility for 🌎, get a taste of it yourself w/ these stunning accounts: <a href="https://t.co/d2kb7Ld4SW">https://t.co/d2kb7Ld4SW</a> <a href="https://t.co/4ukVsN2P3r">pic.twitter.com/4ukVsN2P3r</a></p>&mdash; NASA (@NASA) <a href="https://twitter.com/NASA/status/1188230579646619649?ref_src=twsrc%5Etfw">October 26, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>""",
            "\n{% twitter 1188230579646619649 %}\n ",
        ),
    ],
)
def test_html_to_markdown_embeds(html, result):
    assert pydevto.html_to_markdown(html) == result

@pytest.mark.parametrize(
    "html,result",
    [
        (
                '<iframe width="560" height="315" src="https://www.example.com/unknown/embed?id=2"></iframe>',
                "\nhttps://www.example.com/unknown/embed?id=2\n",
        ),
    ],
)
def test_html_to_markdown_embeds_unknown(html, result):
    assert pydevto.html_to_markdown(html) == result

@pytest.mark.parametrize(
    "html,result",
    [
        (
                '<iframe src="https://cdn.unfurl.dev/embed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dl9nh1l8ZIJQ" frameborder="0" allowfullscreen="true" style="height: 412px;"></iframe>',
                "\n{% youtube l9nh1l8ZIJQ %}\n",
        ),
        (
                """<iframe src="https://cdn.unfurl.dev/embed?url=https%3A%2F%2Ftwitter.com%2FNASAVoyager%2Fstatus%2F1016476808638656521" frameborder="0" allowfullscreen="true" style="height: 556px;"></iframe>""",
                "\n{% twitter 1016476808638656521 %}\n",
        ),
        (
                """<iframe contenteditable="false" width="100%" src="https://cdn.unfurl.dev/embed?url=https%3A%2F%2Fcodepen.io%2Ftwhite96%2Fpen%2FXKqrJX" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="allowfullscreen" style="pointer-events: none; display: block; height: 412px;"></iframe>""",
                "\n{% codepen https://codepen.io/twhite96/pen/XKqrJX %}\n",
        ),
        (
                """<iframe contenteditable="false" width="100%" src="https://cdn.unfurl.dev/embed?url=https%3A%2F%2Fwww.instagram.com%2Fp%2FBXgGcAUjM39%2F" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="allowfullscreen" style="pointer-events: none; display: block; height: 996px;"></iframe>""",
                "\n{% instagram BXgGcAUjM39 %}\n",
        ),
        (
                """<iframe contenteditable="false" width="100%" src="https://cdn.unfurl.dev/embed?url=https%3A%2F%2Fsoundcloud.com%2Fblanc_de_noir%2Fsets%2Fglitched-love" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="allowfullscreen" style="pointer-events: none; display: block; height: 412px;"></iframe>""",
                "\n{% soundcloud https://soundcloud.com/blanc_de_noir/sets/glitched-love %}\n",
        ),
    ],
)
def test_html_to_markdown_embeds_unfurl(html, result):
    assert pydevto.html_to_markdown(html) == result

@pytest.mark.parametrize(
    "html,result",
    [
        (
                """<iframe class="embedly-embed" src="//cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fwww.youtube.com%2Fembed%2F7YpIumoM1Os%3Ffeature%3Doembed&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D7YpIumoM1Os&image=https%3A%2F%2Fi.ytimg.com%2Fvi%2F7YpIumoM1Os%2Fhqdefault.jpg&key=internal&type=text%2Fhtml&schema=youtube" width="500" height="281" scrolling="no" frameborder="0" allow="autoplay; fullscreen" allowfullscreen="true"></iframe>""",
                "\n{% youtube 7YpIumoM1Os %}\n",
        ),
    ],
)
def test_html_to_markdown_embedly(html, result):
    assert pydevto.html_to_markdown(html) == result
