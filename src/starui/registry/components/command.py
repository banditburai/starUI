from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div, Icon, Input, Span
from starhtml import Dialog as HTMLDialog
from starhtml.datastar import (
    ds_attr,
    ds_bind,
    ds_effect,
    ds_on,
    ds_on_click,
    ds_on_close,
    ds_on_input,
    ds_on_keydown,
    ds_on_mouseenter,
    ds_ref,
    ds_show,
    ds_signals,
    value,
)

from .utils import cn, cva

CommandSize = Literal["sm", "md", "lg"]
_command_item_counters = {}


def _get_filter_effect(signal: str) -> str:
    return f"const i=document.querySelectorAll('[data-command-item=\"{signal}\"]'),s=${signal}_search.toLowerCase();let v=0;i.forEach(e=>{{const m=!s||(e.dataset.value||'').toLowerCase().includes(s)||(e.dataset.keywords||'').toLowerCase().includes(s)||(e.textContent||'').toLowerCase().includes(s);e.style.display=m?'':'none';e.dataset.filtered=m?'false':'true';m&&e.dataset.disabled!=='true'&&v++}});document.querySelectorAll('[data-command-group=\"{signal}\"]').forEach(g=>{{g.style.display=Array.from(g.querySelectorAll('[data-command-item=\"{signal}\"]')).some(i=>i.dataset.filtered==='false')?'':'none'}});document.querySelectorAll('[data-command-empty=\"{signal}\"]').forEach(e=>{{e.style.display=v>0?'none':''}});"


def _get_search_handler(signal: str) -> str:
    return f'clearTimeout(window._st_{signal});window._st_{signal}=setTimeout(()=>{{const v=document.querySelectorAll(\'[data-command-item="{signal}"]:not([style*="none"]):not([data-disabled="true"])\');if(v.length>0)${signal}_selected=parseInt(v[0].dataset.index||\'0\')}},50)'


def _get_nav_handler(signal: str, ref_id: str = None) -> str:
    escape_check = f"!document.getElementById('{ref_id}')" if ref_id else "true"
    return f"const i=[...document.querySelectorAll('[data-command-item=\"{signal}\"]:not([data-filtered=\"true\"]):not([data-disabled=\"true\"])')];let c=-1;i.forEach((e,x)=>{{if(parseInt(e.dataset.index)===${signal}_selected)c=x}});switch(event.key){{case'ArrowDown':event.preventDefault();if(i.length>0){{const n=c<i.length-1?c+1:0;${signal}_selected=parseInt(i[n].dataset.index);i[n].scrollIntoView({{block:'nearest'}})}}break;case'ArrowUp':event.preventDefault();if(i.length>0){{const p=c>0?c-1:i.length-1;${signal}_selected=parseInt(i[p].dataset.index);i[p].scrollIntoView({{block:'nearest'}})}}break;case'Enter':event.preventDefault();if(c>=0&&i[c])i[c].click();break;case'Escape':if({escape_check}){{event.preventDefault();${signal}_search='';${signal}_selected=0}}break}}"


def _get_dialog_open_effect(signal: str, ref_id: str) -> str:
    return f"{_get_filter_effect(signal)};if(${ref_id}_open&&!${signal}_search)setTimeout(()=>{{const f=document.querySelector('[data-command-item=\"{signal}\"]:not([data-disabled=\"true\"])');if(f)${signal}_selected=parseInt(f.dataset.index||'0')}},50)"


def _init_command_signals(signal: str) -> dict:
    return {f"{signal}_search": value(""), f"{signal}_selected": 0}


def _process_children(children, signal):
    return [c(signal) if callable(c) else c for c in children]


command_variants = cva(
    base="flex w-full flex-col overflow-hidden rounded-lg border border-input bg-popover text-popover-foreground shadow-md",
    config={
        "variants": {
            "size": {
                "sm": "max-h-[300px]",
                "md": "max-h-[400px] md:min-w-[450px]",
                "lg": "max-h-[500px] md:min-w-[450px]",
            }
        },
        "defaultVariants": {"size": "md"},
    },
)


