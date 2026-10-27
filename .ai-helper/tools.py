"""
title: Staff Visualization Tool
author: Sammy Elfejji 
email: selfejji@camden.k12.ga.us
version: 0.1.0
required_open_webui_version: 0.10.2
description: Renders interactive HTML visualizations inline in chat.
disclaimer: All Scripts and CSS blocks commented-out can be found in ../ai-helper/..
"""

import html
from typing import Literal
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Build marker embedded into the rendered iframe so the running
# version can be verified at runtime.
# (search `data-iv-build` on <html>).  
_IV_BUILD = "0.1.0"

# ---------------------------------------------------------------------------
# Injected CSS — Theme variables (light default, dark via data-theme)
# ---------------------------------------------------------------------------

THEME_CSS = """
"""

# ---------------------------------------------------------------------------
# Injected CSS — Base resets & interactive element styles
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Happy chime on stream completion
# ---------------------------------------------------------------------------
# Injected into BODY_SCRIPTS via a /*__CHIME_BLOCK__*/ placeholder so the
# ``chime`` valve can strip it out entirely when disabled — no bytes
# shipped. finalize() calls playDoneSound() inside
# a ``typeof playDoneSound === 'function'`` guard, so omission is safe.
# ---------------------------------------------------------------------------
#
# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

CHIME_SCRIPT = """
// --- Happy chime ---
// C-major arpeggio (C5 → E5 → G5) on sine oscillators with exponential
// decay. ~300 ms, gentle volume. Silent no-op if AudioContext is still
// suspended (no prior user gesture).
var _ivAudioCtx = null;

function playDoneSound() {
  try {
    var AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    if (!_ivAudioCtx) _ivAudioCtx = new AudioCtx();

    var ctx = _ivAudioCtx;
    if (ctx.state === 'suspended') { try { ctx.resume(); } catch(e) {} }

    var now = ctx.currentTime;
    var notes = [523.25, 659.25, 783.99]; // C5, E5, G5
    notes.forEach(function(freq, i) {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      var start = now + i * 0.09;
      var duration = 0.35;
      
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.exponentialRampToValueAtTime(0.16, start + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
      osc.connect(gain).connect(ctx.destination);
      osc.start(start);
      osc.stop(start + duration + 0.02);
    });
  } catch(e) {}
}
"""

# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

BODY_SCRIPTS = """
"""

# --------------------------------------------------------------------------- 
# Developer Reference
#
# This serves as a standard security script for HTML injections by the agent into the DOM.
# As of version 0.1.0 there is only an "offline" security level with no CDN's.
# In later versions, if outbound CDN requests permits, this security script can
# also accomidate varrying security levels such as "strict" that allow for CDNs.
# 
# It is crucial to have URL sanitization and interception so no URLs can be injected
# that carry-out unwanted web traffic that may expose sensitive data and tokens.
# ---------------------------------------------------------------------------
#
# !! SRCDOC SAFETY !!  Do NOT write the literal tokens <!-- , --> ,
# <![CDATA[ , ]]> , <script> or </script> ANYWHERE in this body —
# not even inside JS comments. See THEME_DETECTION_SCRIPT for full rationale.

