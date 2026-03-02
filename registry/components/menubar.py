from itertools import count
from typing import Literal

from starhtml import FT, Div, Hr, Icon, Signal, Span, clear_timeout, reset_timeout
from starhtml import Button as HTMLButton
from starhtml.datastar import evt, seq

from .utils import cn, cva, gen_id, inject_context, merge_actions


__metadata__ = {
    "description": "Desktop-style persistent menu bar",
    "handlers": ["position"],
}


menubar_item_variants = cva(
    base=(
        "relative flex w-full cursor-default select-none items-center gap-1.5 rounded-sm px-1.5 py-1 "
        "text-sm outline-hidden "
        "[&_[data-icon-sh]:not([class*='text-'])]:text-muted-foreground "
        "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:shrink-0 [&_[data-icon-sh]]:size-4"
    ),
    config={
        "variants": {
            "variant": {
                "default": "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                "destructive": (
                    "text-destructive hover:bg-destructive/10 hover:text-destructive "
                    "focus:bg-destructive/10 focus:text-destructive "
                    "dark:hover:bg-destructive/20 dark:focus:bg-destructive/20 "
                    "[&_[data-icon-sh]]:text-destructive"
                ),
            },
        },
        "defaultVariants": {"variant": "default"},
    },
)


def Menubar(*children, signal: str | Signal = "", cls: str = "", **kwargs) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("menubar")
    active = Signal(f"{sig}_active", "")

    ctx = {
        "sig": sig,
        "active": active,
        "_menu_index": count(),
    }

    return Div(
        active,
        *[inject_context(child, **ctx) for child in children],
        role="menubar",
        data_slot="menubar",
        cls=cn(
            "bg-background flex h-9 items-center gap-1 rounded-md border p-1 shadow-xs",
            cls,
        ),
        **kwargs,
    )


def MenubarMenu(*children, cls: str = "", **kwargs) -> FT:
    def _(*, _menu_index, sig, **ctx):
        menu_id = str(next(_menu_index))
        ctx = dict(
            menu_id=menu_id,
            trigger_ref=Signal(f"{sig}_{menu_id}_trigger", _ref_only=True),
            content_ref=Signal(f"{sig}_{menu_id}_content", _ref_only=True),
            **ctx,
        )
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="menubar-menu",
            cls=cn("relative inline-block", cls),
            **kwargs,
        )

    return _


def MenubarTrigger(*children, cls: str = "", **kwargs) -> FT:
    def _(*, active, menu_id, trigger_ref, content_ref, **_):
        is_active = active == menu_id

        return HTMLButton(
            *children,
            data_ref=trigger_ref,
            popovertarget=content_ref._id,
            popoveraction="toggle",
            data_on_mouseenter=(active != "").then(seq(content_ref.showPopover(), active.set(menu_id))),
            id=trigger_ref._id,
            type="button",
            role="menuitem",
            aria_haspopup="menu",
            data_slot="menubar-trigger",
            data_attr_data_state=is_active.if_("open", "closed"),
            data_attr_aria_expanded=is_active.if_("true", "false"),
            cls=cn(
                "flex items-center rounded-sm px-1.5 py-[2px] text-sm font-medium "
                "outline-hidden select-none cursor-default "
                "hover:bg-muted focus:bg-muted data-[state=open]:bg-muted",
                cls,
            ),
            **kwargs,
        )

    return _


def MenubarContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 8,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, trigger_ref, content_ref, active, menu_id, **ctx):
        ctx = dict(trigger_ref=trigger_ref, content_ref=content_ref, active=active, menu_id=menu_id, **ctx)

        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_ref=content_ref,
            data_on_toggle=active.set((evt.newState == "open").if_(menu_id, (active == menu_id).if_("", active))),
            data_position=(trigger_ref._id, {
                "placement": f"{side}-{align}" if align != "center" else side,
                "offset": side_offset,
                "flip": True,
                "shift": True,
                "hide": True,
            }),
            popover="auto",
            id=content_ref._id,
            role="menu",
            aria_labelledby=trigger_ref._id,
            tabindex="-1",
            data_slot="menubar-content",
            cls=cn(
                "z-50 max-h-[min(var(--popover-available-height,80vh),80vh)] min-w-36",
                "overflow-x-hidden overflow-y-auto rounded-md border",
                "bg-popover p-1 text-popover-foreground shadow-md",
                cls,
            ),
            **kwargs,
        )

    return _


def MenubarItem(
    *children,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, content_ref, **_):
        click_actions = merge_actions(kwargs=kwargs, after=content_ref.hidePopover())

        return HTMLButton(
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                menubar_item_variants(variant=variant),
                "pl-7" if inset else "",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            disabled=disabled,
            role="menuitem",
            data_slot="menubar-item",
            **kwargs,
        )

    return _


