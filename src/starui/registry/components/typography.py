from typing import Literal

from starhtml import FT, Div, Li, Ol, Ul
from starhtml import H1 as HTMLH1
from starhtml import H2 as HTMLH2
from starhtml import H3 as HTMLH3
from starhtml import H4 as HTMLH4
from starhtml import Blockquote as HTMLBlockquote
from starhtml import Code as HTMLCode
from starhtml import Figcaption as HTMLFigcaption
from starhtml import Figure as HTMLFigure
from starhtml import Hr as HTMLHr
from starhtml import Kbd as HTMLKbd
from starhtml import Mark as HTMLMark
from starhtml import P as HTMLP
from starhtml import Small as HTMLSmall

from .utils import cn, cva

ProseSize = Literal["sm", "base", "lg", "xl"]

heading_variants = cva(
    base="scroll-m-20 tracking-tight text-balance first:mt-0",
    config={
        "variants": {
            "level": {
                "display": "text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight",
                "h1": "text-3xl sm:text-4xl lg:text-5xl font-extrabold leading-tight",
                "h2": "border-b pb-2 text-2xl sm:text-3xl font-semibold leading-tight",
                "h3": "text-2xl font-semibold leading-tight",
                "h4": "text-xl font-semibold leading-snug",
            },
        },
    },
)

text_variants = cva(
    base="",
    config={
        "variants": {
            "variant": {
                "body": "leading-7 [&:not(:first-child)]:mt-6",
                "lead": "text-xl text-muted-foreground",
                "large": "text-lg font-semibold",
                "small": "text-sm font-medium leading-none",
                "muted": "text-sm text-muted-foreground",
            }
        },
        "defaultVariants": {"variant": "body"},
    },
)

prose_variants = cva(
    base="prose text-foreground dark:prose-invert prose-headings:text-foreground prose-a:text-primary",
    config={
        "variants": {
            "size": {
                "sm": "prose-sm",
                "base": "",
                "lg": "prose-lg",
                "xl": "prose-xl",
            }
        },
        "defaultVariants": {"size": "base"},
    },
)


def Display(*children, cls="", **kwargs) -> FT:
    return HTMLH1(*children, cls=cn(heading_variants(level="display"), cls), **kwargs)


def H1(*children, cls="", **kwargs) -> FT:
    return HTMLH1(*children, cls=cn(heading_variants(level="h1"), cls), **kwargs)


def H2(*children, cls="", **kwargs) -> FT:
    return HTMLH2(*children, cls=cn(heading_variants(level="h2"), cls), **kwargs)


def H3(*children, cls="", **kwargs) -> FT:
    return HTMLH3(*children, cls=cn(heading_variants(level="h3"), cls), **kwargs)


def H4(*children, cls="", **kwargs) -> FT:
    return HTMLH4(*children, cls=cn(heading_variants(level="h4"), cls), **kwargs)


def P(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="body"), cls), **kwargs)


def Lead(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="lead"), cls), **kwargs)


def Large(*children, cls="", **kwargs) -> FT:
    return Div(*children, cls=cn(text_variants(variant="large"), cls), **kwargs)


def Small(*children, cls="", **kwargs) -> FT:
    return HTMLSmall(*children, cls=cn(text_variants(variant="small"), cls), **kwargs)


def Muted(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="muted"), cls), **kwargs)


def Caption(*children, cls="", **kwargs) -> FT:
    return Div(
        *children,
        cls=cn(
            "text-xs font-medium uppercase tracking-wider text-muted-foreground",
            cls,
        ),
        **kwargs,
    )


def InlineCode(*children, cls="", **kwargs) -> FT:
    return HTMLCode(
        *children,
        cls=cn(
            "rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold",
            cls,
        ),
        **kwargs,
    )


def Blockquote(*children, cls="", **kwargs) -> FT:
    return HTMLBlockquote(
        *children, cls=cn("mt-6 border-l-2 pl-6 italic", cls), **kwargs
    )


def List(*children, ordered=False, cls="", **kwargs) -> FT:
    items = [c if getattr(c, 'tag', None) == 'li' else Li(c) for c in children]
    classes = cn(
        "my-6 ml-6 [&>li]:mt-2",
        "list-decimal" if ordered else "list-disc",
        cls,
    )
    return (Ol if ordered else Ul)(*items, cls=classes, **kwargs)


def Prose(*children, size: ProseSize = "base", cls="", **kwargs) -> FT:
    return Div(*children, cls=cn(prose_variants(size=size), cls), **kwargs)


def Kbd(*children, cls="", **kwargs) -> FT:
    return HTMLKbd(
        *children,
        cls=cn(
            "inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-xs font-medium text-foreground",
            cls,
        ),
        **kwargs,
    )


def Mark(*children, cls="", **kwargs) -> FT:
    return HTMLMark(
        *children,
        cls=cn("bg-primary/20 dark:bg-primary/30 px-1 py-0.5 rounded-sm", cls),
        **kwargs,
    )


def Hr(cls="", **kwargs) -> FT:
    return HTMLHr(cls=cn("my-8 border-0 border-t border-border", cls), **kwargs)


def Figure(*children, cls="", **kwargs) -> FT:
    return HTMLFigure(*children, cls=cn("my-8 space-y-3", cls), **kwargs)


def Figcaption(*children, cls="", **kwargs) -> FT:
    return HTMLFigcaption(
        *children,
        cls=cn("text-sm text-muted-foreground text-center italic", cls),
        **kwargs,
    )