STRICT_SECURITY_SCRIPT = """
// ---------------------------------------------------------------------------
// Outer IIFE (Scope Protection) ensures private scope from global window pollution
// ---------------------------------------------------------------------------

(function() {
    // URL Cleaner: uses browsers built-in URL object to parse the link and clear the query string
    function stripParams(rawUrl) {
        try { 
            // Get window URL
            var parsed = new URL(rawUrl, location.href); 

            // Clears query string
            parsed.search = ''; 

            return parsed.toString(); 
        } catch(e) { 
            return rawUrl; 
        }
    }

    // ---------------------------------------------------------------------------
    // Monkey-Patching Navigation (window.openLink and window.open)
    // --------------------------------------------------------------------------- 
    //
    // Captures the browsers functions (_origOpenLink and _origOpen) and overrides them.
    // Uses stripParams to sanitize.

    // Override openLink to strip query/hash parameters
    var _origOpenLink = window.openLink;

    window.openLink = function(url) {
        _origOpenLink(stripParams(url));
    };

    // Override window.open to strip query parameters
    var _origOpen = window.open;

    window.open = function(url) {
        arguments[0] = stripParams(url);
        return _origOpen.apply(this, arguments);
    };

    // Serves as an initial DOM cleanup.
    // Strip params from all existing and future <a> tags with href attribute
    function sanitizeLinks(root) {
        (root.querySelectorAll ? root : document).querySelectorAll('a[href]').forEach(function(anchor) {
            anchor.href = stripParams(anchor.href);
        });
    }


    // Dynamic Monitoring (MutationObserver) monitors the webpage for newly
    // inserted HTML nodes and automatically strips query params for new <a> tags
    // as soon as they appear in DOM

    sanitizeLinks(document);

    // Creates new instance of MutationObserver
    new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {  
                if (node.nodeType === 1) sanitizeLinks(node); 
            });
        });
    }).observe(document.body, { childList: true, subtree: true });
})();
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
# script. The IIFE then either never executes or executes incompletely.
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

# ---------------------------------------------------------------------------
# Crucial function for preventing unwanted tag injections that break srcdoc
# ---------------------------------------------------------------------------

def _assert_srcdoc_safe(name: str, body: str) -> None:
    """Refuse to load if `body` contains any HTML token that would
    confuse the iframe srcdoc's script-data state machine.

    Each script body is allowed exactly ONE legitimate `<script>` and
    one `</script>` — the wrapping tags themselves.
    """

    # Calculates the count of each open and close tag in the body of code block
    open_script_tag_count = body.count("<script")
    close_script_tag_count = body.count("</script")

    # Logic for raising exception for more then one tag
    if open_script_tag_count > 1 or close_script_tag_count > 1:
        raise RuntimeError(
            f"Inline Visualizer: {name} contains an extra <script> or "
            f"</script> literal (open={open_script_tag_count}, close={close_script_tag_count}). "
            "These break HTML5 srcdoc parsing — build them via string "
            "concatenation in JS instead."
        )

    # Searches body for forbidden srcdoc literals excluding <script and </script 
    for x in ("<!--", "-->", "<![CDATA[", "]]>"):
        if x in body:
            raise RuntimeError(
                f"Inline Visualizer: {name} contains a literal {x!r}. "
                "This puts the iframe srcdoc parser into script-data-escape "
                "mode and silently breaks the IIFE. Concatenate it in JS "
                "instead, even inside comments."
            )

_IFRAME_EMBEDDED_SCRIPTS = {
    "THEME_DETECTION_SCRIPT": THEME_DETECTION_SCRIPT,
    "BODY_SCRIPTS": BODY_SCRIPTS,
    "CHIME_SCRIPT": CHIME_SCRIPT,
    "STRICT_SECURITY_SCRIPT": STRICT_SECURITY_SCRIPT,
}

# Runs srcdoc safety for each script
for _name, _body in _IFRAME_EMBEDDED_SCRIPTS.items():
    _assert_srcdoc_safe(_name, _body)


def _build_csp_tag(level: str) -> str:
    # Return a <meta> CSP tag for the given security level, or empty string.

    if level == "none":
        return ""

    if level == "offline":
        return (
            '<meta http-equiv="Content-Security-Policy" content="'
            "default-src 'self'; "
            "script-src 'unsafe-inline' 'unsafe-eval' 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "connect-src 'none'; "
            "form-action 'none'; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data:; "
            "media-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            '">'
        )

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
    csp_tag = _build_csp_tag(security_level)
    strict_script = (
        STRICT_SECURITY_SCRIPT if security_level in ("offline") else ""
    )

    # Title sanitization that prevents cross-site scripting (XSS) and layout errors
    # Performs replacements for special chars: &, <, >, ", '
    # Imported function acts a a concatenation of title.replace("&", "&amp")
    safe_title = html.escape(title)

    # Strip the chime script entirely when the valve is off — no bytes
    # shipped, no defined playDoneSound in the iframe. 
    body_scripts = BODY_SCRIPTS.replace(
        "/*__CHIME_BLOCK__*/", CHIME_SCRIPT if chime else ""
    )

    # Loader sits *below* the render area so content appears to flow
    # downward toward the pulsing dots — like a cursor following a pen.
    body_inner = (
        '<div id="iv-render"></div>\n'
        '<div id="iv-loader" class="iv-loading" aria-live="polite">'
        '<div class="iv-loading-dots"><span></span><span></span><span></span></div>'
        '<div class="iv-loading-label">Rendering visualization\u2026</div>'
        "</div>\n"
        f"{body_scripts}"
        f"{strict_script}"
    )


    return (
        f'<!DOCTYPE html><html data-iv-build="{_IV_BUILD}"><head>'
        f"<title>{safe_title}</title>"
        f"{csp_tag}"
        f"<style>{THEME_CSS}\n{BASE_STYLES}</style>"
        f'<script>try{{console.info("iv[build]","{_IV_BUILD}");}}catch(e){{}}</script>'
        f"{THEME_DETECTION_SCRIPT}"
        f"</head><body>\n{body_inner}\n</body></html>"
    )

# ---------------------------------------------------------------------------
# Valves (user-configurable settings)
# ---------------------------------------------------------------------------

# Developer reference for security levels 
#
#   OFFLINE  — Nothing leaves the Open WebUI host. 
#              'self' is only allowed. External scripts, images, fonts
#              and media are all blocked; only same-origin, data: and
#              blob: sources load. For air-gapped / privacy-hardened
#              deployments. (You are welcome Timothy lol)

class Tools:
    """Inline Visualizer — renders interactive HTML in chat.

    Security is controlled via the ``security_level`` valve, which applies
    a Content Security Policy to the rendered iframe. OFFLINE permits 
    zero external connections (self-hosted libraries under the instance's 
    /static directory still load). Script execution is always permitted — 
    it is required for interactive visualizations. See the developer reference above
    for the full security model and its limitations.
    """
    def __init__(self):
        pass
