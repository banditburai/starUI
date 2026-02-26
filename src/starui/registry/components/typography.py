from typing import Literal

from starhtml import FT, Div, Ol, Ul
from starhtml import H1 as HTMLH1
from starhtml import H2 as HTMLH2
from starhtml import H3 as HTMLH3
from starhtml import H4 as HTMLH4
from starhtml import H5 as HTMLH5
from starhtml import H6 as HTMLH6
from starhtml import Blockquote as HTMLBlockquote
from starhtml import Code as HTMLCode
from starhtml import Em as HTMLEm
from starhtml import Figcaption as HTMLFigcaption
from starhtml import Figure as HTMLFigure
from starhtml import Hr as HTMLHr
from starhtml import Kbd as HTMLKbd
from starhtml import Mark as HTMLMark
from starhtml import P as HTMLP
from starhtml import Strong as HTMLStrong

from .utils import cn, cva

TextVariant = Literal["body", "lead", "large", "small", "muted"]
ProseSize = Literal["sm", "base", "lg", "xl"]

heading_variants = cva(
    base="scroll-m-20 tracking-tight first:mt-0",
    config={
        "variants": {
            "level": {
                "h1": "text-4xl font-extrabold leading-tight mb-8",
                "h2": "text-3xl font-semibold leading-tight mt-10 mb-6",
                "h3": "text-2xl font-semibold leading-tight mt-8 mb-4",
                "h4": "text-xl font-semibold leading-snug mt-6 mb-3",
                "h5": "text-lg font-semibold leading-snug mt-4 mb-2",
                "h6": "text-base font-semibold leading-snug mt-4 mb-2",
            },
            "section": {
                "true": "border-b pb-2",
                "false": "",
            },
        },
        "defaultVariants": {"section": "false"},
    },
)

text_variants = cva(
    base="",
    config={
        "variants": {
            "variant": {
                "body": "leading-7 mb-6 [&:not(:first-child)]:mt-0",
                "lead": "text-xl text-muted-foreground mb-6",
                "large": "text-lg font-semibold mb-6",
                "small": "text-sm font-medium leading-none",
                "muted": "text-sm text-muted-foreground",
            }
        },
        "defaultVariants": {"variant": "body"},
    },
)

prose_variants = cva(
    base="max-w-none text-foreground prose dark:prose-invert prose-headings:text-foreground prose-a:text-primary",
    config={
        "variants": {
            "size": {
                "sm": "prose-sm",
                "base": "prose",
                "lg": "prose-lg",
                "xl": "prose-xl",
            }
        },
        "defaultVariants": {"size": "base"},
    },
)


def Display(*children, cls="", **kwargs) -> FT:
    return HTMLH1(
        *children,
        cls=cn("text-6xl font-extrabold leading-none mb-8 first:mt-0", cls),
        **kwargs,
    )


def H1(*children, cls="", **kwargs) -> FT:
    return HTMLH1(*children, cls=cn(heading_variants(level="h1"), cls), **kwargs)


def H2(*children, section=False, cls="", **kwargs) -> FT:
    return HTMLH2(
        *children,
        cls=cn(heading_variants(level="h2", section=str(section).lower()), cls),
        **kwargs,
    )


def H3(*children, cls="", **kwargs) -> FT:
    return HTMLH3(*children, cls=cn(heading_variants(level="h3"), cls), **kwargs)


def H4(*children, cls="", **kwargs) -> FT:
    return HTMLH4(*children, cls=cn(heading_variants(level="h4"), cls), **kwargs)


def H5(*children, cls="", **kwargs) -> FT:
    return HTMLH5(*children, cls=cn(heading_variants(level="h5"), cls), **kwargs)


def H6(*children, cls="", **kwargs) -> FT:
    return HTMLH6(*children, cls=cn(heading_variants(level="h6"), cls), **kwargs)


def P(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="body"), cls), **kwargs)


def Lead(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="lead"), cls), **kwargs)


def Large(*children, cls="", **kwargs) -> FT:
    return Div(*children, cls=cn(text_variants(variant="large"), cls), **kwargs)


def Small(*children, cls="", **kwargs) -> FT:
    return Div(*children, cls=cn("text-sm font-medium", cls), **kwargs)


def Muted(*children, cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant="muted"), cls), **kwargs)


def Subtitle(*children, cls="", **kwargs) -> FT:
    return HTMLP(
        *children,
        cls=cn("text-lg leading-relaxed text-muted-foreground mb-6", cls),
        **kwargs,
    )


def Caption(*children, cls="", **kwargs) -> FT:
    return Div(
        *children,
        cls=cn(
            "text-xs uppercase tracking-wider text-muted-foreground mb-2",
            cls,
        ),
        **kwargs,
    )


def Text(*children, variant="body", cls="", **kwargs) -> FT:
    return HTMLP(*children, cls=cn(text_variants(variant=variant), cls), **kwargs)


def InlineCode(*children, cls="", **kwargs) -> FT:
    return HTMLCode(
        *children,
        cls=cn(
            "relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold text-foreground",
            cls,
        ),
        **kwargs,
    )


def Blockquote(*children, cls="", **kwargs) -> FT:
    return HTMLBlockquote(
        *children, cls=cn("mt-6 border-l-2 pl-6 italic", cls), **kwargs
    )


def List(*children, ordered=False, cls="", **kwargs) -> FT:
    classes = cn("my-6 ml-6", "list-decimal" if ordered else "list-disc", cls)
    return (Ol if ordered else Ul)(*children, cls=classes, **kwargs)


def Prose(*children, size: ProseSize = "base", cls="", **kwargs) -> FT:
    return Div(*children, cls=cn(prose_variants(size=size), cls), **kwargs)


def Kbd(*children, cls="", **kwargs) -> FT:
    return HTMLKbd(
        *children,
        cls=cn(
            "pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-xs font-medium text-muted-foreground",
            cls,
        ),
        **kwargs,
    )


def Mark(*children, cls="", **kwargs) -> FT:
    return HTMLMark(
        *children,
        cls=cn("bg-yellow-200 dark:bg-teal-500/40 px-1 py-0.5 rounded", cls),
        **kwargs,
    )


def Strong(*children, cls="", **kwargs) -> FT:
    return HTMLStrong(*children, cls=cn("font-semibold", cls), **kwargs)


def Em(*children, cls="", **kwargs) -> FT:
    return HTMLEm(*children, cls=cn("italic", cls), **kwargs)


def Hr(cls="", **kwargs) -> FT:
    return HTMLHr(cls=cn("my-8 border-0 h-px bg-border", cls), **kwargs)


def Figure(*children, cls="", **kwargs) -> FT:
    return HTMLFigure(*children, cls=cn("my-8 space-y-3", cls), **kwargs)


def Figcaption(*children, cls="", **kwargs) -> FT:
    return HTMLFigcaption(
        *children,
        cls=cn("text-sm text-muted-foreground text-center italic", cls),
        **kwargs,
    )
