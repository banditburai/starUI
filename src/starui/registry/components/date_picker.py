import json
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from starhtml import Div, Icon, Span
from starhtml.datastar import (
    ds_class,
    ds_effect,
    ds_on_click,
    ds_signals,
    ds_text,
    toggle_class,
    value,
)

from .button import Button
from .calendar import Calendar, CalendarMode
from .input import Input
from .popover import Popover, PopoverContent, PopoverTrigger
from .utils import cn

from .calendar import MONTHS as MONTH_NAMES


def DatePicker(
    *attrs,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    placeholder: str | None = None,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    width: str = "w-[280px]",
    with_presets: bool = False,
    **kwargs: Any,
) -> Div:
    signal = signal or f"date_picker_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"
    multi_modes = ("multiple", "range")
    
    placeholder = placeholder or {
        "single": "Select date" if with_presets else "Pick a date",
        "range": "Select date range",
        "multiple": "Select dates",
    }[mode]
    
    initial_selected = (
        selected if isinstance(selected, (list if mode in multi_modes else str))
        else [] if mode in multi_modes else ""
    )
    
    close_js = _close_popover_js(signal)
    calendar = Calendar(
        signal=calendar_signal,
        mode=mode,
        selected=initial_selected if not with_presets or isinstance(initial_selected, str) else "",
        disabled=disabled,
        on_select=f"${signal}_selected=${calendar_signal}_selected{';' + close_js if mode in ('single', 'range') else ''}" if not disabled else None,
        cls="border-0 rounded-none",
    )
    
    content, popover_cls = _build_picker_content(
        signal, calendar_signal, calendar, mode, with_presets, disabled, close_js
    )
    
    popover = Popover(
        _build_trigger(signal, mode, placeholder, width, disabled, "lucide:calendar"),
        PopoverContent(content, cls=popover_cls, align="start"),
    )
    
    effects = [_sync_effect(signal, calendar_signal, mode)]
    
    return Div(
        popover,
        *attrs,  # DS helpers like ds_on_change, etc.
        ds_signals(**{
            f"{signal}_selected": value(
                json.dumps(initial_selected) if isinstance(initial_selected, list) else initial_selected
            )
        }),
        ds_effect(";".join(filter(None, effects))) if any(effects) else None,
        cls=cn("inline-block", class_name, cls),
        **kwargs,
    )


def DateRangePicker(**kwargs: Any) -> Div:
    return DatePicker(mode="range", **kwargs)


def DatePickerWithPresets(**kwargs: Any) -> Div:
    return DatePicker(with_presets=True, **kwargs)


def DateTimePicker(
    *,
    signal: str | None = None,
    selected: str | None = None,
    placeholder: str = "Select date and time",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    width: str = "w-[280px]",
    **kwargs: Any,
) -> Div:
    signal = signal or f"datetime_picker_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"
    
    initial_date, initial_time = _parse_datetime(selected)
    
    content = Div(
        Calendar(
            signal=calendar_signal,
            mode="single",
            selected=initial_date,
            disabled=disabled,
            cls="border-0 rounded-none",
        ),
        _build_time_section(signal, initial_time, disabled),
        cls="flex flex-col",
    )
    
    display_text = f"${signal}_selected ? (()=>{{const [y,m,d]=${signal}_selected.split('-').map(Number);return new Date(y,m-1,d).toLocaleDateString('en-US', {{year: 'numeric', month: 'long', day: 'numeric'}})}})() + ' at ' + ${signal}_time : '{placeholder}'"
    
    popover = Popover(
        _build_trigger(signal, "single", placeholder, width, disabled, "lucide:calendar-clock", display_text),
        PopoverContent(content, cls="w-fit p-0", align="start"),
    )
    
    return Div(
        popover,
        ds_signals(**{
            f"{signal}_selected": value(initial_date),
            f"{signal}_time": value(initial_time),
            f"{signal}_datetime": value(selected or ""),
        }),
        ds_effect(_datetime_sync_effect(signal, calendar_signal)),
        cls=cn("inline-block", class_name, cls),
        **kwargs,
    )


