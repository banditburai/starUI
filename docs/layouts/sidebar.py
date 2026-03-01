from typing import Any
from starhtml import *
from starhtml.datastar import js

# Cache sidebar nav to avoid rebuilding on every request
_SIDEBAR_NAV_CACHE = {}


def build_sidebar_nav(sections: list[dict[str, Any]] | None = None) -> FT:
    sections = sections or []
    cache_key = str(sections)
    
    if cache_key not in _SIDEBAR_NAV_CACHE:
        _SIDEBAR_NAV_CACHE[cache_key] = Nav(
            *[_sidebar_section(section) for section in sections],
            cls="grid items-start px-2 text-sm font-medium lg:px-4",
            aria_label="Components",
        )
    
    return _SIDEBAR_NAV_CACHE[cache_key]


def DocsSidebar(sections: list[dict[str, Any]] | None = None) -> FT:
    sections = sections or []
    nav_content = build_sidebar_nav(sections)

    return Div(
        Aside(
            Div(
                nav_content,
                cls="relative h-full py-2",
                style="overflow-y: auto; scrollbar-width: thin; scrollbar-color: transparent transparent;",
            ),
            cls="hidden xl:block xl:sticky xl:top-14 xl:w-64 xl:h-[calc(100vh-3.5rem)] xl:bg-background xl:border-r xl:border-border",
        ),
        Div(cls="hidden xl:block xl:w-64 xl:shrink-0"),
    )


def MobileSidebar(sections: list[dict[str, Any]] | None = None) -> FT:
    sections = sections or []
    nav_content = build_sidebar_nav(sections)
    
    return Div(
        nav_content,
        cls="px-4 pt-6 bg-background h-full overflow-y-auto",
    )


def _sidebar_section(section: dict[str, Any]) -> FT:
    section_title = section.get("title", "Unknown")
    section_key = (section_title, tuple(str(item.get("href", "#")) for item in section.get("items", [])))

    if not hasattr(_sidebar_section, '_cache'):
        _sidebar_section._cache = {}

    if section_key in _sidebar_section._cache:
        return _sidebar_section._cache[section_key]

    result = Div(
        H4(
            section.get("title", ""),
            cls="mb-4 px-2 text-sm font-semibold text-foreground"
        ) if section.get("title") else None,
        Div(
            *[_sidebar_item(item) for item in section.get("items", [])],
            cls="flex flex-col items-start text-sm mb-6 space-y-1"
        )
    )

    _sidebar_section._cache[section_key] = result
    return result


def _sidebar_item(item: dict[str, Any]) -> FT:
    href = item.get("href", "#")

    if item.get("disabled", False):
        return Span(
            item.get("label", ""),
            cls="inline-flex items-center rounded-md px-2 py-1.5 text-sm text-muted-foreground cursor-not-allowed opacity-60"
        )

    sidebar_active = Signal("sidebar_active", _ref_only=True)

    return A(
        item.get("label", ""),
        href=href,
        cls="inline-flex items-center rounded-md px-2 py-1.5 text-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        data_attr_cls=sidebar_active.eq(href).if_(
            "bg-accent text-accent-foreground font-medium",
            "text-muted-foreground"
        )
    )