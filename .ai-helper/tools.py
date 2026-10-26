"""
title: Staff Visualization Tool
author: Sammy Elfejji 
email: selfejji@camden.k12.ga.us
version: 0.1.0
required_open_webui_version: 0.10.2
description: Renders interactive HTML visualizations inline in chat.
"""

import re
import asyncio
from typing import Literal

# Build marker embedded into the rendered iframe so the running
# version can be verified at runtime (search DevTools for
# `data-iv-build` on <html>).  Keep in sync with the frontmatter version.
_IV_BUILD = "0.1.0"

from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Injected CSS — Theme variables (light default, dark via data-theme)
# ---------------------------------------------------------------------------
#
# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

THEME_CSS = """
"""

# ---------------------------------------------------------------------------
# Injected CSS — Base resets & interactive element styles
# ---------------------------------------------------------------------------
#
# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

BASE_STYLES = """
"""

# ---------------------------------------------------------------------------
# Injected JavaScript — theme detection (head), height reporting & bridges (body)
# ---------------------------------------------------------------------------
# Theme script runs in <head> before user content so CSS vars are resolved
# when model scripts read them at parse time.
#
# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

THEME_DETECTION_SCRIPT = """
"""

# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

BODY_SCRIPTS = """
"""

# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

STRICT_SAFETY_SCRIPT = """
"""

STREAMING_OBSERVER_SCRIPT = """
"""

# ---------------------------------------------------------------------------
# srcdoc safety guard
#
# Every constant listed in _IFRAME_EMBEDDED_SCRIPTS below is concatenated
# into an iframe's srcdoc. Once that srcdoc is parsed by the browser's
# HTML5 tokenizer, the script-data state machine is sensitive to the
# following literal byte sequences appearing ANYWHERE inside a script
# body (including inside JS comments and string literals):
#
#   <!--           triggers "script data escape start"
#   -->            exits  "script data escaped"
#   <![CDATA[      same family of escape transitions
#   ]]>            same
#   <script        in escaped state, triggers "script data double escape start"
#   </script>      in double-escaped state, exits back to escaped — does
#                  NOT terminate the outer script
#
# When any of these appears inside a script body — even commented out —
# the outer script's actual `</script>` tag stops terminating the
# script. The IIFE then either never executes or executes incompletely,
# producing the silent failure mode we hit in 2.1.0–2.1.2 (every
# debugging path looks normal in isolation, but tick never runs).
#
# Always build these tokens via string concatenation in JS — never
# write them as literals, not even inside comments. The guard below
# raises at module load time so the plugin refuses to import if anyone
# ever reintroduces one.
_FORBIDDEN_SRCDOC_LITERALS = (
    "<!--",
    "-->",
    "<![CDATA[",
    "]]>",
    "<script",
    "</script",
)

_IFRAME_EMBEDDED_SCRIPTS = {
    "THEME_DETECTION_SCRIPT": THEME_DETECTION_SCRIPT,
    "BODY_SCRIPTS": BODY_SCRIPTS,
    "CHIME_SCRIPT": CHIME_SCRIPT,
    "STRICT_SECURITY_SCRIPT": STRICT_SECURITY_SCRIPT,
    "STREAMING_OBSERVER_SCRIPT": STREAMING_OBSERVER_SCRIPT,
}
for _name, _body in _IFRAME_EMBEDDED_SCRIPTS.items():
    _assert_srcdoc_safe(_name, _body)

def _assert_srcdoc_safe(name: str, body: str) -> None:
    """Refuse to load if `body` contains any HTML token that would
    confuse the iframe srcdoc's script-data state machine.

    Each script body is allowed exactly ONE legitimate `<script>` and
    one `</script>` — the wrapping tags themselves. Anything beyond
    that count is a reintroduction of the bug fixed in 2.1.3.
    """

DOWNLOAD_BUTTON = (

)

# The strict and balanced tags interpolate the (constant) CDN allowlist, so
# assemble them once at import instead of rebuilding the string on every render.
_CSP_STRICT = ()

_CSP_BALANCED = ()

def _build_csp_tag(level: str) -> str:
    """Return a <meta> CSP tag for the given security level, or empty string.

    'unsafe-eval' is included because runtime expression compilers like
    Vega / Vega-Lite use new Function() internally and fail under
    strict CSP. 'unsafe-inline' is already present (inline scripts can
    execute arbitrary code), so adding 'unsafe-eval' does not
    meaningfully widen the attack surface — the real exfil blockers
    (connect-src, form-action, img-src, object-src) remain intact.
    """

def _build_html(
    security_level: str = "strict",
    title: str = "Visualization",
    chime: bool = True,
) -> str:
    """Wrap the streaming visualization shell: empty render area + observer.

    The observer tails the parent chat DOM for an ``@@@VIZ-START`` …
    ``@@@VIZ-END`` plain-text block in the assistant message and renders
    its contents live into #iv-render.
    """

    return (
        f'<!DOCTYPE html><html data-iv-lang="{safe_lang}" data-iv-build="{_IV_BUILD}"><head>'
        f"<title>{safe_title}</title>"
        f"{csp_tag}"
        f"<style>{THEME_CSS}\n{SVG_CLASSES}\n{BASE_STYLES}</style>"
        f'<script>try{{console.info("iv[build]","{_IV_BUILD}");}}catch(e){{}}</script>'
        f"{THEME_DETECTION_SCRIPT}"
        f"</head><body>\n{body_inner}\n</body></html>"
    )

class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints and descriptions

    async def hello_world(self, __event_emitter__ = None) -> str:
        """
        HTML code for a test webpage.
        """

        # Do not include a descrption for __user__ as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        result = """<!DOCTYPE html>
        <html>
            <head>
                <title>Hello World</title>
                <style>
                    body {
                        text-align: center;
                        margin-top: 20%;
                        font-family: Arial, sans-serif;
                    }
                    h1 {
                        font-size: 3em;
                        color: #333;
                    }
                </style>
            </head>
                <body>
                    <h1>Hello, World!</h1>
                </body>
            </html"""
        # Direct push to chat stream to force the Artifact panel to open
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "message",
                    "data": {"content": f"\n\n```html\n{result}\n```\n\n"},
                }
            )

        return "The workflow calculator HTML has been displayed to the user."
