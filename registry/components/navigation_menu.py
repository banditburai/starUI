from itertools import count

from starhtml import FT, A, Div, Icon, Li, Nav, Signal, Ul, clear_timeout, reset_timeout
from starhtml import Button as HTMLButton
from starhtml.datastar import evt

from .utils import cn, gen_id, inject_context

__metadata__ = {
    "description": "Horizontal nav with hover-activated panels",
    "handlers": ["position"],
}


def NavigationMenu(
    *children,
    signal: str | Signal = "",
    aria_label: str = "Main",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("nav")
    active = Signal(f"{sig}_active", "")
    timer = Signal(f"{sig}_timer", _ref_only=True)
    viewport_ref = Signal(f"{sig}_viewport", _ref_only=True)
    list_id = f"{sig}_list"
    content_panels = []

    ctx = {
        "active": active,
        "timer": timer,
        "viewport_ref": viewport_ref,
        "list_id": list_id,
        "_item_index": count(),
        "_content_panels": content_panels,
    }

    rendered = [inject_context(child, **ctx) for child in children]

    return Nav(
        active,
        *rendered,
        Div(
            *content_panels,
            data_ref=viewport_ref,
            data_on_toggle=active.set((evt.newState == "closed").if_("", active)),
            data_position=(
                list_id,
                {
                    "placement": "bottom-start",
                    "offset": 6,
                    "shift": True,
                },
            ),
            data_on_mouseenter=clear_timeout(timer),
            data_on_mouseleave=reset_timeout(timer, 150, viewport_ref.hidePopover()),
            tabindex="-1",
            popover="auto",
            id=viewport_ref._id,
            data_slot="navigation-menu-viewport",
            cls=cn(
                "z-50 overflow-hidden rounded-md border",
                "bg-popover text-popover-foreground shadow-lg",
            ),
        )
        if content_panels
        else None,
        aria_label=aria_label,
        data_slot="navigation-menu",
        cls=cn(
            "relative z-10 flex max-w-max flex-1 items-center justify-center",
            cls,
        ),
        **kwargs,
    )


def NavigationMenuList(*children, cls: str = "", **kwargs) -> FT:
    def _(*, list_id, **ctx):
        return Ul(
            *[inject_context(child, **ctx) for child in children],
            id=list_id,
            data_orientation="horizontal",
            data_slot="navigation-menu-list",
            cls=cn(
                "flex flex-1 list-none items-center justify-center space-x-1 group",
                cls,
            ),
            **kwargs,
        )

    return _


def NavigationMenuItem(*children, cls: str = "", **kwargs) -> FT:
    def _(*, _item_index, **ctx):
        item_id = str(next(_item_index))
        return Li(
            *[inject_context(child, item_id=item_id, **ctx) for child in children],
            data_slot="navigation-menu-item",
            cls=cn("relative", cls),
            **kwargs,
        )

    return _


def NavigationMenuTrigger(*children, cls: str = "", **kwargs) -> FT:
    def _(*, active, timer, item_id, viewport_ref, **_):
        is_active = active == item_id
        hover_actions = [clear_timeout(timer), active.set(item_id), viewport_ref.showPopover()]

        return HTMLButton(
            *children,
            Icon(
                "lucide:chevron-down",
                cls="relative top-[1px] ml-1 size-3 transition-transform duration-200",
                data_style_transform=is_active.if_("rotate(180deg)", "rotate(0deg)"),
            ),
            data_on_click=[
                clear_timeout(timer),
                active.set(is_active.if_("", item_id)),
                is_active.if_(viewport_ref.hidePopover(), viewport_ref.showPopover()),
            ],
            data_on_mouseenter=hover_actions,
            data_on_mouseleave=reset_timeout(timer, 150, viewport_ref.hidePopover()),
            type="button",
            data_slot="navigation-menu-trigger",
            data_attr_data_state=is_active.if_("open", "closed"),
            data_attr_aria_expanded=is_active.if_("true", "false"),
            cls=cn(
                "inline-flex h-9 w-max items-center justify-center rounded-md group",
                "bg-background px-4 py-2 text-sm font-medium transition-colors outline-none",
                "hover:bg-accent hover:text-accent-foreground",
                "focus-visible:ring-[3px] focus-visible:ring-ring/50",
                "disabled:pointer-events-none disabled:opacity-50",
                "data-[state=open]:bg-accent/50",
                cls,
            ),
            **kwargs,
        )

    return _


def NavigationMenuContent(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, active, item_id, _content_panels, **_):
        is_active = active == item_id
        _content_panels.append(
            Div(
                *children,
                data_show=is_active,
                data_slot="navigation-menu-content",
                data_attr_data_state=is_active.if_("open", "closed"),
                cls=cls,
                **kwargs,
            )
        )
        return None

    return _


def NavigationMenuLink(
    *children,
    href: str = "#",
    active: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    return A(
        *children,
        href=href,
        aria_current="page" if active else None,
        data_active="true" if active else "false",
        data_slot="navigation-menu-link",
        cls=cn(
            "inline-flex h-9 w-max items-center justify-center rounded-md",
            "bg-background px-4 py-2 text-sm font-medium no-underline transition-colors outline-none",
            "hover:bg-accent hover:text-accent-foreground",
            "focus-visible:ring-[3px] focus-visible:ring-ring/50",
            "data-[active=true]:bg-accent/50 data-[active=true]:text-accent-foreground",
            cls,
        ),
        **kwargs,
    )


def NavigationMenuListContent(*children, cls: str = "", **kwargs) -> FT:
    return Ul(
        *children,
        data_slot="navigation-menu-list-content",
        cls=cn(
            "grid gap-3 p-4 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]",
            cls,
        ),
        **kwargs,
    )


def NavigationMenuListItem(
    *children,
    title: str,
    href: str = "#",
    cls: str = "",
    **kwargs,
) -> FT:
    return Li(
        A(
            Div(title, cls="text-sm leading-none font-medium"),
            *children,
            href=href,
            cls=cn(
                "block space-y-1 rounded-md p-3 leading-none no-underline select-none",
                "transition-colors outline-none hover:bg-accent hover:text-accent-foreground",
                "focus-visible:bg-accent focus-visible:text-accent-foreground",
                "focus-visible:ring-[3px] focus-visible:ring-ring/50",
            ),
            **kwargs,
        ),
        data_slot="navigation-menu-list-item",
        cls=cls,
    )