def MenubarCheckboxItem(
    *children,
    signal: str | Signal,
    disabled: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, content_ref, **_):
        checked = Signal(getattr(signal, "_id", signal), _ref_only=True)

        click_actions = merge_actions(kwargs=kwargs, after=[checked.set(~checked), content_ref.hidePopover()])

        return HTMLButton(
            Span(
                Icon("lucide:check"),
                data_show=checked,
                cls="absolute left-1.5 flex size-4 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                menubar_item_variants(variant="default"),
                "pl-7 pr-1.5",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemcheckbox",
            data_slot="menubar-checkbox-item",
            data_attr_aria_checked=checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def MenubarRadioGroup(
    *children,
    signal: str | Signal,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, radio_signal=getattr(signal, "_id", signal), **ctx) for child in children],
            role="radiogroup",
            data_slot="menubar-radio-group",
            cls=cls,
            **kwargs,
        )

    return _


def MenubarRadioItem(
    *children,
    value: str,
    disabled: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, content_ref, radio_signal, **_):
        radio = Signal(radio_signal, _ref_only=True)
        is_checked = radio == value

        click_actions = merge_actions(kwargs=kwargs, after=[radio.set(value), content_ref.hidePopover()])

        return HTMLButton(
            Span(
                Icon("lucide:circle", cls="size-2 fill-current"),
                data_show=is_checked,
                cls="absolute left-1.5 flex size-4 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=cn(
                menubar_item_variants(variant="default"),
                "pl-7 pr-1.5",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemradio",
            data_slot="menubar-radio-item",
            data_attr_aria_checked=is_checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def MenubarSub(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**ctx):
        sub = getattr(signal, "_id", signal) or gen_id("menubar_sub")
        sub_open = Signal(f"{sub}_open", False)
        ctx = dict(
            sub_open=sub_open,
            sub_trigger_ref=Signal(f"{sub}_trigger", _ref_only=True),
            sub_content_ref=Signal(f"{sub}_content", _ref_only=True),
            sub_timer=Signal(f"{sub}_timer", _ref_only=True),
            **ctx,
        )

        return Div(
            sub_open,
            *[inject_context(child, **ctx) for child in children],
            data_slot="menubar-sub",
            cls=cn("relative", cls),
            **kwargs,
        )

    return _


def MenubarSubTrigger(
    *children,
    inset: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sub_open, sub_trigger_ref, sub_content_ref, sub_timer, **_):
        click_actions = merge_actions(kwargs=kwargs) or None

        return HTMLButton(
            *children,
            Icon("lucide:chevron-right", cls="ml-auto size-4"),
            data_ref=sub_trigger_ref,
            id=sub_trigger_ref._id,
            popovertarget=sub_content_ref._id,
            popoveraction="toggle",
            data_on_click=click_actions,
            data_on_mouseenter=clear_timeout(sub_timer, sub_content_ref.showPopover()),
            data_on_mouseleave=reset_timeout(sub_timer, 150, sub_content_ref.hidePopover()),
            cls=cn(
                menubar_item_variants(variant="default"),
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
                "pl-7" if inset else "",
                cls,
            ),
            data_attr_data_state=sub_open.if_("open", "closed"),
            type="button",
            role="menuitem",
            data_slot="menubar-sub-trigger",
            aria_haspopup="menu",
            data_attr_aria_expanded=sub_open.if_("true", "false"),
            **kwargs,
        )

    return _


def MenubarSubContent(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sub_open, sub_trigger_ref, sub_content_ref, sub_timer, **ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_ref=sub_content_ref,
            data_on_toggle=sub_open.set(evt.newState == "open"),
            data_on_mouseenter=clear_timeout(sub_timer),
            data_on_mouseleave=reset_timeout(sub_timer, 150, sub_content_ref.hidePopover()),
            data_position=(sub_trigger_ref._id, {
                "placement": "right-start",
                "flip": True,
                "shift": True,
                "hide": True,
                "container": "auto",
            }),
            popover="auto",
            id=sub_content_ref._id,
            role="menu",
            data_slot="menubar-sub-content",
            cls=cn(
                "z-50 max-h-[min(var(--popover-available-height,80vh),80vh)] min-w-32",
                "overflow-x-hidden overflow-y-auto rounded-md border",
                "bg-popover p-1 text-popover-foreground shadow-lg",
                cls,
            ),
            **kwargs,
        )

    return _


def MenubarSeparator(cls: str = "", **kwargs) -> FT:
    return Hr(
        data_slot="menubar-separator",
        cls=cn("-mx-1 my-1 border-border", cls),
        **kwargs,
    )


def MenubarLabel(*children, inset: bool = False, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="menubar-label",
        cls=cn(
            "px-1.5 py-1 text-sm font-medium",
            "pl-7" if inset else "",
            cls,
        ),
        **kwargs,
    )


def MenubarShortcut(*children, cls: str = "", **kwargs) -> FT:
    return Span(
        *children,
        data_slot="menubar-shortcut",
        cls=cn("ml-auto text-xs tracking-widest text-muted-foreground", cls),
        **kwargs,
    )
