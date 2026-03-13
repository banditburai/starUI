from itertools import count

from starhtml import FT, Div, Icon, Input, Signal, Span, Style, expr, js
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml.datastar import evt

from .utils import cn, gen_id, inject_context, merge_actions, with_signals

__metadata__ = {
    "description": "Searchable dropdown selection",
    "handlers": ["position"],
}

_POPOVER_ANIMATE = """\
[data-popover-animate]{--_dur-in:150ms;--_dur-out:100ms;transform-origin:var(--popover-origin,center);transition:opacity var(--_dur-out) ease,scale var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete}
[data-popover-animate]:popover-open{transition-duration:var(--_dur-in);transition-timing-function:cubic-bezier(0.16,1,0.3,1)}
[data-popover-animate]:not(:popover-open){opacity:0;scale:0.95}
[data-popover-animate]:popover-open{@starting-style{opacity:0;scale:0.95}}
@media(prefers-reduced-motion:reduce){[data-popover-animate]{transition-duration:0ms!important}}"""

_CHIP_X_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>'


def _js_esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def _get_combobox_handler(
    sig, search, visible_items, highlighted, *, multiple=False, selected=None, selected_label=None
) -> str:
    tab = (
        "case'Tab':if(isOpen)pop.hidePopover();break;"
        if multiple
        else "case'Tab':if(isOpen){{if(ci>=0&&vi[ci])clk();else pop.hidePopover()}};break;"
    )
    backspace = (
        f"case'Backspace':if(inp?.value===''&&{selected}.length>0){{evt.preventDefault();{selected}={selected}.slice(0,-1);{selected_label}={selected_label}.slice(0,-1)}};break;"
        if multiple
        else ""
    )
    return f"""\
if(evt.isComposing||evt.keyCode===229)return;
const inp=document.getElementById('{sig}_input');
const pop=document.getElementById('{sig}_content');
const isOpen=pop&&pop.matches(':popover-open');
const vi={visible_items}||[];
const ci=vi.findIndex(x=>x.index==={highlighted});
const hi=idx=>{{if(idx<0)return;{highlighted}=idx;inp?.setAttribute('aria-activedescendant','{sig}_opt_'+idx);document.getElementById('{sig}_opt_'+idx)?.scrollIntoView({{block:'nearest'}})}};
const openPop=()=>{{if(pop&&!isOpen)pop.showPopover()}};
const clk=()=>document.getElementById('{sig}_opt_'+vi[ci]?.index)?.click();
const move=(fi,ni)=>{{evt.preventDefault();if(!isOpen){{openPop();if(vi.length>0)hi(vi[fi].index)}}else if(vi.length>0)hi(vi[ni].index)}};
switch(evt.key){{
case'ArrowDown':move(0,ci<vi.length-1?ci+1:0);break;
case'ArrowUp':move(vi.length-1,ci>0?ci-1:vi.length-1);break;
case'Enter':evt.preventDefault();if(isOpen&&ci>=0&&vi[ci])clk();break;
case'Escape':if(isOpen){{evt.preventDefault();pop.hidePopover()}}else if(inp?.value){{evt.preventDefault();inp.value='';{search}=''}};break;
{tab}
case'Home':if(isOpen&&vi.length>0){{evt.preventDefault();hi(vi[0].index)}};break;
case'End':if(isOpen&&vi.length>0){{evt.preventDefault();hi(vi[vi.length-1].index)}};break;
{backspace}default:if(evt.key.length===1&&!evt.ctrlKey&&!evt.metaKey&&!evt.altKey){{openPop();inp?.removeAttribute('aria-activedescendant');{highlighted}=-1}};break;
}}"""


