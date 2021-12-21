import os

from aqt.webview import AnkiWebView
from aqt import gui_hooks, mw
from typing import Callable

originalSetHtml: Callable = AnkiWebView.setHtml
config = mw.addonManager.getConfig(__name__)


def enable_deckbrowser_css(*argv):
    AnkiWebView.setHtml = setHtml


def setHtml(self: AnkiWebView, html: str) -> None:
    global originalSetHtml
    if config["overrideOriginal"]:
        html.replace(self.bundledCSS("css/deckbrowser.css"), "")

    addon_dir = os.path.dirname(os.path.abspath(__file__))

    with open(addon_dir + config["cssPath"]) as f:
        lines = "<style>\n" + f.read() + "\n</style>\n"
        idx = html.index("</head>")
        html = html[:idx] + lines + html[idx:]

    originalSetHtml(self, html)
    AnkiWebView.setHtml = originalSetHtml


gui_hooks.deck_browser_will_render_content.append(enable_deckbrowser_css)
