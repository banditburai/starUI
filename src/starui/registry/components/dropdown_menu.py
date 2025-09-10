from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div, Hr, Icon, Span
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_on_click, ds_position, ds_ref, ds_show, ds_computed, ds_style, ds_signals, t, toggle_signal

from .button import Button
from .utils import cn


def DropdownMenu(
    *children, 
    signal: str | None = None, 
    cls: str = "", 
    **kwargs: Any
) -> FT:
    signal = signal or f"dropdown_{uuid4().hex[:8]}"
    return Div(
        ds_signals({
            f"{signal}_open": False,
        }),
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
    class_name: str = "",
    **kwargs: Any,
):
    def _trigger(signal):
        trigger_id = f"{signal}-trigger"
        
        if as_child and children:
            child = children[0]
            if hasattr(child, "attrs"):
                child.attrs.update({                 
                    "popovertarget": f"{signal}-content",
                    "popoveraction": "toggle",
                    "id": trigger_id,
                })
            return child
        
        return Button(
            *children,
            ds_ref(f"{signal}_trigger"),
            variant=variant,
            size=size,
            popovertarget=f"{signal}-content",
            popoveraction="toggle",
            id=trigger_id,
            type="button",
            cls=cn(class_name, cls),
            **kwargs,
        )
    
    return _trigger


def DropdownMenuContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "start",
    side_offset: int = 4,    
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _content(signal):
        placement = f"{side}-{align}" if align != "center" else side
        
        return Div(
            *[child(signal) if callable(child) else child for child in children],
            ds_ref(f"{signal}_content"),                        
            ds_style(min_width=f"${signal}_trigger ? ${signal}_trigger.offsetWidth + 'px' : '8rem'"),
            ds_position(
                anchor=f"{signal}-trigger",
                placement=placement,
                offset=side_offset,
                flip=True,
                shift=True,
                hide=True,
            ),
            popover="auto",
            id=f"{signal}-content",
            role="menu",
            aria_labelledby=f"{signal}-trigger",
            tabindex="-1",
            cls=cn(
                "z-50 min-w-[8rem] overflow-hidden rounded-md border border-input",
                "bg-popover text-popover-foreground shadow-lg p-1",
                class_name,
                cls,
            ),
            **kwargs,
        )
    
    return _content


