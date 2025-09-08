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
    ds_text,
    value,
)

from .button import Button
from .utils import cn

CalendarMode = Literal["single", "range", "multiple"]

MONTHS = [
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


def Calendar(
    *,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    month: int | None = None,
    year: int | None = None,
    disabled: bool = False,
    on_select: str | None = None,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    signal = signal or f"calendar_{uuid4().hex[:8]}"
    today = datetime.now()
    current_month = month or today.month
    current_year = year or today.year
    today_str = today.strftime("%Y-%m-%d")

    initial_selected = (
        selected
        if isinstance(selected, list) and mode in ("multiple", "range")
        else selected
        if isinstance(selected, str) and mode == "single"
        else []
        if mode in ("multiple", "range")
        else ""
    )

    years = list(range(current_year - 10, current_year + 11))

    signals = {
        f"{signal}_month": value(current_month),
        f"{signal}_year": value(current_year),
        f"{signal}_month_display": value(MONTHS[current_month - 1]),
        f"{signal}_selected": value(json.dumps(initial_selected))
        if isinstance(initial_selected, list)
        else value(initial_selected),
        f"{signal}_month_open": value(False),
        f"{signal}_year_open": value(False),
    }

    return Div(
        Style(_CALENDAR_STYLES),
        Div(
            Button(
                Icon("lucide:chevron-left", cls="h-4 w-4"),
                *([ds_on_click(_nav_handler(signal, False))] if not disabled else []),
                variant="outline",
                size="icon",
                disabled=disabled,
                cls="h-7 w-7 absolute left-0",
            ),
            Div(
                Div(
                    HTMLButton(
                        Span(
                            ds_text(f"${signal}_month_display"),
                            cls="pointer-events-none",
                        ),
                        Icon(
                            "lucide:chevron-down",
                            cls="h-3 w-3 shrink-0 opacity-50 ml-1",
                        ),
                        ds_ref(f"{signal}MonthTrigger"),
                        id=f"{signal}-month-trigger",
                        popovertarget=f"{signal}-month-content",
                        popoveraction="toggle",
                        type="button",
                        disabled=disabled,
                        cls="flex h-7 items-center gap-1 rounded-md px-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground focus:outline-none disabled:opacity-50",
                    ),
                    Div(
                        *[
                            Div(
                                month_name,
                                cls=cn(
                                    "px-2 py-1 text-sm rounded cursor-pointer hover:bg-accent hover:text-accent-foreground",
                                    "data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground",
                                ),
                                data_selected=f"${signal}_month === {idx + 1}",
                                data_month=idx + 1,
                                data_month_name=month_name,
                            )
                            for idx, month_name in enumerate(MONTHS)
                        ],
                        ds_on_click(_shared_month_handler(signal))
                        if not disabled
                        else None,
                        ds_ref(f"{signal}MonthContent"),
                        ds_position(
                            anchor=f"{signal}-month-trigger",
                            placement="bottom",
                            offset=4,
                            flip=True,
                            shift=True,
                            hide=True,
                        ),
                        popover="auto",
                        id=f"{signal}-month-content",
                        cls="z-50 max-h-[200px] overflow-y-auto scrollbar-hide rounded-md border bg-popover text-popover-foreground shadow-md outline-none dark:border-input",
                    ),
                    cls="relative",
                ),
                Div(
                    HTMLButton(
                        Span(
                            ds_text(f"${signal}_year"),
                            cls="pointer-events-none",
                        ),
                        Icon(
                            "lucide:chevron-down",
                            cls="h-3 w-3 shrink-0 opacity-50 ml-1",
                        ),
                        ds_ref(f"{signal}YearTrigger"),
                        id=f"{signal}-year-trigger",
                        popovertarget=f"{signal}-year-content",
                        popoveraction="toggle",
                        type="button",
                        disabled=disabled,
                        cls="flex h-7 items-center gap-1 rounded-md px-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground focus:outline-none disabled:opacity-50",
                    ),
                    Div(
                        *[
                            Div(
                                str(year_val),
                                cls=cn(
                                    "px-2 py-1 text-sm rounded cursor-pointer hover:bg-accent hover:text-accent-foreground",
                                    "data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground",
                                ),
                                data_selected=f"${signal}_year === {year_val}",
                                data_year=year_val,
                            )
                            for year_val in years
                        ],
                        ds_on_click(_shared_year_handler(signal))
                        if not disabled
                        else None,
                        ds_ref(f"{signal}YearContent"),
                        ds_position(
                            anchor=f"{signal}-year-trigger",
                            placement="bottom",
                            offset=4,
                            flip=True,
                            shift=True,
                            hide=True,
                        ),
                        popover="auto",
                        id=f"{signal}-year-content",
                        cls="z-50 max-h-[200px] overflow-y-auto scrollbar-hide rounded-md border bg-popover text-popover-foreground shadow-md outline-none dark:border-input",
                    ),
                    cls="relative",
                ),
                cls="flex items-center gap-1",
            ),
            Button(
                Icon("lucide:chevron-right", cls="h-4 w-4"),
                *([ds_on_click(_nav_handler(signal, True))] if not disabled else []),
                variant="outline",
                size="icon",
                disabled=disabled,
                cls="h-7 w-7 absolute right-0",
            ),
            cls="relative flex items-center justify-center mb-4",
        ),
        Div(
            Div(
                *[
                    Div(
                        day,
                        cls="h-9 w-9 text-[0.8rem] font-normal text-muted-foreground text-center",
                    )
                    for day in ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
                ],
                cls="grid grid-cols-7 border-b border-input mb-1",
            ),
            Div(
                ds_effect(_render_effect(signal, mode, disabled, today_str)),
                *(
                    [ds_on_click(_select_handler(signal, mode, on_select))]
                    if not disabled
                    else []
                ),
                cls="cal-body grid grid-cols-7 gap-0",
                data_calendar_body=signal,
            ),
            cls="w-full",
        ),
        ds_signals(**signals),
        data_calendar=signal,
        cls=cn("p-3 border border-input rounded-md w-fit", class_name, cls),
        **attrs,
    )


def _gen_cal_js() -> str:
    """Generate calendar data array in JavaScript."""
    return "const f=new Date(y,mm-1,1),days=new Date(y,mm,0).getDate(),o=f.getDay(),a=[];for(let i=0;i<42;i++){const n=i-o+1,v=i>=o&&n<=days;a.push({day:v?n.toString():'',date:v?`${y}-${mm.toString().padStart(2,'0')}-${n.toString().padStart(2,'0')}`:'',empty:!v})}"


def _shared_month_handler(signal: str) -> str:
    return f"const t=event.target;if(!t.dataset.month)return;const m=parseInt(t.dataset.month),n=t.dataset.monthName;${signal}_month=m;${signal}_month_display=n;document.getElementById('{signal}-month-content').hidePopover()"


def _shared_year_handler(signal: str) -> str:
    return f"const t=event.target;if(!t.dataset.year)return;const y=parseInt(t.dataset.year);${signal}_year=y;document.getElementById('{signal}-year-content').hidePopover()"


def _nav_handler(signal: str, is_next: bool) -> str:
    op = "+" if is_next else "-"
    months_str = str(MONTHS)
    return f"let mm=parseInt(${signal}_month){op}1,y=parseInt(${signal}_year);if(mm>12){{mm=1;y++}}else if(mm<1){{mm=12;y--}};${signal}_month=mm;${signal}_year=y;const months={months_str};${signal}_month_display=months[mm-1]"


def _select_handler(
    signal: str, mode: CalendarMode, on_select: str | None = None
) -> str:
    base = "const c=event.target.closest('.cal-cell');if(!c||c.classList.contains('empty'))return;const d=c.dataset.date;if(!d)return;"

    if mode == "single":
        select_logic = f"${signal}_selected=${signal}_selected===d?'':d"
    elif mode == "multiple":
        base += f"let s;try{{s=JSON.parse(${signal}_selected||'[]')}}catch{{s=[]}};"
        select_logic = f"const i=s.indexOf(d);${signal}_selected=JSON.stringify(i>=0?s.filter((_,x)=>x!==i):[...s,d])"
    else:
        base += f"let s;try{{s=JSON.parse(${signal}_selected||'[]')}}catch{{s=[]}};"
        select_logic = f"if(s.length===0){{${signal}_selected=JSON.stringify([d])}}else if(s.length===1){{if(s[0]===d){{${signal}_selected=JSON.stringify([])}}else{{${signal}_selected=JSON.stringify([s[0],d].sort())}}}}else{{${signal}_selected=JSON.stringify([d])}}"

    if on_select:
        if mode == "single":
            return base + select_logic + f";if(${signal}_selected){{{on_select}}}"
        elif mode == "range":
            return (
                base
                + select_logic
                + f";if(JSON.parse(${signal}_selected||'[]').length===2){{{on_select}}}"
            )
        else:
            return base + select_logic + f";{on_select}"
    return base + select_logic


def _render_effect(
    signal: str, mode: CalendarMode, disabled: bool, today_str: str
) -> str:
    sel_check = {
        "single": "s===c.date",
        "multiple": "s.includes(c.date)",
        "range": "s.length===1?c.date===s[0]:s.length===2?c.date>=s[0]&&c.date<=s[1]:false",
    }[mode]

    range_logic = ""
    if mode == "range":
        range_logic = "if(m==='range'&&s.length===2&&!e){const[a,b]=s;if(c.date===a&&a!==b)l+=' range-start';else if(c.date===b&&a!==b)l+=' range-end';else if(c.date>a&&c.date<b){l+=' range-middle';if(y===0)l+=' range-week-start';if(y===6)l+=' range-week-end'}else if(a===b&&c.date===a)l+=' range-single'}"

    if mode == "single":
        selected_setup = f"s=${signal}_selected||''"
    else:
        selected_setup = f"s=JSON.parse(${signal}_selected||'[]')"

    gen_cal = _gen_cal_js()

    return f"const b=document.querySelector('[data-calendar-body=\"{signal}\"]'),m='{mode}';if(!b)return;${signal}_selected;const y=parseInt(${signal}_year),mm=parseInt(${signal}_month);{gen_cal};const {selected_setup};let h='';let lastWeekWithDates=5;for(let w=5;w>=0;w--){{let hasDate=false;for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}};if(c.date){{hasDate=true;break}}}}if(hasDate){{lastWeekWithDates=w;break}}}}for(let w=0;w<=lastWeekWithDates;w++){{for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}},e=!c.date,t=c.date==='{today_str}',x={sel_check};let l='cal-cell h-9 w-9 text-center text-sm rounded-md transition-colors flex items-center justify-center';if(!e&&!{str(disabled).lower()})l+=' cursor-pointer';if(e)l+=' empty';if(t)l+=' today';if(!e&&x)l+=' selected';{range_logic}h+=`<div class=\"${{l}}\" data-date=\"${{c.date||''}}\">${{c.day||''}}</div>`}}}}b.innerHTML=h"


def _format_month_year(month: int, year: int) -> str:
    return f"{MONTHS[month - 1]} {year}"


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
/* Hide scrollbar but keep functionality */
.scrollbar-hide{scrollbar-width:none;-ms-overflow-style:none}
.scrollbar-hide::-webkit-scrollbar{display:none}
"""
