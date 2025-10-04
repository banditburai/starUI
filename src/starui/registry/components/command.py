from typing import Any, Literal

from starhtml import FT, Div, Icon, Input, Span, Signal, js
from starhtml import Dialog as HTMLDialog
from starhtml.datastar import evt, document, seq

from .utils import cn, cva, gen_id

CommandSize = Literal["sm", "md", "lg"]

_SEARCH_DEBOUNCE_MS = 50
_DIALOG_FOCUS_DELAY_MS = 50


def _get_filter_effect(sig: str, search) -> str:
    return f"const i=document.querySelectorAll('[data-command-item=\"{sig}\"]'),s={search}.toLowerCase();let v=0;i.forEach(e=>{{const m=!s||(e.dataset.value||'').toLowerCase().includes(s)||(e.dataset.keywords||'').toLowerCase().includes(s)||(e.textContent||'').toLowerCase().includes(s);e.style.display=m?'':'none';e.dataset.filtered=m?'false':'true';m&&e.dataset.disabled!=='true'&&v++}});document.querySelectorAll('[data-command-group=\"{sig}\"]').forEach(g=>{{g.style.display=[...g.querySelectorAll('[data-command-item=\"{sig}\"]')].some(i=>i.dataset.filtered==='false')?'':'none'}});document.querySelectorAll('[data-command-empty=\"{sig}\"]').forEach(e=>{{e.style.display=v>0?'none':''}})"


def _get_search_handler(sig: str, selected) -> str:
    return f"clearTimeout(window._st_{sig});window._st_{sig}=setTimeout(()=>{{const v=document.querySelectorAll('[data-command-item=\"{sig}\"]:not([style*=\"none\"]):not([data-disabled=\"true\"])');if(v.length>0){selected}=parseInt(v[0].dataset.index||'0')}},{_SEARCH_DEBOUNCE_MS})"


def _get_nav_handler(sig: str, search, selected, dialog_ref=None) -> str:
    esc = f"!{dialog_ref}" if dialog_ref else "true"
    return f"const i=[...document.querySelectorAll('[data-command-item=\"{sig}\"]:not([data-filtered=\"true\"]):not([data-disabled=\"true\"])')];let c=-1;i.forEach((e,x)=>{{if(parseInt(e.dataset.index)==={selected})c=x}});switch(event.key){{case'ArrowDown':event.preventDefault();if(i.length>0){{const n=c<i.length-1?c+1:0;{selected}=parseInt(i[n].dataset.index);i[n].scrollIntoView({{block:'nearest'}})}}break;case'ArrowUp':event.preventDefault();if(i.length>0){{const p=c>0?c-1:i.length-1;{selected}=parseInt(i[p].dataset.index);i[p].scrollIntoView({{block:'nearest'}})}}break;case'Enter':event.preventDefault();if(c>=0&&i[c])i[c].click();break;case'Escape':if({esc}){{event.preventDefault();{search}='';{selected}=0}}break}}"


def _get_dialog_open_effect(sig: str, search, selected, dialog_open, dialog_ref) -> str:
    return f"{_get_filter_effect(sig, search)};if({dialog_open}&&!{search})setTimeout(()=>{{const f=document.querySelector('[data-command-item=\"{sig}\"]:not([data-disabled=\"true\"])');if(f){selected}=parseInt(f.dataset.index||'0')}},{_DIALOG_FOCUS_DELAY_MS})"


