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
    value,
)

from .button import Button
from .calendar import Calendar, CalendarMode
from .input import Input
from .popover import Popover, PopoverContent, PopoverTrigger
from .utils import cn

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _close_popover_js(signal: str) -> str:
    return f"const t=document.querySelector('[data-picker-trigger=\"{signal}\"][popovertarget]');if(t){{const p=t.getAttribute('popovertarget');const c=document.getElementById(p);if(c?.matches(':popover-open')){{c.hidePopover()}}}}"


def _get_display_text(signal: str, mode: CalendarMode, placeholder: str) -> str:
    if mode == "single":
        return f"${signal}_selected?(()=>{{const[y,m,d]=${signal}_selected.split('-').map(Number);return new Date(y,m-1,d).toLocaleDateString('en-US',{{year:'numeric',month:'long',day:'numeric'}})}})():'{placeholder}'"

    parse_array = f"(JSON.parse(${signal}_selected||'[]')??[])"
    if mode == "multiple":
        return f"(()=>{{const a={parse_array};return a.length?`${{a.length}} date${{a.length>1?'s':''}} selected`:'{placeholder}'}})()"

    format_short = (
        "toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})"
    )
    return f"(()=>{{const a={parse_array};return a.length===2?(()=>{{const[y1,m1,d1]=a[0].split('-').map(Number);const[y2,m2,d2]=a[1].split('-').map(Number);return new Date(y1,m1-1,d1).{format_short}+' - '+new Date(y2,m2-1,d2).{format_short}}})():a.length===1?(()=>{{const[y,m,d]=a[0].split('-').map(Number);return new Date(y,m-1,d).{format_short}}})():'{placeholder}'}})()"


def _get_empty_check(signal: str, mode: CalendarMode) -> str:
    return (
        f"!${signal}_selected"
        if mode == "single"
        else f"!(JSON.parse(${signal}_selected||'[]')??[]).length"
    )


def _create_trigger(
    signal: str,
    icon: str,
    display_text: str,
    empty_check: str,
    width: str,
    disabled: bool,
    variant: str = "outline",
) -> PopoverTrigger:
    return PopoverTrigger(
        Span(
            Icon(icon, cls="mr-2 h-4 w-4"),
            Span(ds_text(display_text), cls="text-left"),
            ds_class(**{"text-muted-foreground": empty_check}),
            cls="flex items-center",
        ),
        variant=variant,
        cls=cn(width, "justify-start text-left font-normal"),
        disabled=disabled,
        **{"data-picker-trigger": signal},
    )


def _create_base_picker(
    signal: str,
    calendar_signal: str,
    initial_selected: str | list,
    mode: CalendarMode,
    placeholder: str,
    disabled: bool,
    width: str,
    *,
    icon: str = "lucide:calendar",
    calendar_cls: str = "border-0 rounded-none",
    extra_content: list | None = None,
    presets: list[tuple[str, str]] | None = None,
) -> tuple[Popover, dict]:
    display_text = _get_display_text(signal, mode, placeholder)
    empty_check = _get_empty_check(signal, mode)
    close_js = _close_popover_js(signal)

    on_select = (
        (
            f"${signal}_selected=${calendar_signal}_selected;{close_js}"
            if mode in ("single", "range")
            else f"${signal}_selected=${calendar_signal}_selected"
        )
        if not disabled
        else None
    )

    calendar = Calendar(
        signal=calendar_signal,
        mode=mode,
        selected=initial_selected
        if not presets or isinstance(initial_selected, str)
        else "",
        disabled=disabled,
        on_select=on_select,
        cls=calendar_cls,
    )

    content, popover_cls = (
        (
            Div(
                Div(
                    *[
                        Button(
                            label,
                            ds_on_click(
                                f"${signal}_selected='{date}';${calendar_signal}_selected='{date}';{close_js}"
                            ),
                            variant="ghost",
                            size="sm",
                            cls="w-full justify-start",
                            disabled=disabled,
                        )
                        for label, date in presets
                    ],
                    cls="flex flex-col gap-1 border-r pr-2",
                ),
                calendar,
                cls="flex gap-2",
            ),
            "w-fit p-2",
        )
        if presets
        else (Div(calendar, *extra_content, cls="flex flex-col"), "w-fit p-0")
        if extra_content
        else (calendar, "w-fit p-0")
    )

    popover = Popover(
        _create_trigger(signal, icon, display_text, empty_check, width, disabled),
        PopoverContent(content, cls=popover_cls, align="start"),
    )

    signals = {
        f"{signal}_selected": value(
            json.dumps(initial_selected)
            if isinstance(initial_selected, list)
            else initial_selected
        )
    }

    return popover, signals


