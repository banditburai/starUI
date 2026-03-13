from itertools import count
from typing import Literal

from starhtml import FT, Div, Hr, Icon, Signal, Span, Style, clear_timeout, js, reset_timeout
from starhtml import Button as HTMLButton
from starhtml.datastar import seq

from .utils import cn, cva, gen_id, inject_context, merge_actions

__metadata__ = {
    "description": "Desktop-style persistent menu bar",
    "handlers": ["position"],
}

_POPOVER_ANIMATE = """\
[data-popover-animate]{--_dur-in:150ms;--_dur-out:100ms;transform-origin:var(--popover-origin,center);transition:opacity var(--_dur-out) ease,scale var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete}
[data-popover-animate]:popover-open{transition-duration:var(--_dur-in);transition-timing-function:cubic-bezier(0.16,1,0.3,1)}
[data-popover-animate]:not(:popover-open){opacity:0;scale:0.95}
[data-popover-animate]:popover-open{@starting-style{opacity:0;scale:0.95}}
@media(prefers-reduced-motion:reduce){[data-popover-animate]{transition-duration:0ms!important}}"""

_MENU_ITEM_SEL = (
    "[role=menuitem]:not([disabled]),[role=menuitemcheckbox]:not([disabled]),[role=menuitemradio]:not([disabled])"
)
_MENU_NAV = (
    f"const items=[...evt.currentTarget.querySelectorAll('{_MENU_ITEM_SEL}')];"
    "if(!items.length)return;const k=evt.key;let i=items.indexOf(document.activeElement);"
    "if(k==='ArrowDown'){evt.preventDefault();i=(i+1)%items.length;items[i].focus()}"
    "else if(k==='ArrowUp'){evt.preventDefault();i=(i-1+items.length)%items.length;items[i].focus()}"
    "else if(k==='Home'){evt.preventDefault();items[0].focus()}"
    "else if(k==='End'){evt.preventDefault();items[items.length-1].focus()}"
    "else if(k.length===1&&!evt.ctrlKey&&!evt.metaKey&&!evt.altKey){"
    "const m=evt.currentTarget;m._sb=(m._sb||'')+k.toLowerCase();"
    "clearTimeout(m._st);m._st=setTimeout(()=>{m._sb=''},500);"
    "const b=m._sb,s=b.length===1?i+1:0;"
    "for(let j=0;j<items.length;j++){const x=(s+j)%items.length;"
    "if(items[x].textContent.trim().toLowerCase().startsWith(b)){items[x].focus();break}}}"
)


menubar_item_variants = cva(
    base=(
        "relative flex w-full cursor-default items-center gap-1.5 rounded-sm px-1.5 py-1 select-none "
        "text-sm outline-hidden "
        "[&_[data-icon-sh]:not([class*='text-'])]:text-muted-foreground "
        "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:size-4 [&_[data-icon-sh]]:shrink-0"
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


def _menubar_item_cls(
    *, variant: Literal["default", "destructive"] = "default", inset: str = "", disabled: bool = False, cls: str = ""
) -> str:
    return cn(menubar_item_variants(variant=variant), inset, "pointer-events-none opacity-50" if disabled else "", cls)


def Menubar(*children, signal: str | Signal = "", cls: str = "", **kwargs) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("menubar")
    active = Signal(f"{sig}_active", "")

    ctx = {
        "sig": sig,
        "active": active,
        "_menu_index": count(),
    }

    return Div(
        Style(_POPOVER_ANIMATE),
        active,
        *[inject_context(child, **ctx) for child in children],
        role="menubar",
        data_slot="menubar",
        cls=cn(
            "flex h-9 items-center gap-1 rounded-md border bg-background p-1 shadow-xs",
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
                "flex items-center rounded-sm px-1.5 py-0.5 text-sm font-medium "
                "cursor-default outline-hidden select-none "
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

        toggle_handler = js(
            f"const o=evt.newState==='open';"
            f"{active}=o?'{menu_id}':({active}==='{menu_id}'?'':{active});"
            f"if(o)requestAnimationFrame(()=>"
            f"evt.target.querySelector('{_MENU_ITEM_SEL}')?.focus())"
        )

        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_ref=content_ref,
            data_on_toggle=toggle_handler,
            data_on_keydown=js(_MENU_NAV),
            data_position=(
                trigger_ref._id,
                {
                    "placement": f"{side}-{align}" if align != "center" else side,
                    "offset": side_offset,
                    "flip": True,
                    "shift": True,
                    "hide": True,
                },
            ),
            popover="auto",
            data_popover_animate="",
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
            cls=_menubar_item_cls(variant=variant, inset="pl-7" if inset else "", disabled=disabled, cls=cls),
            type="button",
            disabled=disabled,
            role="menuitem",
            tabindex="-1",
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
            cls=_menubar_item_cls(inset="pr-1.5 pl-7", disabled=disabled, cls=cls),
            type="button",
            role="menuitemcheckbox",
            tabindex="-1",
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
            cls=_menubar_item_cls(inset="pr-1.5 pl-7", disabled=disabled, cls=cls),
            type="button",
            role="menuitemradio",
            tabindex="-1",
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
                _menubar_item_cls(inset="pl-7" if inset else "", cls=cls),
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
            ),
            data_attr_data_state=sub_open.if_("open", "closed"),
            type="button",
            role="menuitem",
            tabindex="-1",
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
        toggle_handler = js(
            f"const o=evt.newState==='open';{sub_open}=o;"
            f"if(o)requestAnimationFrame(()=>"
            f"evt.target.querySelector('{_MENU_ITEM_SEL}')?.focus())"
        )

        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_ref=sub_content_ref,
            data_on_toggle=toggle_handler,
            data_on_keydown=js(_MENU_NAV),
            data_on_mouseenter=clear_timeout(sub_timer),
            data_on_mouseleave=reset_timeout(sub_timer, 150, sub_content_ref.hidePopover()),
            data_position=(
                sub_trigger_ref._id,
                {
                    "placement": "right-start",
                    "flip": True,
                    "shift": True,
                    "hide": True,
                    "container": "auto",
                },
            ),
            popover="auto",
            data_popover_animate="",
            id=sub_content_ref._id,
            role="menu",
            aria_labelledby=sub_trigger_ref._id,
            tabindex="-1",
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
        cls=cn("-mx-1 my-1 h-px border-0 bg-border", cls),
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
        aria_hidden="true",
        cls=cn("ml-auto text-xs tracking-widest text-muted-foreground", cls),
        **kwargs,
    )