command_variants = cva(
    base=(
        "flex w-full flex-col overflow-hidden rounded-lg border border-input "
        "bg-popover text-popover-foreground shadow-md"
    ),
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
    signal: str | Signal = "",
    size: CommandSize = "md",
    label: str = "Command Menu",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("command")
    counter = {"value": 0}
    search = Signal(f"{sig}_search", "")
    selected = Signal(f"{sig}_selected", 0)

    ctx = dict(sig=sig, search=search, selected=selected, counter=counter, dialog_ref=None)

    return Div(
        search,
        selected,
        *[c(**ctx) if callable(c) else c for c in children],
        data_effect=js(_get_filter_effect(sig, search)),
        data_command_root=sig,
        data_slot="command",
        aria_label=label,
        tabindex="-1",
        cls=cn(command_variants(size=size), cls),
        **kwargs,
    )


def CommandDialog(
    trigger: FT,
    content: list[FT],
    signal: str | Signal = "",
    modal: bool = True,
    label: str = "Command Menu",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("command")
    dialog_id = f"{sig}_dialog"
    dialog_ref = Signal(dialog_id, _ref_only=True)
    counter = {"value": 0}

    search = Signal(f"{sig}_search", "")
    selected = Signal(f"{sig}_selected", 0)
    dialog_open = Signal(f"{dialog_id}_open", False)

    reset_signals = [
        dialog_open.set(False),
        search.set(""),
        selected.set(0),
    ]

    ctx = dict(sig=sig, search=search, selected=selected, counter=counter, dialog_ref=dialog_ref)

    command_dialog = HTMLDialog(
        search,
        selected,
        dialog_open,
        *[c(**ctx) if callable(c) else c for c in content],
        data_ref=dialog_id,
        data_on_close=reset_signals,
        data_on_keydown=(evt.key == 'Escape') & seq(evt.preventDefault(), evt.currentTarget.close()),
        data_on_click=(evt.target == evt.currentTarget) & evt.currentTarget.close() if modal else None,
        data_effect=js(_get_dialog_open_effect(sig, search, selected, dialog_open, dialog_ref)),
        id=dialog_id,
        data_command_root=sig,
        data_slot="command",
        aria_label=label,
        tabindex="-1",
        cls=cn(
            "fixed max-h-[85vh] w-full max-w-2xl m-auto p-0",
            "backdrop:bg-black/50 backdrop:backdrop-blur-sm",
            "open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200",
            "open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
            "open:flex open:flex-col overflow-hidden rounded-lg",
            "border border-input bg-popover text-popover-foreground shadow-lg",
            "md:min-w-[450px]",
            cls,
        ),
        **kwargs,
    )

    show_method = dialog_ref.showModal() if modal else dialog_ref.show()
    trigger_elem = Div(
        trigger,
        data_on_click=[show_method, dialog_open.set(True)],
        style="display:contents",
    )

    scroll_lock = Div(
        data_effect=document.body.style.overflow.set(dialog_open.if_('hidden', '')),
        style="display:none",
    )

    return Div(trigger_elem, command_dialog, scroll_lock)


def CommandInput(
    placeholder: str = "Type a command or search...",
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, search, selected, dialog_ref, **_):
        return Div(
            Icon("lucide:search", cls="size-4 shrink-0 opacity-50"),
            Input(
                data_bind=search,
                data_on_keydown=js(_get_nav_handler(sig, search, selected, dialog_ref)) if dialog_ref else js(_get_nav_handler(sig, search, selected)),
                data_on_input=js(_get_search_handler(sig, selected)),
                placeholder=placeholder,
                data_slot="command-input",
                cls="flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
                autocomplete="off",
                autocorrect="off",
                spellcheck="false",
                type="text",
                **kwargs,
            ),
            data_slot="command-input-wrapper",
            cls=cn(
                "flex h-9 items-center gap-2 border-b border-border px-3",
                cls,
            ),
        )

    return _


def CommandList(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, **ctx):
        return Div(
            *[c(sig=sig, **ctx) if callable(c) else c for c in children],
            role="listbox",
            aria_label="Commands",
            data_command_list=sig,
            data_slot="command-list",
            cls=cn(
                "max-h-[300px] scroll-py-1 overflow-x-hidden overflow-y-auto",
                cls,
            ),
            **kwargs,
        )

    return _


def CommandEmpty(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, **_):
        return Div(
            *(children or ["No results found."]),
            data_command_empty=sig,
            data_slot="command-empty",
            style="display: none;",
            cls=cn("py-6 text-center text-sm", cls),
            **kwargs,
        )

    return _


def CommandGroup(
    *children,
    heading: str | None = None,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, **ctx):
        return Div(
            Div(
                heading,
                data_slot="command-group-heading",
                cls="text-muted-foreground px-2 py-1.5 text-xs font-medium",
                aria_hidden="true",
            ) if heading else None,
            *[c(sig=sig, **ctx) if callable(c) else c for c in children],
            role="group",
            data_command_group=sig,
            data_slot="command-group",
            cls=cn(
                "overflow-hidden p-1 text-foreground",
                "[&_[data-slot='command-group-heading']]:text-muted-foreground [&_[data-slot='command-group-heading']]:px-2 [&_[data-slot='command-group-heading']]:py-1.5 [&_[data-slot='command-group-heading']]:text-xs [&_[data-slot='command-group-heading']]:font-medium",
                cls,
            ),
            **kwargs,
        )

    return _


def CommandItem(
    *children,
    value: str,
    onclick: str | None = None,
    disabled: bool = False,
    keywords: str | None = None,
    show: str | None = None,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, selected, counter, dialog_ref, **_):
        index = counter["value"]
        counter["value"] += 1

        click_actions = ([js(onclick)] if onclick else []) + ([dialog_ref.close()] if dialog_ref else [])

        return Div(
            *children,
            data_on_click=click_actions if (click_actions and not disabled) else None,
            data_on_mouseenter=selected.set(index) if not disabled else None,
            data_show=show if show else None,
            data_attr_data_selected=selected.eq(index).if_("true", "false"),
            data_attr_aria_selected=selected.eq(index),
            role="option",
            aria_disabled="true" if disabled else "false",
            data_command_item=sig,
            data_slot="command-item",
            data_value=value,
            data_keywords=keywords or "",
            data_disabled="true" if disabled else "false",
            data_index=str(index),
            cls=cn(
                "relative flex cursor-default items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none select-none transition-colors",
                "[&_svg:not([class*='text-'])]:text-muted-foreground [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
                "hover:bg-accent/50 data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground" if not disabled else "opacity-50 cursor-not-allowed pointer-events-none",
                cls,
            ),
            **kwargs,
        )

    return _


def CommandSeparator(cls: str = "", **kwargs: Any):
    return lambda **_: Div(
        role="separator",
        data_slot="command-separator",
        cls=cn("-mx-1 h-px bg-border", cls),
        **kwargs,
    )


def CommandShortcut(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Span(
        *children,
        data_slot="command-shortcut",
        cls=cn(
            "ml-auto text-xs tracking-widest text-muted-foreground",
            cls,
        ),
        **kwargs,
    )
