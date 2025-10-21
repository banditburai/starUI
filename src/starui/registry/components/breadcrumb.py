from starhtml import FT, Icon
from starhtml import A as HTMLA
from starhtml import Li as HTMLLi
from starhtml import Nav as HTMLNav
from starhtml import Ol as HTMLOl
from starhtml import Span as HTMLSpan

from .utils import cn


def Breadcrumb(*children, cls: str = "", **kwargs) -> FT:
    return HTMLNav(
        *children,
        aria_label="breadcrumb",
        cls=cls,
        **kwargs,
    )


def BreadcrumbList(*children, cls: str = "", **kwargs) -> FT:
    return HTMLOl(
        *children,
        cls=cn(
            "text-muted-foreground flex flex-wrap items-center gap-1.5 text-sm break-words sm:gap-2.5",
            cls,
        ),
        **kwargs,
    )


def BreadcrumbItem(*children, cls: str = "", **kwargs) -> FT:
    return HTMLLi(
        *children,
        cls=cn("inline-flex items-center gap-1.5", cls),
        **kwargs,
    )


def BreadcrumbLink(
    *children, href: str = "#", cls: str = "", **kwargs
) -> FT:
    return HTMLA(
        *children,
        href=href,
        cls=cn("hover:text-foreground transition-colors", cls),
        **kwargs,
    )


def BreadcrumbPage(*children, cls: str = "", **kwargs) -> FT:
    return HTMLSpan(
        *children,
        role="link",
        aria_disabled="true",
        aria_current="page",
        cls=cn("text-foreground font-normal", cls),
        **kwargs,
    )


def BreadcrumbSeparator(*children, cls: str = "", **kwargs) -> FT:
    return HTMLLi(
        *(children or (Icon("lucide:chevron-right"),)),
        role="presentation",
        aria_hidden="true",
        cls=cn("[&_svg]:size-3.5 [&_iconify-icon]:size-3.5 [&>span]:size-3.5", cls),
        **kwargs,
    )


def BreadcrumbEllipsis(cls: str = "", **kwargs) -> FT:
    return HTMLSpan(
        Icon("lucide:more-horizontal", cls="size-4"),
        HTMLSpan("More", cls="sr-only"),
        role="presentation",
        aria_hidden="true",
        cls=cn("flex size-9 items-center justify-center", cls),
        **kwargs,
    )
