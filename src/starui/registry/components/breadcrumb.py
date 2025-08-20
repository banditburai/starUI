from starhtml import FT, A, Icon, Li, Nav, Ol, Span

from .utils import cn


def Breadcrumb(*children, class_name: str = "", cls: str = "", **attrs) -> FT:
    return Nav(
        *children,
        aria_label="breadcrumb",
        data_slot="breadcrumb",
        cls=cn("", class_name, cls),
        **attrs,
    )


def BreadcrumbList(*children, class_name: str = "", cls: str = "", **attrs) -> FT:
    return Ol(
        *children,
        data_slot="breadcrumb-list",
        cls=cn(
            "text-muted-foreground flex flex-wrap items-center gap-1.5 text-sm break-words sm:gap-2.5",
            class_name,
            cls,
        ),
        **attrs,
    )


def BreadcrumbItem(*children, class_name: str = "", cls: str = "", **attrs) -> FT:
    return Li(
        *children,
        data_slot="breadcrumb-item",
        cls=cn("inline-flex items-center gap-1.5", class_name, cls),
        **attrs,
    )


def BreadcrumbLink(
    *children, href: str = "#", class_name: str = "", cls: str = "", **attrs
) -> FT:
    return A(
        *children,
        href=href,
        data_slot="breadcrumb-link",
        cls=cn("hover:text-foreground transition-colors", class_name, cls),
        **attrs,
    )


def BreadcrumbPage(*children, class_name: str = "", cls: str = "", **attrs) -> FT:
    return Span(
        *children,
        role="link",
        aria_disabled="true",
        aria_current="page",
        data_slot="breadcrumb-page",
        cls=cn("text-foreground font-normal", class_name, cls),
        **attrs,
    )


def BreadcrumbSeparator(*children, class_name: str = "", cls: str = "", **attrs) -> FT:
    separator_content = children if children else (Icon("lucide:chevron-right"),)

    return Li(
        *separator_content,
        role="presentation",
        aria_hidden="true",
        data_slot="breadcrumb-separator",
        cls=cn("[&>svg]:size-3.5", class_name, cls),
        **attrs,
    )


def BreadcrumbEllipsis(class_name: str = "", cls: str = "", **attrs) -> FT:
    return Span(
        Icon("lucide:more-horizontal", cls="size-4"),
        Span("More", cls="sr-only"),
        role="presentation",
        aria_hidden="true",
        data_slot="breadcrumb-ellipsis",
        cls=cn("flex size-9 items-center justify-center", class_name, cls),
        **attrs,
    )
