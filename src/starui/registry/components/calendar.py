import json
from datetime import datetime
from typing import Any, Literal

from starhtml import Button as HTMLButton
from starhtml import Div, Icon, Span, Style, Signal, js

from .button import Button
from .utils import cn, gen_id

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
    on_select: str | list | None = None,
    cls: str = "",
    **kwargs: Any,
) -> Div:
    sig = signal or gen_id("calendar")
    today = datetime.now()
    current_month = month or today.month
    current_year = year or today.year
    today_str = today.strftime("%Y-%m-%d")

    if mode == "single":
        initial_selected = selected if isinstance(selected, str) else ""
    else:
        initial_selected = selected if isinstance(selected, list) else []

    calendar = Div(
        Style(_CALENDAR_STYLES),
        (month_sig := Signal(sig + "_month", current_month)),
        (year_sig := Signal(sig + "_year", current_year)),
        (month_display_sig := Signal(sig + "_month_display", MONTHS[current_month - 1])),
        (selected_sig := Signal(sig + "_selected", initial_selected)),
        _build_navigation(sig, month_sig, year_sig, month_display_sig, current_month, current_year, disabled),
        Div(
            _build_weekdays(),
            _build_calendar_grid(sig, selected_sig, mode, disabled, today_str, on_select),
            cls="w-full"
        ),
        *attrs,
        data_calendar=sig,
        role="application",
        aria_label="Calendar",
        cls=cn("p-3 border rounded-md w-fit", cls),
        **kwargs,
    )

    calendar.selected = selected_sig
    calendar.month = month_sig
    calendar.year = year_sig
    calendar.month_display = month_display_sig

    return calendar


def _build_navigation(sig: str, month, year, month_display, current_month: int, current_year: int, disabled: bool) -> Div:
    def nav_button(is_next: bool):
        direction = "right" if is_next else "left"
        label = "Next month" if is_next else "Previous month"
        return Button(
            Icon(f"lucide:chevron-{direction}", cls="h-4 w-4"),
            data_on_click=js(_nav_handler(month, year, month_display, is_next)) if not disabled else None,
            variant="outline",
            size="icon",
            disabled=disabled,
            aria_label=label,
            cls=f"h-7 w-7 absolute {direction}-0",
        )

    return Div(
        nav_button(False),
        Div(
            _build_dropdown(sig, month, year, month_display, "month", MONTHS[current_month - 1],
                          [(i+1, name) for i, name in enumerate(MONTHS)], disabled),
            _build_dropdown(sig, month, year, month_display, "year", current_year,
                          [(y, y) for y in range(current_year - 10, current_year + 11)], disabled),
            cls="flex items-center gap-1",
        ),
        nav_button(True),
        cls="relative flex items-center justify-center mb-4",
        role="group",
        aria_label="Calendar navigation",
    )


