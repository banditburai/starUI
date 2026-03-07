from typing import Literal

from starhtml import Button as HTMLButton
from starhtml import Icon, Li, Nav, Signal, Span, Ul

from .utils import cn, cva, gen_id, inject_context

__metadata__ = {"description": "Page navigation with prev/next controls"}


PaginationSize = Literal["default", "sm", "lg", "icon"]

pagination_link_variants = cva(
    base=(
        "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium "
        "transition-all disabled:pointer-events-none disabled:opacity-50 "
        "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]:not([class*='size-'])]:size-4 "
        "shrink-0 [&_[data-icon-sh]]:shrink-0 outline-none "
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] "
        "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50 "
        "data-[active=true]:border data-[active=true]:bg-background "
        "data-[active=true]:shadow-xs "
        "data-[active=true]:dark:bg-input/30 data-[active=true]:dark:border-input "
        "data-[active=true]:dark:hover:bg-input/50"
    ),
    config={
        "variants": {
            "size": {
                "default": "h-9 px-4 py-2 has-[[data-icon-sh]]:px-3",
                "sm": "h-8 px-2 text-xs",
                "lg": "h-10 px-4",
                "icon": "size-9",
            },
        },
        "defaultVariants": {"size": "icon"},
    },
)


def Pagination(
    *children,
    signal: str | Signal = "",
    total_pages=1,
    current_page=1,
    aria_label="pagination",
    cls="",
    **kwargs,
):
    sig = getattr(signal, "_id", signal) or gen_id("pagination")
    ctx = {"page_sig": (page_sig := Signal(sig, current_page)), "total_pages": total_pages}
    return Nav(
        page_sig,
        *[inject_context(c, **ctx) for c in children],
        role="navigation",
        aria_label=aria_label,
        data_slot="pagination",
        cls=cn("mx-auto flex w-full justify-center", cls),
        **kwargs,
    )


def PaginationContent(*children, cls="", **kwargs):
    return Ul(*children, data_slot="pagination-content", cls=cn("flex flex-row items-center gap-1", cls), **kwargs)


def PaginationItem(*children, cls="", **kwargs):
    return Li(*children, data_slot="pagination-item", cls=cls or None, **kwargs)


def PaginationLink(
    *children,
    page,
    size: PaginationSize = "icon",
    disabled=False,
    cls="",
    **kwargs,
):
    def _(*, page_sig, **_):
        is_active = page_sig == page
        return HTMLButton(
            *children,
            type="button",
            data_on_click=page_sig.set(page) if not disabled else None,
            disabled=disabled,
            data_attr_aria_current=is_active.if_("page", ""),
            data_attr_data_active=is_active,
            data_slot="pagination-link",
            cls=cn(pagination_link_variants(size=size), "cursor-pointer", cls),
            **kwargs,
        )

    return _


def _PaginationNav(direction, show_text=True, cls="", **kwargs):
    is_prev = direction < 0
    icon = Icon("lucide:chevron-left" if is_prev else "lucide:chevron-right")
    text = Span("Previous" if is_prev else "Next", cls="hidden sm:block") if show_text else None
    body = (icon, text) if is_prev else (text, icon)

    def _(*, page_sig, total_pages=1, **_):
        at_boundary = (page_sig <= 1) if is_prev else (page_sig >= total_pages)
        new_val = (page_sig - 1).max(1) if is_prev else (page_sig + 1).min(total_pages)
        return HTMLButton(
            *body,
            data_on_click=page_sig.set(new_val),
            type="button",
            data_attr_disabled=at_boundary,
            aria_label=f"Go to {'previous' if is_prev else 'next'} page",
            data_slot="pagination-link",
            cls=cn(
                pagination_link_variants(size="default"),
                "cursor-pointer gap-1 px-2.5",
                ("sm:pl-2.5" if is_prev else "sm:pr-2.5") if show_text else "",
                cls,
            ),
            **kwargs,
        )

    return _


def PaginationPrevious(show_text=True, cls="", **kwargs):
    return _PaginationNav(-1, show_text, cls, **kwargs)


def PaginationNext(show_text=True, cls="", **kwargs):
    return _PaginationNav(1, show_text, cls, **kwargs)


