from typing import Any
from dataclasses import dataclass, field
from starhtml import *
from starhtml.datastar import clipboard
from layouts.footer import DocsFooter
from layouts.header import DocsHeader
from layouts.sidebar import DocsSidebar, MobileSidebar
from layouts.navigation import TopNavigation, BottomNavigation
from starui.registry.components.button import Button
from starui.registry.components.sheet import Sheet, SheetContent, SheetClose


@dataclass
class LayoutConfig:
    title: str = ""
    description: str = ""
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
    copy_action = (
        f"fetch('/api/markdown/{component_name}').then(r => r.json()).then(data => @clipboard(data.markdown, 'page_copied', 2000)).catch(() => @clipboard(window.location.href, 'page_copied', 2000))"
        if component_name
        else "@clipboard(window.location.href, 'page_copied', 2000)"
    )

    return Button(
        (page_copied := Signal("page_copied", False)),
        Span(
            Icon("lucide:check", cls="h-4 w-4"),
            data_show=page_copied
        ),
        Span(
            Icon("lucide:copy", cls="h-4 w-4"),
            data_show=~page_copied
        ),
        "Copy Page",
        data_on_click=copy_action,
        variant="outline",
        size="sm",
        cls="h-8 rounded-md gap-1.5 px-3"
    )


def _page_header_section(layout: LayoutConfig) -> FT:
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
    return Div(
        _page_header_section(layout),
        Div(
            *content,
            cls=f"max-w-full overflow-x-hidden {layout.content_class}"
        ),
        BottomNavigation(layout.component_name) if layout.component_name else None,
        cls=f"w-full max-w-full mx-auto px-8 sm:px-12 md:px-16 lg:px-20 xl:px-24 py-6 lg:py-8 {layout.container_class}"
    )


def _mobile_sheet_section(sidebar: SidebarConfig) -> FT:
    return Sheet(
        SheetContent(
            MobileSidebar(sections=sidebar.sections),
            signal="mobile_menu_open",
            side="right",
            size="sm",
            cls="xl:hidden w-80 max-w-[80vw] p-0",
            show_close=True,
        ),
        signal="mobile_menu_open",
        modal=True,
        default_open=False,
    )


def _layout_with_sidebar(
    main_content: FT,
    sidebar: SidebarConfig,
    layout: LayoutConfig,
    **attrs
) -> FT:
    Signal("sidebar_active", _ref_only=True)
    return Div(
        main_content,
        _mobile_sheet_section(sidebar),
        cls=f"flex min-h-screen flex-col {layout.class_name}",
        data_effect="$sidebar_active = location.pathname",
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
    layout = layout or LayoutConfig()
    header = header or HeaderConfig()
    footer = footer or FooterConfig()
    sidebar = sidebar or SidebarConfig()
    
    show_sidebar = layout.show_sidebar and sidebar.sections is not None

    main_content = _main_layout_structure(
        content, layout, header, footer, sidebar, show_sidebar, **attrs
    )

    return _layout_with_sidebar(main_content, sidebar, layout, **attrs) if show_sidebar else main_content




