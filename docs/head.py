"""Global <head> elements for star_app(hdrs=...).

Centralizes favicon, theme-color, structured data, fonts, and stylesheets.
"""

from starhtml import JsonLd, Link, Meta, theme_script

SITE_URL = "https://ui.starhtml.com"

_JSONLD_DICT = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "StarUI",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "Any",
    "description": (
        "Python-first UI component library for StarHTML applications. "
        "The shadcn/ui model, rebuilt for Python — 34+ accessible, "
        "copy-paste components powered by Tailwind v4 and Datastar."
    ),
    "url": SITE_URL,
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD",
        "description": "Open source, Apache 2.0 license",
    },
    "publisher": {
        "@type": "Organization",
        "name": "StarUI",
        "url": SITE_URL,
    },
}


def _build_hdrs() -> tuple:
    return (
        theme_script(use_data_theme=True),

        # Favicon — SVG with light/dark media queries
        Link(rel="icon", type="image/svg+xml", href="/static/images/favicon-dark.svg",
             media="(prefers-color-scheme: light)"),
        Link(rel="icon", type="image/svg+xml", href="/static/images/favicon-light.svg",
             media="(prefers-color-scheme: dark)"),
        Link(rel="apple-touch-icon", href="/static/images/apple-touch-icon.png"),

        Meta(name="theme-color", content="#0B1221"),

        # Stylesheets
        Link(rel="stylesheet", href="/static/css/starui.css"),

        # Fonts
        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?"
                 "family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400"
                 "&family=Inter:wght@200;300;400"
                 "&family=Playfair+Display:ital,wght@0,400;0,500;1,400"
                 "&display=swap",
        ),

        JsonLd(_JSONLD_DICT),
    )


hdrs = _build_hdrs()
