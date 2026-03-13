from typing import Literal

from starhtml import FT, Div, Hr, Icon, Signal, Span, Style, js
from starhtml import Button as HTMLButton

from .utils import cn, cva, gen_id, inject_context, merge_actions

__metadata__ = {
    "description": "Dropdown menu with items",
    "handlers": ["position"],
}

_POPOVER_ANIMATE = """\
[data-popover-animate]{--_dur-in:150ms;--_dur-out:100ms;transform-origin:var(--popover-origin,center);transition:opacity var(--_dur-out) ease,scale var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete}
[data-popover-animate]:popover-open{transition-duration:var(--_dur-in);transition-timing-function:cubic-bezier(0.16,1,0.3,1)}
[data-popover-animate]:not(:popover-open){opacity:0;scale:0.95}
[data-popover-animate]:popover-open{@starting-style{opacity:0;scale:0.95}}
@media(prefers-reduced-motion:reduce){[data-popover-animate]{transition-duration:0ms!important}}"""

_MENU_ITEM_SEL = "[role=menuitem]:not([disabled]),[role=menuitemcheckbox]:not([disabled]),[role=menuitemradio]:not([disabled])"
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


dropdown_item_variants = cva(
    base=(
        "relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 "
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


def _dropdown_item_cls(
    *, variant: Literal["default", "destructive"] = "default", inset: str = "", disabled: bool = False, cls: str = ""
) -> str:
    return cn(dropdown_item_variants(variant=variant), inset, "pointer-events-none opacity-50" if disabled else "", cls)


def DropdownMenu(*children, signal: str | Signal = "", cls: str = "", **kwargs) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("dropdown")
    open_state = Signal(f"{sig}_open", False)

    ctx = {
        "open_state": open_state,
        "trigger_ref": Signal(f"{sig}_trigger", _ref_only=True),
        "content_ref": Signal(f"{sig}_content", _ref_only=True),
    }

    return Div(
        Style(_POPOVER_ANIMATE),
        open_state,
        *[inject_context(child, **ctx) for child in children],
        data_slot="dropdown-menu",
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def DropdownMenuTrigger(
    *children,
    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = "outline",
    size: Literal["default", "sm", "lg", "icon"] = "default",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, open_state, trigger_ref, content_ref, **_):
        from .button import Button

        return Button(
            *children,
            data_ref=trigger_ref,
            popovertarget=content_ref._id,
            popoveraction="toggle",
            id=trigger_ref._id,
            data_slot="dropdown-menu-trigger",
            aria_haspopup="menu",
            data_attr_aria_expanded=open_state.if_("true", "false"),
            variant=variant,
            size=size,
            type="button",
            cls=cls,
            **kwargs,
        )

    return _


def DropdownMenuContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 4,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, open_state, trigger_ref, content_ref, **ctx):
        ctx = dict(open_state=open_state, trigger_ref=trigger_ref, content_ref=content_ref, **ctx)

        toggle_handler = js(
            f"const o=evt.newState==='open';{open_state}=o;"
            f"if(o)requestAnimationFrame(()=>"
            f"evt.target.querySelector('{_MENU_ITEM_SEL}')?.focus())"
        )

        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_ref=content_ref,
            data_on_toggle=toggle_handler,
            data_on_keydown=js(_MENU_NAV),
            data_style_min_width=trigger_ref.if_(trigger_ref.offsetWidth + "px", "8rem"),
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
            data_slot="dropdown-menu-content",
            cls=cn(
                "z-50 max-h-[min(var(--popover-available-height,80vh),80vh)] min-w-[8rem]",
                "overflow-x-hidden overflow-y-auto rounded-md border",
                "bg-popover p-1 text-popover-foreground shadow-md",
                cls,
            ),
            **kwargs,
        )

    return _


def DropdownMenuItem(
    *children,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, content_ref, **_):
        return HTMLButton(
            *children,
            data_on_click=merge_actions(kwargs=kwargs, after=content_ref.hidePopover()) if not disabled else None,
            cls=_dropdown_item_cls(variant=variant, inset="pl-8" if inset else "", disabled=disabled, cls=cls),
            type="button",
            disabled=disabled,
            role="menuitem",
            tabindex="-1",
            data_slot="dropdown-menu-item",
            **kwargs,
        )

    return _


def DropdownMenuCheckboxItem(
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
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=_dropdown_item_cls(inset="pl-8 pr-2", disabled=disabled, cls=cls),
            type="button",
            role="menuitemcheckbox",
            tabindex="-1",
            data_slot="dropdown-menu-checkbox-item",
            data_attr_aria_checked=checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def DropdownMenuRadioGroup(
    *children,
    signal: str | Signal,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, radio_signal=getattr(signal, "_id", signal), **ctx) for child in children],
            role="radiogroup",
            data_slot="dropdown-menu-radio-group",
            cls=cls,
            **kwargs,
        )

    return _


