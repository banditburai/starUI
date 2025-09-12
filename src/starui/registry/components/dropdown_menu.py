from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div, Hr, Icon, Span
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_on_click, ds_position, ds_ref, ds_show, ds_style, ds_signals, t, toggle_signal

from .button import Button
from .utils import cn, cva

dropdown_item_variants = cva(
    base=(
        "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 "
        "text-sm outline-none transition-colors "
        "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4 "
        "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0"
    ),
    config={
        "variants": {
            "variant": {
                "default": "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                "destructive": "text-destructive hover:bg-destructive/10 hover:text-destructive focus:bg-destructive/10 focus:text-destructive",
            },
        },
        "defaultVariants": {"variant": "default"},
    },
)


def DropdownMenu(
    *children, 
    signal: str | None = None, 
    cls: str = "", 
    **kwargs: Any
) -> FT:
    signal = signal or f"dropdown_{uuid4().hex[:8]}"
    return Div(
        ds_signals({f"{signal}_open": False}),
        *[child(signal) if callable(child) else child for child in children],
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def DropdownMenuTrigger(
    *children,
    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = "outline",
    size: Literal["default", "sm", "lg", "icon"] = "default",
    as_child: bool = False,    
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(signal):
        trigger_id = f"{signal}_trigger"
        popover_attrs = {
            "popovertarget": f"{signal}_content",
            "popoveraction": "toggle",
            "id": trigger_id,
        }
        
        if as_child and children and hasattr(children[0], "attrs"):
            children[0].attrs.update(popover_attrs)
            return children[0]
        
        return Button(
            *children,
            ds_ref(f"{signal}_trigger"),
            variant=variant,
            size=size,
            type="button",
            cls=cls,
            **popover_attrs,
            **kwargs,
        )
    
    return _


def DropdownMenuContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 4,    
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(signal):        
        return Div(
            *[child(signal) if callable(child) else child for child in children],
            ds_ref(f"{signal}_content"),                        
            ds_style(min_width=f"${signal}_trigger ? ${signal}_trigger.offsetWidth + 'px' : '8rem'"),
            ds_position(
                anchor=f"{signal}_trigger",
                placement=f"{side}-{align}" if align != "center" else side,
                offset=side_offset,
                flip=True,
                shift=True,
                hide=True,
            ),
            popover="auto",
            id=f"{signal}_content",
            role="menu",
            aria_labelledby=f"{signal}_trigger",
            tabindex="-1",
            cls=cn(
                "z-50 min-w-[8rem] overflow-hidden rounded-md border border-input",
                "bg-popover text-popover-foreground shadow-lg p-1",
                cls,
            ),
            **kwargs,
        )
    
    return _


def DropdownMenuItem(
    *children,
    onclick: str | None = None,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,    
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(signal):
        click_handler = f"{onclick}; ${signal}_content.hidePopover()" if onclick else f"${signal}_content.hidePopover()"
        
        return HTMLButton(
            *children,
            ds_on_click(click_handler) if not disabled else None,
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
    signal: str,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(dropdown_signal):
        return HTMLButton(
            Span(
                Icon("lucide:check"),
                ds_show(f"${signal}"),
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            ds_on_click(f"{toggle_signal(signal)}; ${dropdown_signal}_content.hidePopover()") if not disabled else None,
            cls=cn(
                dropdown_item_variants(variant="default"),
                "pl-8 pr-2",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemcheckbox",
            aria_checked=t("{signal} ? 'true' : 'false'"),
            disabled=disabled,
            **kwargs,
        )
    
    return _


def DropdownMenuRadioGroup(
    *children,
    signal: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(dropdown_signal):
        return Div(
            *[child(dropdown_signal) if callable(child) else child for child in children],
            role="radiogroup",
            cls=cls,
            **kwargs,
        )
    return _


def DropdownMenuRadioItem(
    *children,
    value: str,
    signal: str,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(dropdown_signal):
        return HTMLButton(
            Span(
                Icon("lucide:circle", cls="size-2 fill-current"),
                ds_show(f"${signal} === '{value}'"),
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            ds_on_click(f"${signal} = '{value}'; ${dropdown_signal}_content.hidePopover()") if not disabled else None,
            cls=cn(
                dropdown_item_variants(variant="default"),
                "pl-8 pr-2",
                "pointer-events-none opacity-50" if disabled else "",
                cls,
            ),
            type="button",
            role="menuitemradio",
            aria_checked=t("{signal} === '{value}' ? 'true' : 'false'"),
            disabled=disabled,
            **kwargs,
        )
    
    return _


def DropdownMenuSeparator(cls: str = "", **kwargs: Any) -> FT:
    def _(_):
        return Hr(
            cls=cn("-mx-1 my-1 border-t border-input", cls), 
            **kwargs
        )
    return _


def DropdownMenuLabel(
    *children, 
    inset: bool = False, 
    cls: str = "", 
    **kwargs: Any
) -> FT:
    def _(_):
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
    def _(signal):
        return Div(
            *[child(signal) if callable(child) else child for child in children],
            role="group",
            cls=cls,
            **kwargs,
        )
    return _


def DropdownMenuSub(
    *children,
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"dropdown_sub_{uuid4().hex[:8]}"
    return Div(
        ds_signals({f"{signal}_open": False}),
        *[child(signal) if callable(child) else child for child in children],
        cls=cn("relative", cls),
        **kwargs,
    )


def DropdownMenuSubTrigger(
    *children,
    inset: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(signal):
        return HTMLButton(
            *children,
            Icon("lucide:chevron-right", cls="ml-auto size-4"),
            ds_on_click(toggle_signal(f"{signal}_open")),
            cls=cn(
                dropdown_item_variants(variant="default"),
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
                "pl-8" if inset else "",
                cls,
            ),
            data_state=t("{signal}_open ? 'open' : 'closed'"),
            type="button",
            role="menuitem",
            aria_haspopup="menu",
            aria_expanded=t("{signal}_open ? 'true' : 'false'"),
            **kwargs,
        )
    
    return _


def DropdownMenuSubContent(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(signal):
        return Div(
            *[child(signal) if callable(child) else child for child in children],
            ds_show(f"${signal}_open"),
            cls=cn(
                "absolute left-full top-0 ml-1 z-50",
                "min-w-[8rem] overflow-hidden rounded-md border border-input",
                "bg-popover text-popover-foreground shadow-lg p-1",
                cls,
            ),
            role="menu",
            **kwargs,
        )
    
    return _