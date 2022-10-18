import os
from anki.hooks import wrap
from aqt.webview import AnkiWebView
from aqt import gui_hooks, mw, toolbar
from typing import Callable

originalSetHtml: Callable = AnkiWebView.setHtml
config = mw.addonManager.getConfig(__name__)

useDeckBrowser = True

def enable_deckbrowser_css(*argv):
    global useDeckBrowser
    useDeckBrowser = True
    AnkiWebView.setHtml = setHtml

def enable_toolbar_css(*argv):
    global useDeckBrowser
    useDeckBrowser = False
    AnkiWebView.setHtml = setHtml

def setHtml(self: AnkiWebView, html: str) -> None:
    global originalSetHtml
    global useDeckBrowser
    if config["overrideOriginal"]:
        html.replace(self.bundledCSS("css/deckbrowser.css"), "")

    addon_dir = os.path.dirname(os.path.abspath(__file__))

    with open(addon_dir + config["cssPath" if useDeckBrowser else "toolbarCssPath"]) as f:
        lines = "<style>\n" + f.read() + "\n</style>\n"
        idx = html.index("</head>")
        html = html[:idx] + lines + html[idx:]

    originalSetHtml(self, html)
    AnkiWebView.setHtml = originalSetHtml

toolbar.Toolbar.draw = wrap(toolbar.Toolbar.draw, enable_toolbar_css, "before")
gui_hooks.deck_browser_will_render_content.append(enable_deckbrowser_css)
