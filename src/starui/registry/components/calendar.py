import json
from datetime import datetime
from typing import Any, Literal

from starhtml import Button as HTMLButton
from starhtml import Div, Icon, Span, Style, Signal, js

from .button import Button
from .utils import cn, ensure_signal

CalendarMode = Literal["single", "range", "multiple"]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def Calendar(
    *attrs,
    signal: str = "",
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    month: int | None = None,
    year: int | None = None,
    disabled: bool = False,
    on_select: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> Div:
    sig_name = ensure_signal(signal, "calendar")
    today = datetime.now()
    current_month = month or today.month
    current_year = year or today.year
    today_str = today.strftime("%Y-%m-%d")

    if mode == "single":
        initial_selected = selected if isinstance(selected, str) else ""
    else:
        initial_selected = selected if isinstance(selected, list) else []

    return Div(
        Style(_CALENDAR_STYLES),
        Signal(sig_name + "_month", current_month),
        Signal(sig_name + "_year", current_year),
        Signal(sig_name + "_month_display", MONTHS[current_month - 1]),
        Signal(sig_name + "_selected", initial_selected),
        _build_navigation(sig_name, current_month, current_year, disabled),
        Div(
            _build_weekdays(),
            _build_calendar_grid(sig_name, mode, disabled, today_str, on_select),
            cls="w-full"
        ),
        *attrs,
        data_calendar=sig_name,
        role="application",
        aria_label="Calendar",
        cls=cn("p-3 border rounded-md w-fit", cls),
        **kwargs,
    )


def _build_navigation(signal: str, month: int, year: int, disabled: bool) -> Div:
    def nav_button(is_next: bool):
        direction = "right" if is_next else "left"
        label = "Next month" if is_next else "Previous month"
        return Button(
            Icon(f"lucide:chevron-{direction}", cls="h-4 w-4"),
            data_on_click=js(_nav_handler(signal, is_next)) if not disabled else None,
            variant="outline",
            size="icon",
            disabled=disabled,
            aria_label=label,
            cls=f"h-7 w-7 absolute {direction}-0",
        )

    return Div(
        nav_button(False),
        Div(
            _build_dropdown(signal, "month", MONTHS[month - 1],
                          [(i+1, name) for i, name in enumerate(MONTHS)], disabled),
            _build_dropdown(signal, "year", year,
                          [(y, y) for y in range(year - 10, year + 11)], disabled),
            cls="flex items-center gap-1",
        ),
        nav_button(True),
        cls="relative flex items-center justify-center mb-4",
        role="group",
        aria_label="Calendar navigation",
    )


def _build_dropdown(signal: str, type: str, current_display: str | int, items: list[tuple], disabled: bool) -> Div:
    type_sig = Signal(f"{signal}_{type}", _ref_only=True)
    trigger_ref = f"{signal}_{type}_trigger"
    content_ref = f"{signal}_{type}_content"
    display_sig = Signal(f"{signal}_{type}_display", _ref_only=True) if type == "month" else type_sig

    trigger = HTMLButton(
        Span(
            data_text=display_sig,
            cls="pointer-events-none"
        ),
        Icon("lucide:chevron-down", cls="h-3 w-3 shrink-0 opacity-50 ml-1"),
        data_ref=trigger_ref,
        id=trigger_ref,
        popovertarget=content_ref,
        popoveraction="toggle",
        type="button",
        disabled=disabled,
        aria_label="Select " + type,
        aria_haspopup="listbox",
        cls="flex h-7 items-center gap-1 rounded-md px-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground focus:outline-none disabled:opacity-50",
    )

    item_cls = cn(
        "px-2 py-1 text-sm rounded cursor-pointer hover:bg-accent hover:text-accent-foreground",
        "data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground",
    )

    def make_item(value, display):
        attrs = dict(
            cls=item_cls,
            data_selected=type_sig == value,
            role="option",
        )
        if type == "month":
            attrs["data_month"] = value
            attrs["data_month_name"] = display
        else:
            attrs["data_year"] = value
        return Div(str(display), **attrs)

    dropdown = Div(
        *[make_item(value, display) for value, display in items],
        data_on_click=js(_dropdown_handler(signal, type, content_ref)) if not disabled else None,
        data_ref=content_ref,
        data_style_min_width=f"${trigger_ref} ? ${trigger_ref}.offsetWidth + 'px' : '8rem'",
        data_position_anchor=trigger_ref,
        data_position_placement="bottom",
        data_position_offset="8",
        data_position_flip="true",
        data_position_shift="true",
        data_position_hide="true",
        data_position_container="none",
        popover="auto",
        id=content_ref,
        role="listbox",
        aria_label=type.capitalize() + " selection",
        cls="z-50 max-h-[200px] overflow-y-auto scrollbar-hide rounded-md border bg-popover text-popover-foreground shadow-md outline-none dark:border",
    )

    return Div(trigger, dropdown, cls="relative")


def _build_weekdays() -> Div:
    weekdays = ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
    full_weekdays = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    return Div(
        *[
            Div(
                day,
                cls="h-9 w-9 text-[0.8rem] font-normal text-muted-foreground text-center",
                role="columnheader",
                aria_label=full_weekdays[i]
            )
            for i, day in enumerate(weekdays)
        ],
        cls="grid grid-cols-7 border-b mb-1",
        role="row",
    )


def _build_calendar_grid(signal: str, mode: CalendarMode, disabled: bool, today_str: str, on_select: str | None) -> Div:
    return Div(
        data_effect=js(_render_days_effect(signal, mode, disabled, today_str)),
        data_on_click=js(_day_select_handler(signal, mode, on_select)) if not disabled else None,
        cls="cal-body grid grid-cols-7 gap-0",
        data_calendar_body=signal,
        role="grid",
        aria_label="Calendar days",
    )


def _nav_handler(signal: str, is_next: bool) -> str:
    op = "+" if is_next else "-"
    months_str = str(MONTHS)
    return f"let mm=parseInt(${signal}_month){op}1,y=parseInt(${signal}_year);if(mm>12){{mm=1;y++}}else if(mm<1){{mm=12;y--}};${signal}_month=mm;${signal}_year=y;const months={months_str};${signal}_month_display=months[mm-1]"


def _dropdown_handler(signal: str, type: str, content_id: str) -> str:
    if type == "month":
        return f"const t=evt.target;if(!t.dataset.month)return;const m=parseInt(t.dataset.month),n=t.dataset.monthName;${signal}_month=m;${signal}_month_display=n;document.getElementById('{content_id}').hidePopover()"
    return f"const t=evt.target;if(!t.dataset.year)return;const y=parseInt(t.dataset.year);${signal}_year=y;document.getElementById('{content_id}').hidePopover()"


def _day_select_handler(signal: str, mode: CalendarMode, on_select: str | None = None) -> str:
    parts = ["const c=evt.target.closest('.cal-cell');if(!c||c.classList.contains('empty'))return;const d=c.dataset.date;if(!d)return"]

    match mode:
        case "single":
            parts.append(f"${signal}_selected=${signal}_selected===d?'':d")
            if on_select:
                parts.append(f"if(${signal}_selected){{{on_select}}}")
        case "multiple":
            parts.append(f"let s=${signal}_selected||[]")
            parts.append(f"const i=s.indexOf(d);${signal}_selected=i>=0?s.filter((_,x)=>x!==i):[...s,d]")
            if on_select:
                parts.append(on_select)
        case "range":
            parts.append(f"let s=${signal}_selected||[]")
            parts.append(f"if(s.length===0){{${signal}_selected=[d]}}else if(s.length===1){{if(s[0]===d){{${signal}_selected=[]}}else{{${signal}_selected=[s[0],d].sort()}}}}else{{${signal}_selected=[d]}}")
            if on_select:
                parts.append(f"if(${signal}_selected.length===2){{{on_select}}}")

    return ";".join(parts)


def _render_days_effect(signal: str, mode: CalendarMode, disabled: bool, today_str: str) -> str:
    gen_cal = "const f=new Date(y,mm-1,1),days=new Date(y,mm,0).getDate(),o=f.getDay(),a=[];for(let i=0;i<42;i++){const n=i-o+1,v=i>=o&&n<=days;a.push({day:v?n.toString():'',date:v?`${y}-${mm.toString().padStart(2,'0')}-${n.toString().padStart(2,'0')}`:'',empty:!v})}"
    
    sel_check = {
        "single": "s===c.date",
        "multiple": "s.includes(c.date)",
        "range": "s.length===1?c.date===s[0]:s.length===2?c.date>=s[0]&&c.date<=s[1]:false",
    }[mode]
    
    range_logic = "if(m==='range'&&s.length===2&&!e){const[a,b]=s;if(c.date===a&&a!==b)l+=' range-start';else if(c.date===b&&a!==b)l+=' range-end';else if(c.date>a&&c.date<b){l+=' range-middle';if(y===0)l+=' range-week-start';if(y===6)l+=' range-week-end'}else if(a===b&&c.date===a)l+=' range-single'}" if mode == "range" else ""
    
    selected_setup = f"s=${signal}_selected||''" if mode == "single" else f"s=${signal}_selected||[]"
    
    return f"""const b=document.querySelector('[data-calendar-body="{signal}"]'),m='{mode}';if(!b)return;${signal}_selected;const y=parseInt(${signal}_year),mm=parseInt(${signal}_month);{gen_cal};const {selected_setup};let h='';let lastWeekWithDates=5;for(let w=5;w>=0;w--){{let hasDate=false;for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}};if(c.date){{hasDate=true;break}}}}if(hasDate){{lastWeekWithDates=w;break}}}}for(let w=0;w<=lastWeekWithDates;w++){{for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}},e=!c.date,t=c.date==='{today_str}',x={sel_check};let l='cal-cell h-9 w-9 text-center text-sm rounded-md transition-colors flex items-center justify-center';if(!e&&!{str(disabled).lower()})l+=' cursor-pointer';if(e)l+=' empty';if(t)l+=' today';if(!e&&x)l+=' selected';{range_logic}h+=`<div class="${{l}}" data-date="${{c.date||''}}">${{c.day||''}}</div>`}}}}b.innerHTML=h"""


_CALENDAR_STYLES = """
.cal-cell:not(.empty):not(.selected):hover{background-color:hsl(210 40% 96.1%)}
.cal-cell.selected{background-color:hsl(222.2 47.4% 11.2%)!important;color:hsl(210 40% 98%)!important}
.cal-cell.today{font-weight:600;box-shadow:inset 0 0 0 1px hsl(var(--border))}
.cal-cell.disabled{opacity:0.5;cursor:not-allowed}
.cal-cell.range-start{border-top-right-radius:0!important;border-bottom-right-radius:0!important}
.cal-cell.range-middle{border-radius:0!important;background-color:hsl(210 40% 96.1%);color:hsl(222.2 47.4% 11.2%)}
.cal-cell.range-middle.selected{background-color:hsl(222.2 47.4% 11.2%);color:hsl(210 40% 98%)}
.cal-cell.range-end{border-top-left-radius:0!important;border-bottom-left-radius:0!important}
.cal-cell.range-week-start{border-top-left-radius:0.375rem!important;border-bottom-left-radius:0.375rem!important}
.cal-cell.range-week-end{border-top-right-radius:0.375rem!important;border-bottom-right-radius:0.375rem!important}
[data-theme="dark"] .cal-cell:not(.empty):not(.selected):hover{background-color:hsl(217.2 32.6% 17.5%)}
[data-theme="dark"] .cal-cell.selected{background-color:hsl(210 40% 98%)!important;color:hsl(222.2 47.4% 11.2%)!important}
[data-theme="dark"] .cal-cell.range-middle{background-color:hsl(217.2 32.6% 17.5%);color:hsl(210 40% 98%)}
[data-theme="dark"] .cal-cell.range-middle.selected{background-color:hsl(210 40% 98%);color:hsl(222.2 47.4% 11.2%)}
.scrollbar-hide{scrollbar-width:none;-ms-overflow-style:none}
.scrollbar-hide::-webkit-scrollbar{display:none}
"""