def DatePickerWithInput(
    *,
    signal: str | None = None,
    selected: str | None = None,
    placeholder: str = "Select date",
    format: str = "YYYY-MM-DD",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    width: str = "w-[240px]",
    **kwargs: Any,
) -> Div:
    signal = signal or f"date_input_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"
    initial_selected = selected or ""
    
    input_with_popover = Div(
        Input(
            type="text",
            placeholder=format,
            value=initial_selected,
            data_date_input=signal,
            data_model=f"{signal}_selected",
            cls=cn(width, "pr-10"),
            disabled=disabled,
        ),
        Popover(
            PopoverTrigger(
                Icon("lucide:calendar", cls="h-4 w-4"),
                variant="ghost",
                size="icon",
                cls="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7 px-0 hover:bg-transparent",
                disabled=disabled,
            ),
            PopoverContent(
                Calendar(
                    signal=calendar_signal,
                    mode="single",
                    selected=initial_selected,
                    disabled=disabled,
                    cls="border-0 rounded-none",
                ),
                cls="w-fit p-0",
                align="end",
            ),
        ),
        cls="relative inline-block",
    )
    
    return Div(
        input_with_popover,
        ds_signals(**{f"{signal}_selected": value(initial_selected)}),
        ds_effect(f"{_input_sync_effect(signal, calendar_signal)};{_input_close_effect(signal)}"),
        cls=cn("inline-block", class_name, cls),
        **kwargs,
    )


def _build_trigger(signal: str, mode: CalendarMode, placeholder: str, width: str, disabled: bool, icon: str, custom_display: str = None) -> PopoverTrigger:
    display_text = custom_display or _get_display_text(signal, mode, placeholder)
    empty_check = f"!${signal}_selected" if mode == "single" else f"!(JSON.parse(${signal}_selected||'[]')??[]).length"
    
    return PopoverTrigger(
        Span(
            Icon(icon, cls="mr-2 h-4 w-4"),
            Span(ds_text(display_text), cls="text-left"),
            toggle_class(empty_check, "text-muted-foreground", ""),
            cls="flex items-center",
        ),
        variant="outline",
        cls=cn(width, "justify-start text-left font-normal"),
        disabled=disabled,
        **{"data-picker-trigger": signal},
    )


def _build_picker_content(signal: str, calendar_signal: str, calendar: Calendar, mode: CalendarMode, with_presets: bool, disabled: bool, close_js: str) -> tuple[Div, str]:
    if not with_presets or mode != "single":
        return calendar, "w-fit p-0"
    
    today = datetime.now()
    presets = [
        ("Today", today.strftime("%Y-%m-%d")),
        ("Tomorrow", (today + timedelta(days=1)).strftime("%Y-%m-%d")),
        ("In a week", (today + timedelta(days=7)).strftime("%Y-%m-%d")),
    ]
    
    preset_buttons = Div(
        *[
            Button(
                label,
                ds_on_click(f"${signal}_selected='{date}';${calendar_signal}_selected='{date}';{close_js}"),
                variant="ghost",
                size="sm",
                cls="w-full justify-start",
                disabled=disabled,
            )
            for label, date in presets
        ],
        cls="flex flex-col gap-1 border-r pr-2",
    )
    
    return Div(preset_buttons, calendar, cls="flex gap-2"), "w-fit p-2"


def _build_time_section(signal: str, initial_time: str, disabled: bool) -> Div:
    return Div(
        Div(
            Span("Time", cls="text-sm font-medium"),
            Input(
                type="time",
                value=initial_time,
                data_time_input=signal,
                data_model=f"{signal}_time",
                cls="w-full",
                disabled=disabled,
            ),
            cls="space-y-2",
        ),
        cls="p-3 border-t",
    )


def _parse_datetime(selected: str | None) -> tuple[str, str]:
    if selected and "T" in selected:
        parts = selected.split("T", 1)
        return parts[0], parts[1][:5] if len(parts) > 1 else "00:00"
    return "", "00:00"


