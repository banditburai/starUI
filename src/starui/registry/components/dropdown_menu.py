from typing import Any, Literal

from starhtml import FT, Div, Hr, Icon, Signal, Span
from starhtml import Button as HTMLButton
from starhtml.datastar import evt

from .utils import cn, cva, gen_id, inject_context, merge_actions

dropdown_item_variants = cva(
    base=(
        "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 "
        "text-sm outline-hidden "
        "[&_[data-icon-sh]:not([class*='text-'])]:text-muted-foreground "
        "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:shrink-0 [&_[data-icon-sh]]:size-4"
    ),
    config={
        "variants": {
            "variant": {
                "default": "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                "destructive": (
                    "text-destructive hover:bg-destructive/10 hover:text-destructive focus:bg-destructive/10 focus:text-destructive "
                    "dark:hover:bg-destructive/20 dark:focus:bg-destructive/20"
                ),
            },
        },
        "defaultVariants": {"variant": "default"},
    },
)


def DropdownMenu(
    *children, signal: str | Signal = "", cls: str = "", **kwargs: Any
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("dropdown")

    ctx = {"sig": sig}

    return Div(
        Signal(f"{sig}_open", False),
        *[inject_context(child, **ctx) for child in children],
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def DropdownMenuTrigger(
    *children,
    variant: Literal[
        "default", "destructive", "outline", "secondary", "ghost", "link"
    ] = "outline",
    size: Literal["default", "sm", "lg", "icon"] = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def trigger(*, sig, **_):
        from .button import Button

        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)

        return Button(
            *children,
            data_ref=trigger_ref,
            popovertarget=f"{sig}_content",
            popoveraction="toggle",
            id=trigger_ref._id,
            variant=variant,
            size=size,
            type="button",
            cls=cls,
            **kwargs,
        )

    return trigger


def DropdownMenuContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 4,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def content(*, sig, **ctx):
        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)
        content_ref = Signal(f"{sig}_content", _ref_only=True)

        position_mods = {
            "placement": f"{side}-{align}" if align != "center" else side,
            "offset": side_offset,
            "flip": True,
            "shift": True,
            "hide": True,
        }

        return Div(
            *[inject_context(child, sig=sig, **ctx) for child in children],
            data_ref=content_ref,
            data_style_min_width=trigger_ref.if_(
                trigger_ref.offsetWidth + "px", "8rem"
            ),
            data_position=(trigger_ref._id, position_mods),
            popover="auto",
            id=content_ref._id,
            role="menu",
            aria_labelledby=trigger_ref._id,
            tabindex="-1",
            cls=cn(
                "z-50 min-w-[8rem] overflow-x-hidden overflow-y-auto rounded-md border",
                "bg-popover text-popover-foreground shadow-md p-1",
                cls,
            ),
            **kwargs,
        )

    return content


def DropdownMenuItem(
    *children,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sig, **_):
        content_ref = Signal(f"{sig}_content", _ref_only=True)

        click_actions = merge_actions(kwargs=kwargs, after=content_ref.hidePopover())

        return HTMLButton(
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                dropdown_item_variants(variant=variant),
                "pl-8" if inset else "",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            disabled=disabled,
            role="menuitem",
            **kwargs,
        )

    return _


def DropdownMenuCheckboxItem(
    *children,
    signal: str | Signal,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sig, **_):
        checked = Signal(getattr(signal, "_id", signal), _ref_only=True)
        content_ref = Signal(f"{sig}_content", _ref_only=True)

        click_actions = merge_actions(
            kwargs=kwargs, after=[checked.set(~checked), content_ref.hidePopover()]
        )

        return HTMLButton(
            Span(
                Icon("lucide:check"),
                data_show=checked,
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                dropdown_item_variants(variant="default"),
                "pl-8 pr-2",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemcheckbox",
            data_attr_aria_checked=checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def DropdownMenuRadioGroup(
    *children,
    signal: str | Signal,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(**ctx):
        return Div(
            *[
                inject_context(child, radio_signal=getattr(signal, "_id", signal), **ctx)
                for child in children
            ],
            role="radiogroup",
            cls=cls,
            **kwargs,
        )

    return _


def DropdownMenuRadioItem(
    *children,
    value: str,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sig, radio_signal, **_):
        radio = Signal(radio_signal, _ref_only=True)
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        is_checked = radio == value

        click_actions = merge_actions(
            kwargs=kwargs, after=[radio.set(value), content_ref.hidePopover()]
        )

        return HTMLButton(
            Span(
                Icon("lucide:circle", cls="size-2 fill-current"),
                data_show=is_checked,
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                dropdown_item_variants(variant="default"),
                "pl-8 pr-2",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemradio",
            data_attr_aria_checked=is_checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def DropdownMenuSeparator(cls: str = "", **kwargs: Any) -> FT:
    def _(**_):
        return Hr(cls=cn("-mx-1 my-1 border-border", cls), **kwargs)

    return _


def DropdownMenuLabel(
    *children, inset: bool = False, cls: str = "", **kwargs: Any
) -> FT:
    def _(**_):
        return Div(
            *children,
            cls=cn(
                "px-2 py-1.5 text-sm font-medium",
                "pl-8" if inset else "",
                cls,
            ),
            **kwargs,
        )

    return _


def DropdownMenuShortcut(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Span(
        *children,
        cls=cn("ml-auto text-xs tracking-widest text-muted-foreground", cls),
        **kwargs,
    )


def DropdownMenuGroup(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            role="group",
            cls=cls,
            **kwargs,
        )

    return _


def DropdownMenuSub(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(**ctx):
        sub = getattr(signal, "_id", signal) or gen_id("dropdown_sub")
        sub_ctx = dict(sub=sub, **ctx)

        return Div(
            Signal(f"{sub}_open", False),
            *[inject_context(child, **sub_ctx) for child in children],
            cls=cn("relative", cls),
            **kwargs,
        )

    return _


def DropdownMenuSubTrigger(
    *children,
    inset: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sub, **_):
        sub_trigger_ref = Signal(f"{sub}_trigger", _ref_only=True)
        sub_content_ref = Signal(f"{sub}_content", _ref_only=True)
        sub_open = Signal(f"{sub}_open", _ref_only=True)

        click_actions = merge_actions(kwargs=kwargs) or None

        return HTMLButton(
            *children,
            Icon("lucide:chevron-right", cls="ml-auto size-4"),
            data_ref=sub_trigger_ref,
            id=sub_trigger_ref._id,
            popovertarget=sub_content_ref._id,
            popoveraction="toggle",
            data_on_click=click_actions,
            cls=cn(
                dropdown_item_variants(variant="default"),
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
                "pl-8" if inset else "",
                cls,
            ),
            data_attr_data_state=sub_open.if_("open", "closed"),
            type="button",
            role="menuitem",
            aria_haspopup="menu",
            data_attr_aria_expanded=sub_open.if_("true", "false"),
            **kwargs,
        )

    return _


def DropdownMenuSubContent(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sub, **ctx):
        sub_trigger_ref = Signal(f"{sub}_trigger", _ref_only=True)
        sub_content_ref = Signal(f"{sub}_content", _ref_only=True)
        sub_open = Signal(f"{sub}_open", _ref_only=True)

        position_mods = {
            "placement": "right-start",
            "flip": True,
            "shift": True,
            "hide": True,
            "container": "auto",
        }

        return Div(
            *[inject_context(child, sub=sub, **ctx) for child in children],
            data_ref=sub_content_ref,
            data_on_toggle=sub_open.set(evt.newState == "open"),
            data_position=(sub_trigger_ref._id, position_mods),
            popover="auto",
            id=sub_content_ref._id,
            cls=cn(
                "z-50 min-w-[8rem] overflow-hidden rounded-md border",
                "bg-popover text-popover-foreground shadow-lg p-1",
                cls,
            ),
            role="menu",
            **kwargs,
        )

    return _