def PaginationEllipsis(cls="", **kwargs):
    return Span(
        Icon("lucide:ellipsis", cls="size-4"),
        Span("More pages", cls="sr-only"),
        data_slot="pagination-ellipsis",
        cls=cn("flex size-9 items-center justify-center", cls),
        **kwargs,
    )


def _JumpEllipsis(page_sig, direction, total_pages):
    icon_name = "lucide:chevrons-left" if direction < 0 else "lucide:chevrons-right"
    label = "Jump 5 pages back" if direction < 0 else "Jump 5 pages forward"
    target = (page_sig + 5 * direction).max(1).min(total_pages)

    return HTMLButton(
        Span(
            Icon("lucide:ellipsis", cls="size-4"),
            cls="flex items-center justify-center group-hover:hidden group-focus-within:hidden",
        ),
        Span(
            Icon(icon_name, cls="size-4"),
            cls="hidden items-center justify-center group-hover:flex group-focus-within:flex",
        ),
        Span(label, cls="sr-only"),
        data_on_click=page_sig.set(target),
        type="button",
        aria_label=label,
        data_slot="pagination-ellipsis",
        cls=cn(pagination_link_variants(size="icon"), "group cursor-pointer"),
    )


def SimplePagination(
    current_page=1,
    total_pages=1,
    signal: str | Signal = "",
    max_visible=7,
    show_prev_next_text=True,
    cls="",
    **kwargs,
):
    total_pages = max(total_pages, 1)
    max_visible = max(max_visible, 5)
    current_page = max(1, min(current_page, total_pages))

    sig = getattr(signal, "_id", signal) or gen_id("pagination")
    page_sig = Signal(sig, _ref_only=True)

    prev = PaginationItem(PaginationPrevious(show_text=show_prev_next_text))
    nxt = PaginationItem(PaginationNext(show_text=show_prev_next_text))

    if total_pages <= max_visible:
        pages = [
            PaginationItem(
                PaginationLink(
                    str(p),
                    page=p,
                    aria_label=f"Page {p}" if p == current_page else f"Go to page {p}",
                    data_attr_aria_label=(page_sig == p).if_(f"Page {p}", f"Go to page {p}"),
                )
            )
            for p in range(1, total_pages + 1)
        ]
    else:
        middle_count = max(max_visible - 4, 1)
        half = middle_count // 2

        # Snap thresholds avoid orphan pages (e.g. [1] [...] [3] — page 2 orphaned)
        left_snap = half + 3
        right_snap = total_pages - middle_count + half - 1

        window_start = (page_sig <= left_snap).if_(
            2,
            (page_sig >= right_snap).if_(total_pages - middle_count, page_sig - half),
        )
        ssr_start = (
            2
            if current_page <= left_snap
            else total_pages - middle_count
            if current_page >= right_snap
            else current_page - half
        )

        middle = []
        for i in range(middle_count):
            page_expr = window_start + i
            ssr_page = ssr_start + i
            middle.append(
                PaginationItem(
                    PaginationLink(
                        str(ssr_page),
                        page=page_expr,
                        data_text=page_expr,
                        aria_label=f"Page {ssr_page}" if ssr_page == current_page else f"Go to page {ssr_page}",
                        data_attr_aria_label=(page_sig == page_expr).if_(
                            "Page " + page_expr, "Go to page " + page_expr
                        ),
                    )
                )
            )

        pages = [
            PaginationItem(PaginationLink("1", page=1, aria_label="Go to page 1")),
            PaginationItem(
                _JumpEllipsis(page_sig, -1, total_pages),
                data_show=page_sig > left_snap,
            ),
            *middle,
            PaginationItem(
                _JumpEllipsis(page_sig, 1, total_pages),
                data_show=page_sig < right_snap,
            ),
            PaginationItem(
                PaginationLink(
                    str(total_pages),
                    page=total_pages,
                    aria_label=f"Go to page {total_pages}",
                )
            ),
        ]

    return Pagination(
        PaginationContent(prev, *pages, nxt),
        signal=sig,
        total_pages=total_pages,
        current_page=current_page,
        cls=cls,
        **kwargs,
    )
