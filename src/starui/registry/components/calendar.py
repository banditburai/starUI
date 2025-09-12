import json
from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from starhtml import Button as HTMLButton
from starhtml import Div, Icon, Span, Style
from starhtml.datastar import (
    ds_effect,
    ds_on_click,
    ds_position,
    ds_ref,
    ds_signals,
    ds_style,
    ds_text,
    value,
)

from .button import Button
from .utils import cn

CalendarMode = Literal["single", "range", "multiple"]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def Calendar(
    *attrs,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    month: int | None = None,
    year: int | None = None,
    disabled: bool = False,
    on_select: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> Div:
    signal = signal or f"calendar_{uuid4().hex[:8]}"
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
        _build_navigation(signal, current_month, current_year, disabled),
        Div(
            _build_weekdays(),
            _build_calendar_grid(signal, mode, disabled, today_str, on_select),
            cls="w-full"
        ),
        *attrs,
        ds_signals(**_create_signals(signal, current_month, current_year, initial_selected)),
        data_calendar=signal,
        cls=cn("p-3 border border-input rounded-md w-fit", cls),
        **kwargs,
    )


def _build_navigation(signal: str, month: int, year: int, disabled: bool) -> Div:
    def nav_button(is_next: bool):
        direction = "right" if is_next else "left"
        return Button(
            Icon(f"lucide:chevron-{direction}", cls="h-4 w-4"),
            ds_on_click(_nav_handler(signal, is_next)) if not disabled else None,
            variant="outline",
            size="icon",
            disabled=disabled,
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
    )


def _build_dropdown(signal: str, type: str, current_display: str | int, items: list[tuple], disabled: bool) -> Div:
    trigger_id = f"{signal}_{type}_trigger"
    content_id = f"{signal}_{type}_content"
    
    trigger = HTMLButton(
        Span(ds_text(f"${signal}_{type}_display" if type == "month" else f"${signal}_{type}"), 
             cls="pointer-events-none"),
        Icon("lucide:chevron-down", cls="h-3 w-3 shrink-0 opacity-50 ml-1"),
        ds_ref(f"{signal}_{type}_trigger"),
        id=trigger_id,
        popovertarget=content_id,
        popoveraction="toggle",
        type="button",
        disabled=disabled,
        cls="flex h-7 items-center gap-1 rounded-md px-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground focus:outline-none disabled:opacity-50",
    )
    
    dropdown_items = [
        Div(
            str(display) if type == "year" else display,
            cls=cn(
                "px-2 py-1 text-sm rounded cursor-pointer hover:bg-accent hover:text-accent-foreground",
                "data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground",
            ),
            data_selected=f"${signal}_{type} === {value}",
            **{f"data_{type}": value, f"data_{type}_name": display} if type == "month" else {f"data_{type}": value}
        )
        for value, display in items
    ]
    
    dropdown = Div(
        *dropdown_items,
        ds_on_click(_dropdown_handler(signal, type, content_id)) if not disabled else None,
        ds_ref(f"{signal}_{type}_content"),
        ds_style(min_width=f"${signal}_{type}_trigger ? ${signal}_{type}_trigger.offsetWidth + 'px' : '8rem'"),
        ds_position(anchor=trigger_id, placement="bottom", offset=8, flip=True, shift=True, hide=True, container="none"),
        popover="auto",
        id=content_id,
        cls="z-50 max-h-[200px] overflow-y-auto scrollbar-hide rounded-md border bg-popover text-popover-foreground shadow-md outline-none dark:border-input",
    )
    
    return Div(trigger, dropdown, cls="relative")


def _build_weekdays() -> Div:
    weekdays = ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
    return Div(
        *[
            Div(day, cls="h-9 w-9 text-[0.8rem] font-normal text-muted-foreground text-center")
            for day in weekdays
        ],
        cls="grid grid-cols-7 border-b border-input mb-1",
    )


def _build_calendar_grid(signal: str, mode: CalendarMode, disabled: bool, today_str: str, on_select: str | None) -> Div:
    return Div(
        ds_effect(_render_days_effect(signal, mode, disabled, today_str)),
        ds_on_click(_day_select_handler(signal, mode, on_select)) if not disabled else None,
        cls="cal-body grid grid-cols-7 gap-0",
        data_calendar_body=signal,
    )


