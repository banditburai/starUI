from itertools import count
from typing import Any, Literal

from starhtml import FT, Div, Icon, Input, Span, Signal, js, set_timeout, expr
from starhtml import Dialog as HTMLDialog
from starhtml.datastar import evt, document

from .utils import cn, cva, gen_id, with_signals

CommandSize = Literal["sm", "md", "lg"]

_DIALOG_FOCUS_DELAY_MS = 50


def _get_nav_handler(sig, search, selected, visible_items) -> str:
    return f"const i={visible_items}||[];let c=-1;for(let x=0;x<i.length;x++)if(i[x].index==={selected}){{c=x;break}}const sel=idx=>({selected}=idx,document.querySelector('[data-command-item=\"{sig}\"][data-index=\"'+idx+'\"]')?.scrollIntoView({{block:'nearest'}}));switch(evt.key){{case'ArrowDown':evt.preventDefault();i.length>0&&sel(i[c<i.length-1?c+1:0].index);break;case'ArrowUp':evt.preventDefault();i.length>0&&sel(i[c>0?c-1:i.length-1].index);break;case'Enter':evt.preventDefault();c>=0&&i[c]&&document.querySelector('[data-command-item=\"{sig}\"][data-index=\"'+i[c].index+'\"]')?.click();break;case'Escape':{search}&&(evt.preventDefault(),{search}='',{selected}=0);break}}"