def DatePicker(
    *,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    placeholder: str | None = None,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    width: str = "w-[280px]",
    with_presets: bool = False,
    **attrs: Any,
) -> Div:
    signal = signal or f"date_picker_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"

    multi_modes = ("multiple", "range")

    if placeholder is None:
        placeholder = {
            "single": "Select date" if with_presets else "Pick a date",
            "range": "Select date range",
            "multiple": "Select dates",
        }[mode]
    initial_selected = (
        selected
        if (isinstance(selected, list) and mode in multi_modes)
        or (isinstance(selected, str) and mode == "single")
        else []
        if mode in multi_modes
        else ""
    )

    presets = None
    if with_presets and mode == "single":
        today = datetime.now()
        presets = [
            ("Today", today.strftime("%Y-%m-%d")),
            ("Tomorrow", (today + timedelta(days=1)).strftime("%Y-%m-%d")),
            ("In a week", (today + timedelta(days=7)).strftime("%Y-%m-%d")),
        ]

    popover, signals = _create_base_picker(
        signal,
        calendar_signal,
        initial_selected,
        mode,
        placeholder,
        disabled,
        width,
        presets=presets,
    )

    effects = []
    if mode in multi_modes:
        effects.append(_selection_sync_from_calendar(signal, calendar_signal))
    effects.append(_selection_sync_to_calendar(signal, calendar_signal))

    return Div(
        popover,
        ds_signals(**signals),
        ds_effect(";".join(effects)),
        cls=cn("inline-block", class_name, cls),
        **attrs,
    )


def DateRangePicker(**kwargs: Any) -> Div:
    """Convenience wrapper for range mode date picker."""
    return DatePicker(mode="range", **kwargs)


def DatePickerWithPresets(**kwargs: Any) -> Div:
    """Convenience wrapper for date picker with presets."""
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
    **attrs: Any,
) -> Div:
    signal = signal or f"datetime_picker_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"

    if selected and "T" in selected:
        initial_date, time_part = selected.split("T", 1)
        initial_time = time_part[:5] if time_part else "00:00"
    else:
        initial_date, initial_time = "", "00:00"

    time_section = Div(
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

    display_text = f"${signal}_selected ? (()=>{{const [y,m,d]=${signal}_selected.split('-').map(Number);return new Date(y,m-1,d).toLocaleDateString('en-US', {{year: 'numeric', month: 'long', day: 'numeric'}})}})() + ' at ' + ${signal}_time : '{placeholder}'"

    popover = Popover(
        _create_trigger(
            signal,
            "lucide:calendar-clock",
            display_text,
            f"!${signal}_selected",
            width,
            disabled,
        ),
        PopoverContent(
            Div(
                Calendar(
                    signal=calendar_signal,
                    mode="single",
                    selected=initial_date,
                    disabled=disabled,
                    cls="border-0 rounded-none",
                ),
                time_section,
                cls="flex flex-col",
            ),
            cls="w-fit p-0",
            align="start",
        ),
    )

    return Div(
        popover,
        ds_signals(
            **{
                f"{signal}_selected": value(initial_date),
                f"{signal}_time": value(initial_time),
                f"{signal}_datetime": value(selected or ""),
            }
        ),
        ds_effect(_datetime_sync_effect(signal, calendar_signal)),
        cls=cn("inline-block", class_name, cls),
        **attrs,
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
    **attrs: Any,
) -> Div:
    signal = signal or f"date_input_{uuid4().hex[:8]}"
    calendar_signal = f"{signal}_calendar"
    initial_selected = selected or ""

    return Div(
        Div(
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
                cls="",
            ),
            cls="relative inline-block",
        ),
        ds_signals(**{f"{signal}_selected": value(initial_selected)}),
        ds_effect(
            _input_sync_effect(signal, calendar_signal)
            + ";"
            + _input_close_effect(signal)
        ),
        cls=cn("inline-block", class_name, cls),
        **attrs,
    )


