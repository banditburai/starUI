from typing import Any
from dataclasses import dataclass, field
from starhtml import *
from starhtml.datastar import ds_on_click, ds_signals, ds_text, ds_show
from layouts.footer import DocsFooter
from layouts.header import DocsHeader
from layouts.sidebar import DocsSidebar, MobileSidebar
from layouts.navigation import TopNavigation, BottomNavigation
from starui.registry.components.breadcrumb import (
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
)
from starui.registry.components.button import Button
from starui.registry.components.sheet import Sheet, SheetContent, SheetClose


@dataclass
class LayoutConfig:
    title: str = ""
    description: str = ""
    breadcrumb_items: list[dict[str, Any]] | None = None
    prev_page: dict[str, str] | None = None
    next_page: dict[str, str] | None = None
    show_copy: bool = True
    show_sidebar: bool = True
    show_footer: bool = True
    max_width: str = "screen-2xl"
    container_class: str = ""
    content_class: str = ""
    class_name: str = ""
    component_name: str | None = None


@dataclass
class HeaderConfig:
    logo_text: str = "starui"
    logo_href: str = "/"
    nav_items: list[dict[str, Any]] = field(default_factory=lambda: [
        {"href": "/docs", "label": "Docs"},
        {"href": "/components", "label": "Components"},
        {"href": "/blocks", "label": "Blocks"},
        {"href": "/themes", "label": "Themes"},
    ])
    github_stars: str = "star us"
    show_search: bool = True
    show_github: bool = True
    show_theme_toggle: bool = True


@dataclass
class FooterConfig:
    attribution: str = "Built with StarHTML"
    hosting_info: str = "Component library for Python web apps"
    source_text: str = "The source code is available on GitHub"
    source_href: str = "https://github.com/banditburai/starui"
    links: list[dict[str, Any]] | None = None


@dataclass
class SidebarConfig:
    sections: list[dict[str, Any]] | None = None


def _copy_page_button(component_name: str | None = None) -> FT:
    """Create the copy page button with clipboard functionality for markdown content."""
    # If we have a component name, fetch markdown from API; otherwise copy URL
    if component_name:
        copy_action = f"fetch('/api/markdown/{component_name}').then(r => r.json()).then(data => @clipboard(data.markdown, 'page_copied', 2000)).catch(() => @clipboard(window.location.href, 'page_copied', 2000))"
    else:
        copy_action = "@clipboard(window.location.href, 'page_copied', 2000)"
    
    return Button(
        Span(
            Icon("lucide:check", cls="h-4 w-4"),
            ds_show("$page_copied")
        ),
        Span(
            Icon("lucide:copy", cls="h-4 w-4"),
            ds_show("!$page_copied")
        ),
        "Copy Page",
        ds_on_click(copy_action),
        ds_signals(page_copied=False),
        variant="outline",
        size="sm",
        cls="h-8 rounded-md gap-1.5 px-3"
    )


def _page_header_section(layout: LayoutConfig) -> FT:
    """Create the page header section with title, description, and copy/navigation buttons."""
    if not layout.title:
        return None
    
    return Div(
        Div(
            H1(layout.title, cls="scroll-m-20 text-4xl font-semibold tracking-tight"),
            Div(
                _copy_page_button(layout.component_name) if layout.show_copy else None,
                TopNavigation(layout.component_name) if layout.component_name else None,
                cls="flex items-center gap-3"
            ),
            cls="flex items-center justify-between"
        ),
        P(layout.description, cls="text-muted-foreground mt-2") if layout.description else None,
        cls="pb-8 pt-6 md:pb-10 md:pt-10 lg:py-10"
    )


def _main_content_area(content: tuple, layout: LayoutConfig) -> FT:
    """Create the main content area with breadcrumbs, header, content, and navigation."""
    return Div(
        _breadcrumb(layout.breadcrumb_items) if layout.breadcrumb_items else None,
        _page_header_section(layout),
        Div(
            *content,
            cls=f"max-w-full overflow-x-hidden {layout.content_class}"
        ),
        BottomNavigation(layout.component_name) if layout.component_name else None,
        cls=f"w-full max-w-full mx-auto px-8 sm:px-12 md:px-16 lg:px-20 xl:px-24 py-6 lg:py-8 {layout.container_class}"
    )


def _mobile_sheet_section(sidebar: SidebarConfig) -> FT:
    """Create the mobile menu sheet for sidebar navigation."""
    return Sheet(
        SheetContent(
            MobileSidebar(sections=sidebar.sections),
            signal="mobile_menu",
            side="right",
            size="sm",
            cls="xl:hidden w-80 max-w-[80vw] p-0",
            show_close=True,
        ),
        signal="mobile_menu",
        modal=True,
    )


def _layout_with_sidebar(
    main_content: FT,
    sidebar: SidebarConfig,
    layout: LayoutConfig,
    **attrs
) -> FT:
    """Create layout wrapper with mobile sidebar sheet."""
    return Div(
        main_content,
        _mobile_sheet_section(sidebar),
        cls=f"flex min-h-screen flex-col {layout.class_name}",
        **attrs
    )


def _main_layout_structure(
    content: tuple,
    layout: LayoutConfig,
    header: HeaderConfig,
    footer: FooterConfig,
    sidebar: SidebarConfig,
    show_sidebar: bool,
    **attrs
) -> FT:
    """Create the main layout structure with header, content, and footer."""
    return Div(
        DocsHeader(header, show_mobile_menu_button=show_sidebar),
        Div(
            DocsSidebar(sections=sidebar.sections) if show_sidebar else None,
            Main(
                _main_content_area(content, layout),
                cls="flex-1 overflow-x-hidden"
            ),
            cls="flex min-h-[calc(100vh-3.5rem)]"
        ),
        DocsFooter(
            attribution=footer.attribution,
            hosting_info=footer.hosting_info,
            source_text=footer.source_text,
            source_href=footer.source_href,
            links=footer.links,
        ) if layout.show_footer else None,
        cls=f"flex min-h-screen flex-col {layout.class_name}",
        **attrs
    )


def DocsLayout(
    *content,
    layout: LayoutConfig | None = None,
    header: HeaderConfig | None = None,
    footer: FooterConfig | None = None,
    sidebar: SidebarConfig | None = None,
    **attrs,
) -> FT:
    """Create a documentation layout with optional sidebar, header, and footer."""
    layout = layout or LayoutConfig()
    header = header or HeaderConfig()
    footer = footer or FooterConfig()
    sidebar = sidebar or SidebarConfig()
    
    show_sidebar = layout.show_sidebar and sidebar.sections is not None

    main_content = _main_layout_structure(
        content, layout, header, footer, sidebar, show_sidebar, **attrs
    )

    if show_sidebar:
        return _layout_with_sidebar(main_content, sidebar, layout, **attrs)
    else:
        return main_content


def _breadcrumb(items: list[dict[str, Any]]) -> FT:
    breadcrumb_items = []
    for i, item in enumerate(items):
        breadcrumb_items.append(
            BreadcrumbItem(
                BreadcrumbLink(item["label"], href=item.get("href", "#"))
                if not item.get("active")
                else BreadcrumbPage(item["label"])
            )
        )
        if i < len(items) - 1:
            breadcrumb_items.append(BreadcrumbSeparator())
    
    return Breadcrumb(
        BreadcrumbList(*breadcrumb_items),
        cls="mb-4"
    )