def Command(
    *children: Any,
    signal: str | None = None,
    size: CommandSize = "md",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"command_{uuid4().hex[:8]}"

    global _command_item_counters
    _command_item_counters[signal] = 0

    return Div(
        *_process_children(children, signal),
        ds_signals(**_init_command_signals(signal)),
        ds_effect(_get_filter_effect(signal)),
        data_command_root=signal,
        data_slot="command",
        tabindex="-1",
        cls=cn(command_variants(size=size), class_name, cls),
        **attrs,
    )


def CommandDialog(
    trigger: FT,
    content: list[FT],
    signal: str | None = None,
    modal: bool = True,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"command_{uuid4().hex[:8]}"
    ref_id = f"{signal}_dialog"
    signal_open = f"{ref_id}_open"

    global _command_item_counters
    _command_item_counters[signal] = 0

    reset_signals = f"${signal_open}=false;${signal}_search='';${signal}_selected=0;document.body.style.overflow=''"

    dialog_attrs = [
        ds_signals(**{**_init_command_signals(signal), signal_open: False}),
        ds_ref(ref_id),
        ds_on_close(reset_signals),
        ds_on_keydown(
            f"if(evt.key==='Escape'){{evt.preventDefault();const d=document.getElementById('{ref_id}');if(d){{d.close();d.style.display='none';{reset_signals};setTimeout(()=>{{d.style.display=''}},100)}}}}"
        ),
        ds_effect(_get_dialog_open_effect(signal, ref_id)),
    ]

    if modal:
        dialog_attrs.append(
            ds_on(
                "click",
                f"if(evt.target===evt.currentTarget){{evt.currentTarget.close();{reset_signals}}}",
            )
        )

    command_dialog = HTMLDialog(
        *_process_children(content, signal),
        *dialog_attrs,
        id=ref_id,
        data_command_root=signal,
        data_slot="command",
        tabindex="-1",
        cls=cn(
            "fixed max-h-[85vh] w-full max-w-2xl overflow-auto m-auto p-0",
            "backdrop:bg-black/50 backdrop:backdrop-blur-sm",
            "open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200",
            "open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
            "flex flex-col overflow-hidden rounded-lg",
            "border border-input bg-popover text-popover-foreground shadow-lg",
            "md:min-w-[450px]",
            class_name,
            cls,
        ),
        **attrs,
    )

    method = "showModal" if modal else "show"
    trigger_elem = Div(
        trigger,
        ds_on_click(f"${ref_id}.{method}();${signal_open}=true"),
        style="display:contents",
    )

    scroll_lock = Div(
        ds_effect(f"document.body.style.overflow=${signal_open}?'hidden':''"),
        style="display:none",
    )

    return Div(trigger_elem, command_dialog, scroll_lock)


def CommandInput(
    placeholder: str = "Type a command or search...",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
):
    def _(signal):
        return Div(
            Icon("lucide:search", cls="size-4 shrink-0 opacity-50"),
            Input(
                ds_bind(f"{signal}_search"),
                ds_on_keydown(_get_nav_handler(signal, f"{signal}_dialog")),
                ds_on_input(_get_search_handler(signal)),
                placeholder=placeholder,
                data_slot="command-input",
                cls="flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
                autocomplete="off",
                autocorrect="off",
                spellcheck="false",
                type="text",
                **attrs,
            ),
            data_slot="command-input-wrapper",
            cls=cn(
                "flex h-9 items-center gap-2 border-b border-border px-3",
                class_name,
                cls,
            ),
        )

    return _


def CommandList(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
):
    def _(signal):
        return Div(
            *_process_children(children, signal),
            role="listbox",
            aria_label="Commands",
            data_command_list=signal,
            data_slot="command-list",
            cls=cn(
                "max-h-[300px] scroll-py-1 overflow-x-hidden overflow-y-auto",
                class_name,
                cls,
            ),
            **attrs,
        )

    return _


def CommandEmpty(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
):
    def _(signal):
        return Div(
            *(children or ["No results found."]),
            data_command_empty=signal,
            data_slot="command-empty",
            style="display: none;",
            cls=cn("py-6 text-center text-sm", class_name, cls),
            **attrs,
        )

    return _


def CommandGroup(
    *children,
    heading: str | None = None,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
):
    def _(signal):
        return Div(
            *(
                [
                    Div(
                        heading,
                        data_slot="command-group-heading",
                        cls="text-muted-foreground px-2 py-1.5 text-xs font-medium",
                        aria_hidden="true",
                    )
                ]
                if heading
                else []
            ),
            *_process_children(children, signal),
            role="group",
            data_command_group=signal,
            data_slot="command-group",
            cls=cn(
                "overflow-hidden p-1 text-foreground",
                "[&_[data-slot='command-group-heading']]:text-muted-foreground",
                "[&_[data-slot='command-group-heading']]:px-2",
                "[&_[data-slot='command-group-heading']]:py-1.5",
                "[&_[data-slot='command-group-heading']]:text-xs",
                "[&_[data-slot='command-group-heading']]:font-medium",
                class_name,
                cls,
            ),
            **attrs,
        )

    return _


def CommandItem(
    *children,
    value: str,
    onclick: str | None = None,
    disabled: bool = False,
    keywords: str | None = None,
    show: str | None = None,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
):
    def _(signal):
        index = attrs.pop("index", attrs.pop("data_index", None))

        if index is None:
            global _command_item_counters
            _command_item_counters.setdefault(signal, 0)
            index = _command_item_counters[signal]
            _command_item_counters[signal] += 1

        event_attrs = []
        if not disabled:
            if onclick:
                click_handler = f"{onclick};const d=document.querySelector('dialog[data-command-root=\"{signal}\"]');if(d){{d.close();d.style.display='none';${signal}_dialog_open=false;${signal}_search='';${signal}_selected=0;document.body.style.overflow='';setTimeout(()=>{{d.style.display=''}},100)}}"
                event_attrs.append(ds_on_click(click_handler))
            event_attrs.append(ds_on_mouseenter(f"${signal}_selected={index}"))
        
        # Add ds_show if show condition is provided
        show_attrs = []
        if show:
            show_attrs.append(ds_show(show))

        return Div(
            *children,
            *event_attrs,
            *show_attrs,
            ds_attr(data_selected=f"${signal}_selected==={index}?'true':'false'"),
            role="option",
            aria_selected=f"${{{signal}_selected}} === {index}",
            aria_disabled="true" if disabled else "false",
            data_command_item=signal,
            data_slot="command-item",
            data_value=value,
            data_keywords=keywords or "",
            data_disabled="true" if disabled else "false",
            data_index=str(index),
            cls=cn(
                "relative flex cursor-default items-center gap-2 rounded-sm px-2 py-1.5",
                "text-sm outline-none select-none transition-colors",
                "hover:bg-accent/50 data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground"
                if not disabled
                else "",
                "[&_svg:not([class*='text-'])]:text-muted-foreground",
                "opacity-50 cursor-not-allowed pointer-events-none" if disabled else "",
                "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
                class_name,
                cls,
            ),
            **attrs,
        )

    return _


def CommandSeparator(class_name: str = "", cls: str = "", **attrs: Any):
    return lambda signal: Div(
        role="separator",
        data_slot="command-separator",
        cls=cn("-mx-1 h-px bg-border", class_name, cls),
        **attrs,
    )


def CommandDialogWithTrigger(trigger: FT, content: FT | list, **kwargs) -> FT:
    """Backward compatibility wrapper."""
    if not isinstance(content, list | tuple):
        content = [content]
    return CommandDialog(*content, trigger=trigger, **kwargs)


def CommandShortcut(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    return Span(
        *children,
        data_slot="command-shortcut",
        cls=cn(
            "ml-auto text-xs tracking-widest text-muted-foreground",
            class_name,
            cls,
        ),
        **attrs,
    )