def _chip_effect(sig, selected, selected_label) -> str:
    return f"""\
const c=document.getElementById('{sig}_chips');if(!c)return;
const vs={selected}||[],ls={selected_label}||[];let h='';
vs.forEach((v,i)=>{{const l=ls[i]||v;const ev=v.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');const el=l.replace(/&/g,'&amp;').replace(/</g,'&lt;');
h+='<span class="inline-flex items-center gap-0.5 rounded-md bg-secondary text-secondary-foreground pl-2 pr-1 py-0.5 text-xs font-medium" data-slot="combobox-chip"><span class="truncate max-w-[150px]">'+el+'</span><button type="button" class="ml-0.5 rounded-sm hover:bg-secondary-foreground/20 inline-flex items-center justify-center size-3.5 shrink-0 cursor-pointer" data-chip-remove data-chip-value="'+ev+'" aria-label="Remove '+el+'">{_CHIP_X_SVG}</button></span>'}});
c.innerHTML=h"""


def _chip_click_handler(sig, selected, selected_label) -> str:
    return f"""\
const btn=evt.target.closest('[data-chip-remove]');
if(btn){{evt.stopPropagation();evt.preventDefault();const v=btn.dataset.chipValue,idx={selected}.indexOf(v);if(idx>=0){{{selected}={selected}.filter((_,i)=>i!==idx);{selected_label}={selected_label}.filter((_,i)=>i!==idx)}};return}}
if(evt.target.closest('input,button'))return;
document.getElementById('{sig}_input')?.focus();const pop=document.getElementById('{sig}_content');if(pop&&!pop.matches(':popover-open'))pop.showPopover()"""


def _trigger_button(icon: str, **kwargs) -> FT:
    return HTMLButton(
        Icon(icon, cls="size-4 shrink-0 text-muted-foreground"),
        type="button",
        tabindex="-1",
        cls="flex items-center justify-center px-2",
        **kwargs,
    )


def _process_combobox_option(opt) -> FT:
    match opt:
        case str():
            return ComboboxItem(opt)
        case (value, label):
            return ComboboxItem(label, value=value)
        case {"group": group_label, "items": group_items}:
            return ComboboxGroup(
                *[ComboboxItem(label, value=value) for value, label in map(_get_value_label, group_items)],
                heading=group_label,
            )