def DropdownMenuRadioItem(
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
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            data_on_click=click_actions if not disabled else None,
            cls=_dropdown_item_cls(inset="pl-8 pr-2", disabled=disabled, cls=cls),
            type="button",
            role="menuitemradio",
            tabindex="-1",
            data_slot="dropdown-menu-radio-item",
            data_attr_aria_checked=is_checked.if_("true", "false"),
            disabled=disabled,
            **kwargs,
        )

    return _


def DropdownMenuSeparator(cls: str = "", **kwargs) -> FT:
    return Hr(
        data_slot="dropdown-menu-separator",
        cls=cn("-mx-1 my-1 h-px border-0 bg-border", cls),
        **kwargs,
    )


def DropdownMenuLabel(*children, inset: bool = False, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="dropdown-menu-label",
        cls=cn(
            "px-2 py-1.5 text-sm font-medium",
            "pl-8" if inset else "",
            cls,
        ),
        **kwargs,
    )


def DropdownMenuShortcut(*children, cls: str = "", **kwargs) -> FT:
    return Span(
        *children,
        data_slot="dropdown-menu-shortcut",
        aria_hidden="true",
        cls=cn("ml-auto text-xs tracking-widest text-muted-foreground", cls),
        **kwargs,
    )


def DropdownMenuGroup(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            role="group",
            data_slot="dropdown-menu-group",
            cls=cls,
            **kwargs,
        )

    return _


def DropdownMenuSub(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**ctx):
        sub = getattr(signal, "_id", signal) or gen_id("dropdown_sub")
        sub_open = Signal(f"{sub}_open", False)
        ctx = dict(
            sub_open=sub_open,
            sub_trigger_ref=Signal(f"{sub}_trigger", _ref_only=True),
            sub_content_ref=Signal(f"{sub}_content", _ref_only=True),
            **ctx,
        )

        return Div(
            sub_open,
            *[inject_context(child, **ctx) for child in children],
            data_slot="dropdown-menu-sub",
            cls=cn("relative", cls),
            **kwargs,
        )

    return _


def DropdownMenuSubTrigger(
    *children,
    inset: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sub_open, sub_trigger_ref, sub_content_ref, **_):
        return HTMLButton(
            *children,
            Icon("lucide:chevron-right", cls="ml-auto size-4"),
            data_ref=sub_trigger_ref,
            id=sub_trigger_ref._id,
            popovertarget=sub_content_ref._id,
            popoveraction="toggle",
            data_on_click=merge_actions(kwargs=kwargs) or None,
            cls=cn(
                _dropdown_item_cls(inset="pl-8" if inset else "", cls=cls),
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
            ),
            data_attr_data_state=sub_open.if_("open", "closed"),
            type="button",
            role="menuitem",
            tabindex="-1",
            data_slot="dropdown-menu-sub-trigger",
            aria_haspopup="menu",
            data_attr_aria_expanded=sub_open.if_("true", "false"),
            **kwargs,
        )

    return _


def DropdownMenuSubContent(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sub_open, sub_trigger_ref, sub_content_ref, **ctx):
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
            data_slot="dropdown-menu-sub-content",
            cls=cn(
                "z-50 max-h-[min(var(--popover-available-height,80vh),80vh)] min-w-[8rem]",
                "overflow-x-hidden overflow-y-auto rounded-md border",
                "bg-popover p-1 text-popover-foreground shadow-lg",
                cls,
            ),
            **kwargs,
        )

    return _
