from typing import Literal

from starhtml import FT, Div, P
from starhtml import H1 as HTMLH1
from starhtml import H2 as HTMLH2
from starhtml import H3 as HTMLH3
from starhtml import H4 as HTMLH4
from starhtml import H5 as HTMLH5
from starhtml import H6 as HTMLH6

from .utils import cn

HeadingLevel = Literal["h1", "h2", "h3", "h4", "h5", "h6"]

_HEADING_COMPONENTS = {
    "h1": HTMLH1,
    "h2": HTMLH2,
    "h3": HTMLH3,
    "h4": HTMLH4,
    "h5": HTMLH5,
    "h6": HTMLH6,
}


def Card(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children, 
        cls=cn(
            "bg-card text-card-foreground flex flex-col gap-6 rounded-xl border py-6 shadow-sm",
            class_name,
            cls,
        ), 
        data_slot="card", 
        **kwargs
    )


def CardHeader(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children, 
        cls=cn(
            "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
            class_name,
            cls,
        ), 
        data_slot="card-header", 
        **kwargs
    )


def CardTitle(
    *children,
    level: HeadingLevel = "h3",
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    Heading = _HEADING_COMPONENTS[level]
    return Heading(
        *children, 
        cls=cn("leading-none font-semibold", class_name, cls), 
        data_slot="card-title", 
        **kwargs
    )


def CardDescription(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return P(
        *children, 
        cls=cn("text-muted-foreground text-sm", class_name, cls), 
        data_slot="card-description", 
        **kwargs
    )


def CardAction(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children, 
        cls=cn(
            "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
            class_name,
            cls,
        ), 
        data_slot="card-action", 
        **kwargs
    )


def CardContent(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children, 
        cls=cn("px-6", class_name, cls), 
        data_slot="card-content", 
        **kwargs
    )


def CardFooter(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children, 
        cls=cn("flex items-center px-6 [.border-t]:pt-6", class_name, cls), 
        data_slot="card-footer", 
        **kwargs
    )