def _datetime_sync_effect(signal: str, calendar_signal: str) -> str:
    return f"const c=typeof ${calendar_signal}_selected!=='undefined'?${calendar_signal}_selected:'',p=typeof ${signal}_selected!=='undefined'?${signal}_selected:'';if(c!==p)${signal}_selected=c;const t=document.querySelector('[data-time-input=\"{signal}\"]');if(t){{const u=()=>{{const d=typeof ${signal}_selected!=='undefined'?${signal}_selected:'',v=t.value;if(d&&v){{${signal}_time=v;${signal}_datetime=`${{d}}T${{v}}:00`}}}};t.removeEventListener('change',u);t.addEventListener('change',u)}}"


def _input_sync_effect(signal: str, calendar_signal: str) -> str:
    month_names = str(MONTH_NAMES)
    return f"const c=typeof ${calendar_signal}_selected!=='undefined'?${calendar_signal}_selected:'',i=document.querySelector('[data-date-input=\"{signal}\"]'),ps=typeof ${signal}_selected!=='undefined'?${signal}_selected:'';if(i&&c&&c!==ps){{i.value=c;${signal}_selected=c}}if(i){{const u=()=>{{const v=i.value;if(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(v)){{${signal}_selected=v;${calendar_signal}_selected=v;const[y,m,d]=v.split('-').map(Number);${calendar_signal}_month=m;${calendar_signal}_year=y;const M={month_names};${calendar_signal}_month_display=M[m-1]}}}};i.removeEventListener('change',u);i.addEventListener('change',u)}}"


def _input_close_effect(signal: str) -> str:
    return f"const s=typeof ${signal}_selected!=='undefined'?${signal}_selected:'',p=window['_prev_{signal}_input_selected'];if(s&&s!==p){{const t=document.querySelector('[data-picker-trigger=\"{signal}\"]'),v=t?.getAttribute('popovertarget');if(v){{const c=document.getElementById(v);if(c?.matches(':popover-open')){{c.hidePopover()}}}}}}window['_prev_{signal}_input_selected']=s"


def _selection_sync_to_calendar(signal: str, calendar_signal: str) -> str:
    return f"if(typeof ${signal}_selected!=='undefined'&&typeof ${calendar_signal}_selected!=='undefined'&&!window._syncingFromCalendar_{signal}){{const p=${signal}_selected,c=${calendar_signal}_selected,r=typeof p==='string'&&(p.startsWith('[')||p==='[]');if(r){{const e=c===''||c==='[]',pe=p==='[]';if(!pe&&e){{window._syncingToCalendar_{signal}=true;${calendar_signal}_selected=p;setTimeout(()=>{{window._syncingToCalendar_{signal}=false}},0)}}}}else if(p!==c){{window._syncingToCalendar_{signal}=true;${calendar_signal}_selected=p;setTimeout(()=>{{window._syncingToCalendar_{signal}=false}},0)}}}}"


def _selection_sync_from_calendar(signal: str, calendar_signal: str) -> str:
    return f"if(typeof ${calendar_signal}_selected!=='undefined'&&typeof ${signal}_selected!=='undefined'&&!window._syncingToCalendar_{signal}){{const c=${calendar_signal}_selected,p=${signal}_selected;if(c!==p){{window._syncingFromCalendar_{signal}=true;${signal}_selected=c;setTimeout(()=>{{window._syncingFromCalendar_{signal}=false}},0)}}}}"