def _create_signals(signal: str, month: int, year: int, selected: str | list) -> dict:
    return {
        f"{signal}_month": value(month),
        f"{signal}_year": value(year),
        f"{signal}_month_display": value(MONTHS[month - 1]),
        f"{signal}_selected": value(json.dumps(selected) if isinstance(selected, list) else selected),
        f"{signal}_month_open": value(False),
        f"{signal}_year_open": value(False),
    }


def _nav_handler(signal: str, is_next: bool) -> str:
    op = "+" if is_next else "-"
    months_str = str(MONTHS)
    return f"let mm=parseInt(${signal}_month){op}1,y=parseInt(${signal}_year);if(mm>12){{mm=1;y++}}else if(mm<1){{mm=12;y--}};${signal}_month=mm;${signal}_year=y;const months={months_str};${signal}_month_display=months[mm-1]"


def _dropdown_handler(signal: str, type: str, content_id: str) -> str:
    if type == "month":
        return f"const t=event.target;if(!t.dataset.month)return;const m=parseInt(t.dataset.month),n=t.dataset.monthName;${signal}_month=m;${signal}_month_display=n;document.getElementById('{content_id}').hidePopover()"
    return f"const t=event.target;if(!t.dataset.year)return;const y=parseInt(t.dataset.year);${signal}_year=y;document.getElementById('{content_id}').hidePopover()"


def _day_select_handler(signal: str, mode: CalendarMode, on_select: str | None = None) -> str:
    base = "const c=event.target.closest('.cal-cell');if(!c||c.classList.contains('empty'))return;const d=c.dataset.date;if(!d)return;"
    
    match mode:
        case "single":
            logic = f"${signal}_selected=${signal}_selected===d?'':d"
        case "multiple":
            base += f"let s;try{{s=JSON.parse(${signal}_selected||'[]')}}catch{{s=[]}};"
            logic = f"const i=s.indexOf(d);${signal}_selected=JSON.stringify(i>=0?s.filter((_,x)=>x!==i):[...s,d])"
        case "range":
            base += f"let s;try{{s=JSON.parse(${signal}_selected||'[]')}}catch{{s=[]}};"
            logic = f"if(s.length===0){{${signal}_selected=JSON.stringify([d])}}else if(s.length===1){{if(s[0]===d){{${signal}_selected=JSON.stringify([])}}else{{${signal}_selected=JSON.stringify([s[0],d].sort())}}}}else{{${signal}_selected=JSON.stringify([d])}}"
    
    if not on_select:
        return base + logic
    
    match mode:
        case "single":
            return base + logic + f";if(${signal}_selected){{{on_select}}}"
        case "range":
            return base + logic + f";if(JSON.parse(${signal}_selected||'[]').length===2){{{on_select}}}"
        case _:
            return base + logic + f";{on_select}"


def _render_days_effect(signal: str, mode: CalendarMode, disabled: bool, today_str: str) -> str:
    gen_cal = "const f=new Date(y,mm-1,1),days=new Date(y,mm,0).getDate(),o=f.getDay(),a=[];for(let i=0;i<42;i++){const n=i-o+1,v=i>=o&&n<=days;a.push({day:v?n.toString():'',date:v?`${y}-${mm.toString().padStart(2,'0')}-${n.toString().padStart(2,'0')}`:'',empty:!v})}"
    
    sel_check = {
        "single": "s===c.date",
        "multiple": "s.includes(c.date)",
        "range": "s.length===1?c.date===s[0]:s.length===2?c.date>=s[0]&&c.date<=s[1]:false",
    }[mode]
    
    range_logic = "if(m==='range'&&s.length===2&&!e){const[a,b]=s;if(c.date===a&&a!==b)l+=' range-start';else if(c.date===b&&a!==b)l+=' range-end';else if(c.date>a&&c.date<b){l+=' range-middle';if(y===0)l+=' range-week-start';if(y===6)l+=' range-week-end'}else if(a===b&&c.date===a)l+=' range-single'}" if mode == "range" else ""
    
    selected_setup = f"s=${signal}_selected||''" if mode == "single" else f"s=JSON.parse(${signal}_selected||'[]')"
    
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