def _sync_effect(signal: str, calendar_signal: str, mode: CalendarMode) -> str:
    if mode not in ("multiple", "range"):
        return ""
    
    sync_from = f"if(typeof ${calendar_signal}_selected!=='undefined'&&typeof ${signal}_selected!=='undefined'&&!window._syncingToCalendar_{signal}){{const c=${calendar_signal}_selected,p=${signal}_selected;if(c!==p){{window._syncingFromCalendar_{signal}=true;${signal}_selected=c;setTimeout(()=>{{window._syncingFromCalendar_{signal}=false}},0)}}}}"
    sync_to = f"if(typeof ${signal}_selected!=='undefined'&&typeof ${calendar_signal}_selected!=='undefined'&&!window._syncingFromCalendar_{signal}){{const p=${signal}_selected,c=${calendar_signal}_selected,r=typeof p==='string'&&(p.startsWith('[')||p==='[]');if(r){{const e=c===''||c==='[]',pe=p==='[]';if(!pe&&e){{window._syncingToCalendar_{signal}=true;${calendar_signal}_selected=p;setTimeout(()=>{{window._syncingToCalendar_{signal}=false}},0)}}}}else if(p!==c){{window._syncingToCalendar_{signal}=true;${calendar_signal}_selected=p;setTimeout(()=>{{window._syncingToCalendar_{signal}=false}},0)}}}}"
    
    return f"{sync_from};{sync_to}"


def _close_popover_js(signal: str) -> str:
    return f"const t=document.querySelector('[data-picker-trigger=\"{signal}\"][popovertarget]');if(t){{const p=t.getAttribute('popovertarget');const c=document.getElementById(p);if(c?.matches(':popover-open')){{c.hidePopover()}}}}"


def _get_display_text(signal: str, mode: CalendarMode, placeholder: str) -> str:
    match mode:
        case "single":
            return f"${signal}_selected?(()=>{{const[y,m,d]=${signal}_selected.split('-').map(Number);return new Date(y,m-1,d).toLocaleDateString('en-US',{{year:'numeric',month:'long',day:'numeric'}})}})():'{placeholder}'"
        case "multiple":
            return f"(()=>{{const a=(JSON.parse(${signal}_selected||'[]')??[]);return a.length?`${{a.length}} date${{a.length>1?'s':''}} selected`:'{placeholder}'}})()"
        case "range":
            fmt = "toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})"
            return f"(()=>{{const a=(JSON.parse(${signal}_selected||'[]')??[]);return a.length===2?(()=>{{const[y1,m1,d1]=a[0].split('-').map(Number);const[y2,m2,d2]=a[1].split('-').map(Number);return new Date(y1,m1-1,d1).{fmt}+' - '+new Date(y2,m2-1,d2).{fmt}}})():a.length===1?(()=>{{const[y,m,d]=a[0].split('-').map(Number);return new Date(y,m-1,d).{fmt}}})():'{placeholder}'}})()"


def _datetime_sync_effect(signal: str, calendar_signal: str) -> str:
    return f"const c=typeof ${calendar_signal}_selected!=='undefined'?${calendar_signal}_selected:'',p=typeof ${signal}_selected!=='undefined'?${signal}_selected:'';if(c!==p)${signal}_selected=c;const t=document.querySelector('[data-time-input=\"{signal}\"]');if(t){{const u=()=>{{const d=typeof ${signal}_selected!=='undefined'?${signal}_selected:'',v=t.value;if(d&&v){{${signal}_time=v;${signal}_datetime=`${{d}}T${{v}}:00`}}}};t.removeEventListener('change',u);t.addEventListener('change',u)}}"


def _input_sync_effect(signal: str, calendar_signal: str) -> str:
    month_names = str(MONTH_NAMES)
    return f"const c=typeof ${calendar_signal}_selected!=='undefined'?${calendar_signal}_selected:'',i=document.querySelector('[data-date-input=\"{signal}\"]'),ps=typeof ${signal}_selected!=='undefined'?${signal}_selected:'';if(i&&c&&c!==ps){{i.value=c;${signal}_selected=c}}if(i){{const u=()=>{{const v=i.value;if(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(v)){{${signal}_selected=v;${calendar_signal}_selected=v;const[y,m,d]=v.split('-').map(Number);${calendar_signal}_month=m;${calendar_signal}_year=y;const M={month_names};${calendar_signal}_month_display=M[m-1]}}}};i.removeEventListener('change',u);i.addEventListener('change',u)}}"


def _input_close_effect(signal: str) -> str:
    return f"const s=typeof ${signal}_selected!=='undefined'?${signal}_selected:'',p=window['_prev_{signal}_input_selected'];if(s&&s!==p){{const t=document.querySelector('[data-picker-trigger=\"{signal}\"]'),v=t?.getAttribute('popovertarget');if(v){{const c=document.getElementById(v);if(c?.matches(':popover-open')){{c.hidePopover()}}}}}}window['_prev_{signal}_input_selected']=s"