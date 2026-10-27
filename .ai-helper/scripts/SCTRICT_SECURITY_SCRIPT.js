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
                if (node.nodeType === 1) 
                    sanitizeLinks(node); 
            });
        });
    }).observe(document.body, { childList: true, subtree: true });
})();