command_variants = cva(
    base=(
        "flex w-full flex-col overflow-hidden rounded-lg border border-input "
        "bg-popover text-popover-foreground shadow-md outline-none"
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
    _dialog_ref=None,
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, '_id', signal) or gen_id("command")
    search = Signal(f"{sig}_search", "")
    selected = Signal(f"{sig}_selected", 0)
    visible_count = Signal(f"{sig}_visible", 0)
    visible_items = Signal(f"{sig}_visible_items", [])
    input_ref = Signal(f"{sig}_input", _ref_only=True)

    ctx = dict(
        sig=sig,
        search=search,
        selected=selected,
        visible_count=visible_count,
        visible_items=visible_items,
        input_ref=input_ref,
        _item_index=count(),
        dialog_ref=_dialog_ref,
    )

    return with_signals(
        Div(
            search,
            selected,
            visible_count,
            visible_items,
            *[c(**ctx) if callable(c) else c for c in children],
            data_command_root=sig,
            data_slot="command",
            aria_label=label,
            tabindex="-1",
            cls=cn(command_variants(size=size), cls),
            **kwargs,
        ),
        search=search,
        selected=selected,
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
    sig = getattr(signal, '_id', signal) or gen_id("command")
    dialog_ref = Signal(f"{sig}_dialog", _ref_only=True)
    dialog_open = Signal(f"{dialog_ref._id}_open", False)

    command = Command(
        *content,
        signal=sig,
        _dialog_ref=dialog_ref,
        label=label,
        cls="border-0",
    )

    input_ref = Signal(f"{sig}_input", _ref_only=True)

    reset_signals = [
        dialog_open.set(False),
        command.search.set(""),
        command.selected.set(0),
    ]

    command_dialog = HTMLDialog(
        dialog_open,
        command,
        data_ref=dialog_ref,
        data_on_close=reset_signals,
        data_on_click=(evt.target == evt.currentTarget) & evt.currentTarget.close() if modal else None,
        data_effect=(dialog_open & ~command.search).then(set_timeout(input_ref.focus(), _DIALOG_FOCUS_DELAY_MS)),
        id=dialog_ref._id,
        cls=cn(
            "fixed max-h-[85vh] w-full max-w-2xl m-auto p-0",
            "backdrop:bg-black/50 backdrop:backdrop-blur-sm",
            "open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200",
            "open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
            "open:flex open:flex-col overflow-hidden rounded-lg",
            "bg-popover text-popover-foreground shadow-lg",
            "outline-none",
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
    def _(*, sig, search, selected, visible_items, input_ref, **_):
        return Div(
            Div(
                Icon("lucide:search", width="16", height="16", style="display: block; width: 100%; height: 100%;"),
                style="display: inline-block; width: 16px; height: 16px; flex-shrink: 0; overflow: hidden;",
                cls="opacity-50"
            ),
            Input(
                data_ref=input_ref,
                data_bind=search,
                data_on_keydown=js(_get_nav_handler(sig, search, selected, visible_items)),
                placeholder=placeholder,
                data_slot="command-input",
                cls="flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 focus-visible:ring-0 focus-visible:border-transparent",
                autocomplete="off",
                autocorrect="off",
                spellcheck="false",
                type="text",
                **kwargs,
            ),
            data_slot="command-input-wrapper",
            cls=cn("flex h-9 items-center gap-2 border-b border-border px-3", cls),
        )

    return _


def CommandList(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, visible_count, visible_items, search, selected, **ctx):
        # RAF ensures DOM updates (data-show hiding) complete before scanning
        scan_effect = js(f"""
            {search};
            requestAnimationFrame(() => {{
                const items = [...document.querySelectorAll('[data-command-item="{sig}"]')];
                const visible = items.filter(el => !el.style.display.includes('none') && el.dataset.disabled !== 'true');
                {visible_count} = visible.length;
                {visible_items} = visible.map(el => ({{
                    index: parseInt(el.dataset.index || '0'),
                    el: el
                }}));
                if (visible.length > 0) {selected} = parseInt(visible[0].dataset.index || '0');
            }});
        """)

        return Div(
            *[c(sig=sig, visible_count=visible_count, visible_items=visible_items, search=search, selected=selected, **ctx) if callable(c) else c for c in children],
            data_effect=scan_effect,
            role="listbox",
            aria_label="Commands",
            data_command_list=sig,
            data_slot="command-list",
            cls=cn("max-h-[300px] scroll-py-1 overflow-x-hidden overflow-y-auto outline-none", cls),
            **kwargs,
        )

    return _


def CommandEmpty(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, sig, visible_count, **_):
        return Div(
            *(children or ["No results found."]),
            data_show=visible_count.eq(0),
            data_command_empty=sig,
            data_slot="command-empty",
            style="display:none",
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
                cls="text-muted-foreground px-2 py-1.5 text-xs font-medium select-none",
                aria_hidden="true",
            ) if heading else None,
            *[c(sig=sig, **ctx) if callable(c) else c for c in children],
            role="group",
            data_command_group=sig,
            data_slot="command-group",
            cls=cn(
                "overflow-hidden p-1 text-foreground",
                "[&_[data-slot='command-group-heading']]:text-muted-foreground [&_[data-slot='command-group-heading']]:px-2 [&_[data-slot='command-group-heading']]:py-1.5 [&_[data-slot='command-group-heading']]:text-xs [&_[data-slot='command-group-heading']]:font-medium [&_[data-slot='command-group-heading']]:select-none",
                "[&:not(:has([data-command-item]:not([style*='none'])))]:hidden",
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
    def _(*, sig, search, selected, _item_index, dialog_ref, **_):
        index = next(_item_index)

        item_show = show if show is not None or disabled else (
            ~search | expr(value).lower().contains(search.lower()) | expr(keywords or "").lower().contains(search.lower())
        )

        user_click = kwargs.pop('data_on_click', None)
        if user_click and not isinstance(user_click, list):
            user_click = [user_click]

        click_actions = (
            ([js(onclick)] if onclick else []) +
            (user_click or []) +
            ([dialog_ref.close()] if dialog_ref else [])
        )

        return Div(
            *children,
            data_on_click=click_actions if (click_actions and not disabled) else None,
            data_on_mouseenter=selected.set(index) if not disabled else None,
            data_show=item_show,
            data_attr_data_selected=selected.eq(index).if_("true", "false"),
            data_attr_aria_selected=selected.eq(index),
            role="option",
            aria_disabled="true" if disabled else "false",
            data_command_item=sig,
            data_slot="command-item",
            data_value=value,
            data_keywords=keywords or "",
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
        cls=cn(
            "-mx-1 h-px bg-border",
            "[&:not(:has(+_[role=group]))]:hidden",
            "[&:has(+_[role=group]:not(:has([data-command-item]:not([style*='none']))))]:hidden",
            cls
        ),
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
        cls=cn("ml-auto text-xs tracking-widest text-muted-foreground", cls),
        **kwargs,
    )