def DropdownMenuItem(
    *children,
    onclick: str | None = None,
    variant: Literal["default", "destructive"] = "default",
    inset: bool = False,
    disabled: bool = False,    
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _item(signal):
        variant_classes = {
            "default": "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            "destructive": "text-destructive hover:bg-destructive/10 hover:text-destructive focus:bg-destructive/10 focus:text-destructive",
        }
        close_popover = f"${signal}_content.hidePopover()"
        click_handler = f"{onclick}; {close_popover}" if onclick else close_popover
        
        return HTMLButton(
            *children,
            ds_on_click(click_handler) if not disabled else None,
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5",
                "text-sm outline-none transition-colors",
                variant_classes.get(variant, variant_classes["default"]),
                "pl-8" if inset else "",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            disabled=disabled,
            role="menuitem",
            **kwargs,
        )
    
    return _item


def DropdownMenuCheckboxItem(
    *children,
    signal: str,
    inset: bool = False,
    disabled: bool = False,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _checkbox_item(dropdown_signal):
        toggle_handler = (
            f"{toggle_signal(signal)}; "
            f"${dropdown_signal}_content.hidePopover()"
        ) if not disabled else None
        
        return HTMLButton(
            Span(
                Icon("lucide:check"),
                ds_show(f"${signal}"),
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            ds_on_click(toggle_handler) if toggle_handler else None,
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm",
                "py-1.5 pr-2 pl-8 text-sm outline-none transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                "focus:bg-accent focus:text-accent-foreground",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            role="menuitemcheckbox",
            aria_checked=t("{signal} ? 'true' : 'false'"),
            disabled=disabled,
            **kwargs,
        )
    
    return _checkbox_item


def DropdownMenuRadioGroup(
    *children,
    signal: str,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    return lambda dropdown_signal: Div(
        *[child(dropdown_signal) if callable(child) else child for child in children],
        role="radiogroup",
        cls=cn(class_name, cls),
        **kwargs,
    )


def DropdownMenuRadioItem(
    *children,
    value: str,
    signal: str,
    disabled: bool = False,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _radio_item(dropdown_signal):
        select_handler = (
            f"${signal} = '{value}'; "
            f"${dropdown_signal}_content.hidePopover()"
        ) if not disabled else None
        
        return HTMLButton(
            Span(
                Icon("lucide:circle", cls="size-2 fill-current"),
                ds_show(f"${signal} === '{value}'"),
                cls="absolute left-2 flex size-3.5 items-center justify-center",
            ),
            *children,
            ds_on_click(select_handler) if select_handler else None,
            cls=cn(
                "relative flex w-full cursor-default select-none items-center gap-2 rounded-sm",
                "py-1.5 pr-2 pl-8 text-sm outline-none transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                "focus:bg-accent focus:text-accent-foreground",
                "pointer-events-none opacity-50" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4",
                "[&_iconify-icon]:size-4 [&_iconify-icon]:shrink-0",
                class_name,
                cls,
            ),
            type="button",
            role="menuitemradio",
            aria_checked=t("{signal} === '{value}' ? 'true' : 'false'"),
            disabled=disabled,
            **kwargs,
        )
    
    return _radio_item


def DropdownMenuSeparator(cls: str = "", class_name: str = "", **kwargs: Any):
    return lambda _: Hr(
        cls=cn("-mx-1 my-1 border-t border-input", class_name, cls), 
        **kwargs
    )


def DropdownMenuLabel(
    *children, 
    inset: bool = False, 
    cls: str = "", 
    class_name: str = "", 
    **kwargs: Any
):
    return lambda _: Div(
        *children,
        cls=cn(
            "px-2 py-1.5 text-sm font-medium",
            "pl-8" if inset else "",
            class_name,
            cls,
        ),
        **kwargs,
    )


def DropdownMenuShortcut(
    *children,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    return Span(
        *children,
        cls=cn(
            "ml-auto text-xs tracking-widest text-muted-foreground",
            class_name,
            cls,
        ),
        **kwargs,
    )


def DropdownMenuGroup(
    *children,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    return lambda signal: Div(
        *[child(signal) if callable(child) else child for child in children],
        role="group",
        cls=cn(class_name, cls),
        **kwargs,
    )


def DropdownMenuSub(
    *children,
    signal: str | None = None,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    signal = signal or f"dropdown_sub_{uuid4().hex[:8]}"
    return Div(
        ds_signals({f"{signal}_open": False }),
        *[child(signal) if callable(child) else child for child in children],
        cls=cn("relative", class_name, cls),
        **kwargs,
    )


def DropdownMenuSubTrigger(
    *children,
    inset: bool = False,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _sub_trigger(signal):
        return HTMLButton(
            *children,
            Icon("lucide:chevron-right", cls="ml-auto size-4"),
            ds_on_click(toggle_signal(f"{signal}_open")),
            cls=cn(
                "flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5",
                "text-sm outline-none transition-colors",
                "hover:bg-accent hover:text-accent-foreground",
                "focus:bg-accent focus:text-accent-foreground",
                "data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
                "pl-8" if inset else "",
                class_name,
                cls,
            ),
            data_state=t("{signal}_open ? 'open' : 'closed'"),
            type="button",
            role="menuitem",
            aria_haspopup="menu",
            aria_expanded=t("{signal}_open ? 'true' : 'false'"),
            **kwargs,
        )
    
    return _sub_trigger


def DropdownMenuSubContent(
    *children,
    cls: str = "",
    class_name: str = "",
    **kwargs: Any,
):
    def _sub_content(signal):
        return Div(
            *[child(signal) if callable(child) else child for child in children],
            ds_show(f"${signal}_open"),
            cls=cn(
                "absolute left-full top-0 ml-1 z-50",
                "min-w-[8rem] overflow-hidden rounded-md border border-input",
                "bg-popover text-popover-foreground shadow-lg",
                "p-1",
                class_name,
                cls,
            ),
            role="menu",
            **kwargs,
        )
    
    return _sub_content