def Combobox(
    *children,
    value: str | list[str] | None = None,
    label: str | list[str] | None = None,
    multiple: bool = False,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("combobox")
    init_val = (value if isinstance(value, list) else ([value] if value else [])) if multiple else (value or "")
    init_lbl = (label if isinstance(label, list) else ([label] if label else [])) if multiple else (label or "")
    selected = Signal(f"{sig}_value", init_val)
    selected_label = Signal(f"{sig}_label", init_lbl)
    open_state = Signal(f"{sig}_open", False)
    search = Signal(f"{sig}_search", "")
    highlighted = Signal(f"{sig}_highlighted", -1)
    visible_items = Signal(f"{sig}_visible_items", [])
    content_ref = Signal(f"{sig}_content", _ref_only=True)

    ctx = {
        "sig": sig,
        "selected": selected,
        "selected_label": selected_label,
        "open_state": open_state,
        "search": search,
        "highlighted": highlighted,
        "visible_items": visible_items,
        "content_ref": content_ref,
        "multiple": multiple,
        "_item_index": count(),
    }

    return with_signals(
        Div(
            Style(_POPOVER_ANIMATE),
            selected,
            selected_label,
            open_state,
            search,
            highlighted,
            visible_items,
            Div(id=f"{sig}_sr", role="status", aria_live="polite", aria_atomic="true", cls="sr-only"),
            *[inject_context(child, **ctx) for child in children],
            cls=cn("relative", cls),
            data_slot="combobox",
            **kwargs,
        ),
        selected=selected,
        selected_label=selected_label,
    )


def ComboboxTrigger(
    *children,
    placeholder: str = "Search...",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(
        *, sig, selected, selected_label, open_state, search, highlighted, visible_items, content_ref, multiple, **ctx
    ):
        input_ref = Signal(f"{sig}_input", _ref_only=True)
        is_disabled = kwargs.pop("disabled", None)

        ctx = dict(
            sig=sig,
            selected=selected,
            selected_label=selected_label,
            open_state=open_state,
            search=search,
            highlighted=highlighted,
            visible_items=visible_items,
            content_ref=content_ref,
            multiple=multiple,
            **ctx,
        )

        input_attrs = dict(data_attr_placeholder=selected.length.eq(0).if_(placeholder, "")) if multiple else {}

        input_el = Input(
            data_ref=input_ref,
            data_on_input=search.set(evt.target.value),
            data_on_keydown=js(
                _get_combobox_handler(
                    sig,
                    search,
                    visible_items,
                    highlighted,
                    multiple=multiple,
                    selected=selected,
                    selected_label=selected_label,
                )
            ),
            data_on_click=content_ref.showPopover(),
            value=None if multiple else (selected_label._initial or None),
            placeholder=placeholder if not (multiple and selected._initial) else "",
            **input_attrs,
            type="text",
            role="combobox",
            aria_label=placeholder,
            aria_haspopup="listbox",
            aria_autocomplete="list",
            aria_controls=content_ref._id,
            aria_expanded="false",
            data_attr_aria_expanded=open_state.if_("true", "false"),
            autocomplete="off",
            autocorrect="off",
            spellcheck="false",
            id=input_ref._id,
            disabled=is_disabled,
            cls=cn(
                "bg-transparent text-sm outline-hidden placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
                "h-7 min-w-[50px] flex-1" if multiple else "min-w-0 flex-1 text-ellipsis",
            ),
            **kwargs,
        )

        trigger_children = [inject_context(child, **ctx) for child in children]

        if multiple:
            trigger_children += [
                Div(data_effect=js(_chip_effect(sig, selected, selected_label)), id=f"{sig}_chips", cls="contents"),
                input_el,
            ]
        else:
            trigger_children.append(input_el)
            if not is_disabled:
                trigger_children.append(
                    _trigger_button(
                        "lucide:x",
                        aria_label="Clear selection",
                        data_show=selected,
                        data_on_click=js(
                            f"evt.stopPropagation();evt.preventDefault();{selected}='';{selected_label}='';const i=document.getElementById('{sig}_input');if(i){{i.value='';i.focus()}}"
                        ),
                    )
                )
            trigger_children.append(
                _trigger_button(
                    "lucide:chevron-down",
                    aria_label="Toggle options",
                    disabled=is_disabled,
                    data_show=~selected if not is_disabled else None,
                    popovertarget=content_ref._id,
                )
            )

        return Div(
            *trigger_children,
            data_on_click=js(_chip_click_handler(sig, selected, selected_label)) if multiple else None,
            data_slot="combobox-trigger",
            data_ref=Signal(f"{sig}_trigger", _ref_only=True),
            data_disabled="" if is_disabled else None,
            id=f"{sig}_trigger",
            cls=cn(
                "flex w-full rounded-lg border border-input",
                "bg-transparent text-sm shadow-xs",
                "outline-hidden transition-[color,box-shadow]",
                "dark:bg-input/30 dark:hover:bg-input/50",
                "focus-within:border-ring focus-within:ring-[3px] focus-within:ring-ring/50",
                "aria-invalid:border-destructive aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
                "data-[disabled]:cursor-not-allowed data-[disabled]:opacity-50",
                "max-h-[120px] min-h-9 flex-wrap items-center gap-1 overflow-y-auto py-1 pr-2 pl-1.5"
                if multiple
                else "h-9 items-center py-2 pl-3",
                cls,
            ),
        )

    return _


def ComboboxContent(
    *children,
    side: str = "bottom",
    align: str = "start",
    side_offset: int = 4,
    container: str = "none",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sig, open_state, search, highlighted, selected_label, visible_items, content_ref, multiple, **ctx):
        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        toggle_handler = js(f"""\
const o=evt.newState==='open';{open_state}=o;const i=document.getElementById('{sig}_input');
if(o)requestAnimationFrame(()=>{{i?.focus();i?.select()}});
else{{{search}='';{highlighted}=-1;if(i){{{"i.value=''" if multiple else f"i.value={selected_label}||''"};i.removeAttribute('aria-activedescendant')}}}}""")

        scan_effect = js(f"""\
{search};requestAnimationFrame(()=>{{
const items=[...document.querySelectorAll('[data-combobox-item="{sig}"]')];
const v=items.filter(el=>!el.style.display.includes('none')&&el.dataset.disabled!=='true');
{visible_items}=v.map(el=>({{index:parseInt(el.dataset.index||'0')}}));
if(v.length>0&&{highlighted}===-1){highlighted}=parseInt(v[0].dataset.index||'0');
const sr=document.getElementById('{sig}_sr');
if(sr&&document.getElementById('{sig}_content')?.matches(':popover-open'))sr.textContent=`${{v.length}} option${{v.length!==1?'s':''}} available`}})""")

        ctx = dict(
            sig=sig,
            open_state=open_state,
            search=search,
            highlighted=highlighted,
            selected_label=selected_label,
            visible_items=visible_items,
            content_ref=content_ref,
            multiple=multiple,
            **ctx,
        )

        return Div(
            Div(
                *[inject_context(child, **ctx) for child in children],
                data_effect=scan_effect,
                cls="p-1",
            ),
            data_ref=content_ref,
            data_on_toggle=toggle_handler,
            data_style_min_width=trigger_ref.if_(trigger_ref.offsetWidth + "px", "8rem"),
            data_position=(
                trigger_ref._id,
                {
                    "placement": placement,
                    "offset": side_offset,
                    "flip": True,
                    "shift": True,
                    "hide": True,
                    "container": container,
                },
            ),
            popover="auto",
            data_popover_animate="",
            id=content_ref._id,
            role="listbox",
            aria_labelledby=f"{sig}_trigger",
            tabindex="-1",
            aria_multiselectable="true" if multiple else None,
            cls=cn(
                "z-50 max-h-[300px] min-w-[8rem] overflow-x-hidden overflow-y-auto rounded-md border bg-popover text-popover-foreground shadow-md",
                cls,
            ),
            data_slot="combobox-content",
            **kwargs,
        )

    return _


def ComboboxItem(
    *children,
    value: str = "",
    disabled: bool = False,
    keywords: str | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sig, search, selected, highlighted, selected_label, content_ref, multiple, _item_index, **_):
        index = next(_item_index)

        first_text = next((c for c in children if isinstance(c, str)), "")
        item_value = value or first_text
        label_text = first_text or item_value
        is_selected = selected.contains(item_value) if multiple else selected.eq(item_value)

        item_show = (
            None
            if disabled
            else (
                ~search
                | expr(item_value).lower().contains(search.lower())
                | expr(label_text).lower().contains(search.lower())
                | expr(keywords or "").lower().contains(search.lower())
            )
        )

        if multiple and not disabled:
            ev, el = _js_esc(item_value), _js_esc(label_text)
            after = [
                js(
                    f"const v='{ev}',l='{el}',idx={selected}.indexOf(v);"
                    f"{selected}=idx>=0?{selected}.filter((_,i)=>i!==idx):[...{selected},v];"
                    f"{selected_label}=idx>=0?{selected_label}.filter((_,i)=>i!==idx):[...{selected_label},l];"
                    f"{search}='';document.getElementById('{sig}_input').value=''"
                )
            ]
        else:
            after = [selected.set(item_value), selected_label.set(label_text), content_ref.hidePopover()]
        click_actions = merge_actions(kwargs=kwargs, after=after)

        return Div(
            *children,
            Span(
                Icon("lucide:check", cls="size-4"),
                style="opacity: 0; transition: opacity 0.15s",
                data_style_opacity=is_selected.if_("1", "0"),
                cls="pointer-events-none absolute right-2 flex size-4 items-center justify-center",
                data_slot="combobox-item-indicator",
            ),
            data_on_click=click_actions if not disabled else None,
            data_on_mouseenter=highlighted.set(index) if not disabled else None,
            data_show=item_show,
            data_attr_data_highlighted=highlighted.eq(index).if_("true", "false") if not disabled else None,
            role="option",
            aria_disabled="true" if disabled else "false",
            data_attr_aria_selected=is_selected,
            data_disabled="true" if disabled else None,
            data_combobox_item=sig,
            data_slot="combobox-item",
            data_value=item_value,
            data_index=str(index),
            id=f"{sig}_opt_{index}",
            cls=cn(
                "relative flex w-full cursor-default items-center gap-2 rounded-sm py-1.5 pr-8 pl-2 text-sm outline-hidden select-none",
                "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:shrink-0 [&_[data-icon-sh]:not([class*='size-'])]:size-4 [&_[data-icon-sh]:not([class*='text-'])]:text-muted-foreground",
                "data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50",
                "data-[highlighted=true]:bg-accent data-[highlighted=true]:text-accent-foreground"
                if not disabled
                else "",
                cls,
            ),
            **kwargs,
        )

    return _


def ComboboxEmpty(*children, cls: str = "", **kwargs) -> FT:
    def _(*, visible_items, **_):
        return Div(
            *(children or ["No results found."]),
            data_show=visible_items.length.eq(0),
            data_slot="combobox-empty",
            cls=cn("py-6 text-center text-sm text-muted-foreground", cls),
            **kwargs,
        )

    return _


def ComboboxGroup(
    *children,
    heading: str | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    if not heading and children and isinstance(children[0], str):
        heading, children = children[0], children[1:]

    def _(*, sig, **ctx):
        return Div(
            Div(
                heading,
                data_slot="combobox-group-heading",
                cls="px-2 py-1.5 text-xs font-medium text-muted-foreground select-none",
                aria_hidden="true",
            )
            if heading
            else None,
            *[inject_context(c, sig=sig, **ctx) for c in children],
            role="group",
            data_slot="combobox-group",
            cls=cn(
                "overflow-hidden p-1 text-foreground",
                "[&:not(:has([data-combobox-item]:not([style*='none'])))]:hidden",
                cls,
            ),
            **kwargs,
        )

    return _


def ComboboxSeparator(cls: str = "", **kwargs) -> FT:
    return Div(
        cls=cn(
            "-mx-1 my-1 h-px bg-border",
            "[&:not(:has(+_[role=group]))]:hidden",
            "[&:has(+_[role=group]:not(:has([data-combobox-item]:not([style*='none']))))]:hidden",
            cls,
        ),
        data_slot="combobox-separator",
        **kwargs,
    )


def _get_value_label(item: str | tuple) -> tuple[str, str]:
    return (item, item) if isinstance(item, str) else (item[0], item[1]) if isinstance(item, tuple) else ("", "")


def _find_initial_label(options: list, value) -> str | list[str]:
    if not value:
        return [] if isinstance(value, list) else ""
    all_items = (item for opt in options for item in (opt.get("items", []) if isinstance(opt, dict) else [opt]))
    lookup = dict(map(_get_value_label, all_items))
    return [lookup.get(v, v) for v in value] if isinstance(value, list) else lookup.get(value, "")


def ComboboxWithLabel(
    *attrs,
    label: str,
    options: list[str | tuple[str, str] | dict],
    value: str | list[str] | None = None,
    placeholder: str = "Search...",
    multiple: bool = False,
    signal: str | Signal = "",
    helper_text: str = "",
    error_text: str = "",
    required: bool = False,
    disabled: bool = False,
    side: str = "bottom",
    label_cls: str = "",
    trigger_cls: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("combobox")

    return Div(
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else None,
            fr=f"{sig}_input",
            cls=cn("mb-1.5 block text-sm font-medium", label_cls),
        ),
        Combobox(
            ComboboxTrigger(
                placeholder=placeholder,
                cls=trigger_cls,
                disabled=disabled or None,
                aria_invalid="true" if error_text else None,
            ),
            ComboboxContent(
                ComboboxEmpty(),
                *[_process_combobox_option(opt) for opt in options],
                side=side,
            ),
            *attrs,
            value=value,
            label=_find_initial_label(options, value),
            multiple=multiple,
            signal=sig,
            cls="w-full",
            **kwargs,
        ),
        HTMLP(error_text, cls="mt-1.5 text-sm text-destructive") if error_text else None,
        HTMLP(helper_text, cls="mt-1.5 text-sm text-muted-foreground") if helper_text and not error_text else None,
        data_slot="combobox-with-label",
        cls=cn("space-y-1.5", cls),
    )
