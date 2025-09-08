from typing import Any
from starhtml import *
from starui.registry.components.theme_toggle import ThemeToggle
from starui.registry.components.button import Button
from starui.registry.components.popover import Popover, PopoverTrigger, PopoverContent


def MobileMenuButton(**attrs) -> FT:
    from starui.registry.components.sheet import SheetTrigger
    
    return SheetTrigger(
        Icon("ph:list-bold", width="20", height="20"),
        signal="mobile_menu",
        variant="ghost",
        cls="xl:hidden h-9 px-4 py-2 flex-shrink-0",
        aria_label="Toggle mobile menu",
        **attrs,
    )


def _search_button() -> FT:
    """Create the search button with keyboard shortcuts."""
    return Button(
        Icon("lucide:search", cls="w-4 h-4 shrink-0"),
        Span("Search...", cls="text-sm text-muted-foreground"),
        Div(
            Kbd("⌘", cls="pointer-events-none inline-flex h-4 select-none items-center gap-1 rounded border bg-muted px-1 font-mono text-[10px] font-medium text-muted-foreground"),
            Kbd("K", cls="pointer-events-none inline-flex h-4 select-none items-center gap-1 rounded border bg-muted px-1 font-mono text-[10px] font-medium text-muted-foreground"),
            cls="hidden lg:flex gap-1"
        ),
        cls="inline-flex items-center h-8 min-w-32 max-w-48 md:max-w-64 justify-start bg-muted/50 hover:bg-muted/80 gap-2 px-3 rounded-md",
        variant="ghost",
    )


def _github_dropdown(github_stars: str) -> FT:
    """Create a minimal GitHub dropdown matching docs style."""
    return Popover(
        PopoverTrigger(
            Icon("lucide:star", width="16", height="16"),
            Span(github_stars, cls="hidden lg:inline-block text-sm"),
            Icon("lucide:chevron-down", width="12", height="12", cls="ml-1 transition-transform duration-200 group-data-[state=open]:rotate-180"),
            variant="ghost",
            cls="h-9 px-3 py-2 gap-1.5 group"
        ),
        PopoverContent(
            Div(
                A(
                    Div(
                        Span("starHTML", cls="font-medium"),
                        Span("Python web framework", cls="text-xs text-muted-foreground"),
                        cls="flex flex-col"
                    ),
                    href="https://github.com/banditburai/starhtml",
                    target="_blank",
                    rel="noopener noreferrer",
                    cls="flex items-center gap-2 p-2 rounded-md hover:bg-accent transition-colors"
                ),
                A(
                    Div(
                        Span("starUI", cls="font-medium"),
                        Span("Component library", cls="text-xs text-muted-foreground"),
                        cls="flex flex-col"
                    ),
                    href="https://github.com/banditburai/starui",
                    target="_blank",
                    rel="noopener noreferrer",
                    cls="flex items-center gap-2 p-2 rounded-md hover:bg-accent transition-colors"
                ),
                cls="space-y-1"
            ),
            side="bottom",
            align="end",
            cls="p-2",
            style="width: 180px;"
        ),
        cls="relative"
    )


def _navigation_menu(nav_items: list[dict[str, Any]]) -> FT:
    """Create the desktop navigation menu."""
    return Nav(
        *[
            A(
                item["label"],
                href=item["href"],
                cls="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring h-9 px-4 py-2 text-foreground/60 hover:text-foreground/80"
            )
            for item in nav_items
        ],
        cls="hidden xl:flex items-center gap-4 text-sm xl:gap-6",
    )


def _header_actions(
    show_search: bool,
    show_github: bool,
    show_theme_toggle: bool,
    show_mobile_menu_button: bool,
    github_stars: str
) -> FT:
    """Create the header action buttons section."""
    return Div(
        _search_button() if show_search else "",
        _github_dropdown(github_stars) if show_github else "",
        ThemeToggle() if show_theme_toggle else "",
        MobileMenuButton() if show_mobile_menu_button else "",
        cls="flex items-center gap-2 flex-shrink-0",
    )


def DocsHeader(config: "HeaderConfig", show_mobile_menu_button: bool = False, **attrs) -> FT:
    """Create a documentation header with logo, navigation, and action buttons."""
    from layouts.base import HeaderConfig
    
    return Header(
        Div(
            Div(
                A(config.logo_text, href=config.logo_href, cls="mr-4 flex items-center space-x-2 lg:mr-6"),
                _navigation_menu(config.nav_items),
                cls="flex items-center",
            ),
            _header_actions(
                config.show_search, config.show_github, config.show_theme_toggle, 
                show_mobile_menu_button, config.github_stars
            ),
            cls="flex h-14 w-full items-center justify-between px-4 sm:px-6 md:px-8 lg:px-6 max-w-full mx-auto",
        ),
        cls="sticky top-0 z-50 w-full border-b border-border bg-background",
        style="will-change: transform; transform: translateZ(0); backface-visibility: hidden;",
        **attrs
    )