def _build_dropdown(sig: str, month, year, month_display, type: str, current_display: str | int, items: list[tuple], disabled: bool) -> Div:
    type_sig = month if type == "month" else year
    trigger_id = f"{sig}_{type}_trigger"
    trigger_ref = Signal(trigger_id, _ref_only=True)
    content_id = f"{sig}_{type}_content"
    content_ref = Signal(content_id, _ref_only=True)
    display_sig = month_display if type == "month" else type_sig

    trigger = HTMLButton(
        Span(
            data_text=display_sig,
            cls="pointer-events-none"
        ),
        Icon("lucide:chevron-down", cls="h-3 w-3 shrink-0 opacity-50 ml-1"),
        data_ref=trigger_id,
        id=trigger_id,
        popovertarget=content_id,
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

    position_mods = {
        "placement": "bottom",
        "offset": 8,
        "flip": True,
        "shift": True,
        "hide": True,
        "container": "none",  # Key for calendar dropdowns to position correctly
    }

    dropdown = Div(
        *[make_item(value, display) for value, display in items],
        data_on_click=js(_dropdown_handler(month, year, month_display, type, content_ref)) if not disabled else None,
        data_ref=content_id,
        data_style_min_width=trigger_ref.if_(trigger_ref.offsetWidth + 'px', '8rem'),
        data_position=(trigger_id, position_mods),
        popover="auto",
        id=content_id,
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


def _build_calendar_grid(sig: str, selected, mode: CalendarMode, disabled: bool, today_str: str, on_select: str | None) -> Div:
    return Div(
        data_effect=js(_render_days_effect(sig, selected, mode, disabled, today_str)),
        data_on_click=js(_day_select_handler(selected, mode, on_select)) if not disabled else None,
        cls="cal-body grid grid-cols-7 gap-0",
        data_calendar_body=sig,
        role="grid",
        aria_label="Calendar days",
    )


def _nav_handler(month, year, month_display, is_next: bool) -> str:
    op = "+" if is_next else "-"
    months_str = str(MONTHS)
    return f"let mm=parseInt({month}){op}1,y=parseInt({year});if(mm>12){{mm=1;y++}}else if(mm<1){{mm=12;y--}};{month}=mm;{year}=y;const months={months_str};{month_display}=months[mm-1]"


def _dropdown_handler(month, year, month_display, type: str, content_ref) -> str:
    close = content_ref.hidePopover()
    if type == "month":
        return f"const t=evt.target;if(!t.dataset.month)return;const m=parseInt(t.dataset.month),n=t.dataset.monthName;{month}=m;{month_display}=n;{close}"
    return f"const t=evt.target;if(!t.dataset.year)return;const y=parseInt(t.dataset.year);{year}=y;{close}"


def _day_select_handler(selected, mode: CalendarMode, on_select: str | list | None = None) -> str:
    parts = ["const c=evt.target.closest('.cal-cell');if(!c||c.classList.contains('empty'))return;const d=c.dataset.date;if(!d)return"]

    if isinstance(on_select, list):
        on_select = ";".join(str(a) for a in on_select)

    match mode:
        case "single":
            parts.append(f"{selected}={selected}===d?'':d")
            if on_select:
                parts.append(f"if({selected}){{{on_select}}}")
        case "multiple":
            parts.append(f"let s={selected}||[]")
            parts.append(f"const i=s.indexOf(d);{selected}=i>=0?s.filter((_,x)=>x!==i):[...s,d]")
            if on_select:
                parts.append(on_select)
        case "range":
            parts.append(f"let s={selected}||[]")
            parts.append(f"if(s.length===0){{{selected}=[d]}}else if(s.length===1){{if(s[0]===d){{{selected}=[]}}else{{{selected}=[s[0],d].sort()}}}}else{{{selected}=[d]}}")
            if on_select:
                parts.append(f"if({selected}.length===2){{{on_select}}}")

    return ";".join(parts)


def _render_days_effect(sig: str, selected, mode: CalendarMode, disabled: bool, today_str: str) -> str:
    gen_cal = "const f=new Date(y,mm-1,1),days=new Date(y,mm,0).getDate(),o=f.getDay(),a=[];for(let i=0;i<42;i++){const n=i-o+1,v=i>=o&&n<=days;a.push({day:v?n.toString():'',date:v?`${y}-${mm.toString().padStart(2,'0')}-${n.toString().padStart(2,'0')}`:'',empty:!v})}"
    
    sel_check = {
        "single": "s===c.date",
        "multiple": "s.includes(c.date)",
        "range": "s.length===1?c.date===s[0]:s.length===2?c.date>=s[0]&&c.date<=s[1]:false",
    }[mode]
    
    range_logic = "if(m==='range'&&s.length===2&&!e){const[a,b]=s;if(c.date===a&&a!==b)l+=' range-start';else if(c.date===b&&a!==b)l+=' range-end';else if(c.date>a&&c.date<b){l+=' range-middle';if(y===0)l+=' range-week-start';if(y===6)l+=' range-week-end'}else if(a===b&&c.date===a)l+=' range-single'}" if mode == "range" else ""
    
    selected_setup = f"s={selected}||''" if mode == "single" else f"s={selected}||[]"

    disabled_check = "if(!e)l+=' disabled';" if disabled else ""
    return f"""const b=document.querySelector('[data-calendar-body="{sig}"]'),m='{mode}';if(!b)return;{selected};const y=parseInt(${sig}_year),mm=parseInt(${sig}_month);{gen_cal};const {selected_setup};let h='';let lastWeekWithDates=5;for(let w=5;w>=0;w--){{let hasDate=false;for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}};if(c.date){{hasDate=true;break}}}}if(hasDate){{lastWeekWithDates=w;break}}}}for(let w=0;w<=lastWeekWithDates;w++){{for(let yy=0;yy<7;yy++){{const i=w*7+yy,c=a[i]||{{}},e=!c.date,t=c.date==='{today_str}',x={sel_check};let l='cal-cell h-9 w-9 text-center text-sm rounded-md transition-colors flex items-center justify-center';if(!e&&!{str(disabled).lower()})l+=' cursor-pointer';{disabled_check}if(e)l+=' empty';if(t)l+=' today';if(!e&&x)l+=' selected';{range_logic}h+=`<div class="${{l}}" data-date="${{c.date||''}}">${{c.day||''}}</div>`}}}}b.innerHTML=h"""


_CALENDAR_STYLES = """
.cal-cell:not(.empty):not(.selected):not(.disabled):hover{background-color:hsl(210 40% 96.1%)}
.cal-cell.selected{background-color:hsl(222.2 47.4% 11.2%)!important;color:hsl(210 40% 98%)!important}
.cal-cell.today{font-weight:600;box-shadow:inset 0 0 0 1px hsl(var(--border))}
.cal-cell.disabled{opacity:0.5;cursor:not-allowed;pointer-events:none}
.cal-cell.range-start{border-top-right-radius:0!important;border-bottom-right-radius:0!important}
.cal-cell.range-middle{border-radius:0!important;background-color:hsl(210 40% 96.1%);color:hsl(222.2 47.4% 11.2%)}
.cal-cell.range-middle.selected{background-color:hsl(222.2 47.4% 11.2%);color:hsl(210 40% 98%)}
.cal-cell.range-end{border-top-left-radius:0!important;border-bottom-left-radius:0!important}
.cal-cell.range-week-start{border-top-left-radius:0.375rem!important;border-bottom-left-radius:0.375rem!important}
.cal-cell.range-week-end{border-top-right-radius:0.375rem!important;border-bottom-right-radius:0.375rem!important}
[data-theme="dark"] .cal-cell:not(.empty):not(.selected):not(.disabled):hover{background-color:hsl(217.2 32.6% 17.5%)}
[data-theme="dark"] .cal-cell.selected{background-color:hsl(210 40% 98%)!important;color:hsl(222.2 47.4% 11.2%)!important}
[data-theme="dark"] .cal-cell.range-middle{background-color:hsl(217.2 32.6% 17.5%);color:hsl(210 40% 98%)}
[data-theme="dark"] .cal-cell.range-middle.selected{background-color:hsl(210 40% 98%);color:hsl(222.2 47.4% 11.2%)}
.scrollbar-hide{scrollbar-width:none;-ms-overflow-style:none}
.scrollbar-hide::-webkit-scrollbar{display:none}
"""