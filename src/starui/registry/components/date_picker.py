from datetime import datetime, timedelta
from typing import Any, Protocol

from starhtml import FT, Div, Icon, Span, Signal, js
from starhtml import Button as HTMLButton

from .button import Button
from .calendar import Calendar, CalendarElement, CalendarMode, MONTHS
from .input import Input
from .popover import Popover, PopoverContent, PopoverTrigger
from .utils import cn, gen_id, with_signals


class DatePickerElement(Protocol):
    selected: Signal  # str for single, list for range/multiple
    calendar: CalendarElement


class DateTimePickerElement(Protocol):
    datetime: Signal  # combined datetime string
    date: Signal
    time: Signal
    calendar: CalendarElement


def DatePicker(
    *attrs,
    signal: str | Signal = "",
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    placeholder: str | None = None,
    disabled: bool = False,
    cls: str = "",
    width: str = "w-[280px]",
    with_presets: bool = False,
    **kwargs: Any,
) -> DatePickerElement:
    sig = getattr(signal, '_id', signal) or gen_id("date_picker")
    cal = f"{sig}_calendar"

    if not placeholder:
        placeholder = {
            "single": "Select date" if with_presets else "Pick a date",
            "range": "Select date range",
            "multiple": "Select dates",
        }[mode]

    initial_selected = selected or ([] if mode in ("multiple", "range") else "")

    selected = Signal(f"{sig}_selected", initial_selected)
    cal_selected = Signal(f"{cal}_selected", initial_selected, _ref_only=True)
    popover_content_ref = Signal(f"{sig}_popover_content", _ref_only=True)

    on_select = [selected.set(cal_selected)] + ([popover_content_ref.hidePopover()] if mode in ("single", "range") else [])

    calendar = Calendar(
        signal=cal,
        mode=mode,
        selected=initial_selected,
        disabled=disabled,
        on_select=on_select if not disabled else None,
        cls="border-0 rounded-none",
    )

    if with_presets and mode == "single":
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
                    data_on_click=[selected.set(date), cal_selected.set(date), popover_content_ref.hidePopover()],
                    variant="ghost",
                    size="sm",
                    cls="w-full justify-start",
                    disabled=disabled,
                )
                for label, date in presets
            ],
            cls="flex flex-col gap-1 border-r pr-2",
        )
        content = Div(preset_buttons, calendar, cls="flex gap-2")
        popover_cls = "w-fit p-2"
    else:
        content = calendar
        popover_cls = "w-fit p-0"

    popover = Popover(
        _build_trigger(sig, selected, mode, placeholder, width, disabled, "lucide:calendar"),
        PopoverContent(content, cls=popover_cls, align="start", container="none"),
        signal=f"{sig}_popover",
    )

    return with_signals(
        Div(
            selected,
            popover,
            *attrs,
            cls=cn("inline-block", cls),
            **kwargs,
        ),
        selected=selected,
        calendar=calendar,
    )


def DateTimePicker(
    *attrs,
    signal: str | Signal = "",
    selected: str | None = None,
    placeholder: str = "Select date and time",
    disabled: bool = False,
    cls: str = "",
    width: str = "w-[280px]",
    **kwargs: Any,
) -> DateTimePickerElement:
    sig = getattr(signal, '_id', signal) or gen_id("datetime_picker")
    cal = f"{sig}_calendar"

    initial_date, initial_time = _parse_datetime(selected)
    hours, minutes = (initial_time.split(":") if initial_time else ("12", "00"))
    hour_24 = int(hours)
    is_pm = hour_24 >= 12
    hour_12 = hour_24 % 12 or 12

    selected = Signal(f"{sig}_selected", initial_date)
    time = Signal(f"{sig}_time", initial_time)
    hour_display = Signal(f"{sig}_hour_display", f"{hour_12:02d}")
    minute_display = Signal(f"{sig}_minute_display", minutes)
    pm = Signal(f"{sig}_pm", is_pm)
    datetime = Signal(f"{sig}_datetime", f"{initial_date}T{initial_time}" if initial_date and initial_time else "")
    cal_selected = Signal(f"{cal}_selected", initial_date, _ref_only=True)

    calendar = Calendar(
        signal=cal,
        mode="single",
        selected=initial_date,
        disabled=disabled,
        cls="border-0 rounded-none",
    )

    content = Div(
        calendar,
        _build_time_section(sig, hour_display, minute_display, pm, time, disabled),
        cls="flex flex-col",
    )

    popover = Popover(
        _build_trigger(sig, selected, "single", placeholder, width, disabled, "lucide:calendar-clock", time=time),
        PopoverContent(content, cls="w-fit p-0 max-h-[600px] overflow-y-auto", align="start", offset=8, container="none"),
    )

    return with_signals(
        Div(
            selected,
            hour_display,
            minute_display,
            pm,
            time,
            datetime,
            popover,
            *attrs,
            data_effect=js(_datetime_sync_effect(selected, cal_selected, hour_display, minute_display, pm, time, datetime)),
            cls=cn("inline-block", cls),
            **kwargs,
        ),
        datetime=datetime,
        date=selected,
        time=time,
        calendar=calendar,
    )


def DatePickerWithInput(
    *attrs,
    signal: str | Signal = "",
    selected: str | None = None,
    placeholder: str = "Select date",
    format: str = "YYYY-MM-DD",
    disabled: bool = False,
    cls: str = "",
    width: str = "w-[280px]",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, '_id', signal) or gen_id("date_input")
    cal = f"{sig}_calendar"
    initial_selected = selected or ""

    trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)
    content_ref = Signal(f"{sig}_content", _ref_only=True)

    selected_sig = Signal(f"{sig}_selected", initial_selected)
    cal_selected = Signal(f"{cal}_selected", initial_selected, _ref_only=True)
    cal_month = Signal(f"{cal}_month", _ref_only=True)
    cal_year = Signal(f"{cal}_year", _ref_only=True)
    cal_month_display = Signal(f"{cal}_month_display", _ref_only=True)

    input_ref = Signal(f"{sig}_input", _ref_only=True)

    input_with_popover = Div(
        Input(
            type="text",
            placeholder=format,
            value=initial_selected,
            data_ref=input_ref,
            cls=cn(width, "pr-10"),
            disabled=disabled,
        ),
        Button(
            Icon("lucide:calendar", cls="h-4 w-4 text-muted-foreground"),
            data_ref=trigger_ref,
            id=trigger_ref._id,
            popovertarget=content_ref._id,
            popoveraction="toggle",
            variant="ghost",
            size="icon",
            aria_haspopup="dialog",
            aria_describedby=content_ref._id,
            data_slot="popover-trigger",
            cls="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7 px-0 hover:bg-transparent",
            disabled=disabled,
        ),
        _build_input_popover_content(content_ref._id, trigger_ref._id, cal, initial_selected, disabled),
        cls="relative inline-block",
    )

    return with_signals(
        Div(
            selected_sig,
            input_with_popover,
            *attrs,
            data_effect=js(f"{_input_sync_effect(selected_sig, cal_selected, cal_month, cal_year, cal_month_display, input_ref)};{_input_close_effect(selected_sig, content_ref)}"),
            cls=cn("inline-block", cls),
            **kwargs,
        ),
        selected=selected_sig,
    )


def _build_input_popover_content(content_id: str, trigger_id: str, cal: str, initial_selected: str, disabled: bool) -> Div:
    position_mods = {
        "placement": "bottom-end",
        "flip": True,
        "shift": True,
        "hide": True,
        "container": "none",
    }

    return Div(
        Calendar(
            signal=cal,
            mode="single",
            selected=initial_selected,
            disabled=disabled,
            cls="border-0 rounded-none",
        ),
        data_ref=content_id,
        data_position=(trigger_id, position_mods),
        popover="auto",
        id=content_id,
        role="dialog",
        tabindex="-1",
        data_slot="popover-content",
        cls="z-50 rounded-md border border-input bg-popover text-popover-foreground shadow-md outline-none w-fit p-0",
    )


def _build_trigger(sig: str, selected, mode: CalendarMode, placeholder: str, width: str, disabled: bool, icon: str, time=None) -> PopoverTrigger:
    display_text = _get_display_text(selected, mode, placeholder, time=time)
    is_empty = ~selected if mode == "single" else ~selected.or_([]).length

    return PopoverTrigger(
        Span(
            Icon(icon, cls="mr-2 h-4 w-4"),
            Span(data_text=js(display_text), cls="text-left"),
            data_attr_class=is_empty.if_("text-muted-foreground flex items-center", "flex items-center"),
        ),
        variant="outline",
        cls=cn(width, "justify-start text-left font-normal"),
        disabled=disabled,
        data_picker_trigger=sig,
    )


def _build_time_section(sig: str, hour_display, minute_display, pm, time, disabled: bool) -> Div:
    return Div(
        Span("Time", cls="text-sm font-medium text-muted-foreground mb-2 block"),
        Div(
            _build_time_dropdown(sig, hour_display, minute_display, pm, time, "hour", disabled),
            Span(":", cls="text-xl font-semibold text-muted-foreground mx-0.5"),
            _build_time_dropdown(sig, hour_display, minute_display, pm, time, "minute", disabled),
            _build_ampm_toggle(hour_display, minute_display, pm, time, disabled),
            cls="flex items-center justify-center gap-1",
        ),
        cls="p-4 pt-3 border-t",
    )


def _build_time_dropdown(sig: str, hour_display, minute_display, pm, time, field: str, disabled: bool) -> Div:
    trigger_ref = Signal(f"{sig}_{field}_trigger", _ref_only=True)
    content_ref = Signal(f"{sig}_{field}_content", _ref_only=True)
    display = hour_display if field == "hour" else minute_display

    base_items = list(range(1, 13)) if field == "hour" else list(range(0, 60))
    base_count = len(base_items)
    items = base_items * 3

    trigger = HTMLButton(
        Span(data_text=display, cls="pointer-events-none font-mono text-base"),
        Icon("lucide:chevron-down", cls="h-3 w-3 shrink-0 opacity-50 ml-1"),
        data_ref=trigger_ref,
        id=trigger_ref._id,
        popovertarget=content_ref._id,
        popoveraction="toggle",
        type="button",
        disabled=disabled,
        aria_label=f"Select {field}",
        aria_haspopup="listbox",
        cls="flex h-8 w-16 items-center justify-center gap-1 rounded-md px-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground focus:outline-none disabled:opacity-50 border",
    )

    item_cls = cn(
        "px-3 py-1.5 text-sm font-mono rounded cursor-pointer hover:bg-accent hover:text-accent-foreground",
        "data-[selected=true]:bg-primary data-[selected=true]:text-primary-foreground",
    )

    def make_item(val: int, idx: int):
        val_str = f"{val:02d}"
        return Div(
            val_str,
            cls=item_cls,
            data_selected=display == val_str,
            data_value=str(val),
            data_section=str(idx // base_count),
            role="option",
        )

    dropdown = Div(
        *[make_item(val, idx) for idx, val in enumerate(items)],
        data_on_click=js(_time_select_handler(display, hour_display, minute_display, pm, time, content_ref)) if not disabled else None,
        data_on_scroll=js(_circular_scroll_handler(base_count)) if not disabled else None,
        data_effect=js(_init_scroll_position(content_ref, base_count, display)),
        data_ref=content_ref,
        data_style_min_width=trigger_ref.if_(trigger_ref.offsetWidth + 'px', '4rem'),
        data_position=(trigger_ref._id, {
            "placement": "top",
            "offset": 4,
            "flip": True,
            "shift": True,
            "hide": True,
            "container": "none",
        }),
        popover="auto",
        id=content_ref._id,
        role="listbox",
        aria_label=f"{field.capitalize()} selection",
        cls="z-50 max-h-[180px] overflow-y-auto scrollbar-hide rounded-md border bg-popover text-popover-foreground shadow-md outline-none",
    )

    return Div(trigger, dropdown, cls="relative")


def _build_ampm_toggle(hour_display, minute_display, pm, time, disabled: bool) -> Div:
    def make_button(label: str, is_pm: bool, rounding: str):
        is_selected = pm if is_pm else ~pm
        return HTMLButton(
            label,
            data_on_click=[pm.set(is_pm), js(_update_time_signal(hour_display, minute_display, pm, time))] if not disabled else None,
            data_attr_cls=is_selected.if_("bg-primary text-primary-foreground font-semibold", ""),
            type="button",
            disabled=disabled,
            cls=f"h-8 w-10 text-xs {rounding} transition-colors border hover:bg-accent hover:text-accent-foreground",
        )

    return Div(make_button("AM", False, "rounded-l-md"), make_button("PM", True, "rounded-r-md"), cls="flex ml-2")


def _time_select_handler(display, hour_display, minute_display, pm, time, content_ref) -> str:
    return f"const t=evt.target;const v=t.dataset.value;if(!v)return;{display}=v.padStart(2,'0');{_update_time_signal(hour_display, minute_display, pm, time)};{content_ref}.hidePopover()"


def _update_time_signal(hour_display, minute_display, pm, time) -> str:
    return f"const h=parseInt({hour_display})||12,m=parseInt({minute_display})||0,pm={pm};const h24=pm?(h===12?12:h+12):(h===12?0:h);{time}=`${{h24.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}`"


def _parse_datetime(selected: str | None) -> tuple[str, str]:
    if selected and "T" in selected:
        parts = selected.split("T", 1)
        return parts[0], parts[1][:5] if len(parts) > 1 else ""
    return "", ""


def _get_display_text(selected, mode: CalendarMode, placeholder: str, time=None) -> str:
    if time is not None:
        return f"(()=>{{const d={selected},t={time};if(!d&&!t)return'{placeholder}';let r='';if(d){{const[y,m,dy]=d.split('-').map(Number);r=new Date(y,m-1,dy).toLocaleDateString('en-US',{{year:'numeric',month:'long',day:'numeric'}})}}if(t){{r+=(r?' at ':'')+t}}return r}})()"

    match mode:
        case "single":
            return f"{selected}?(()=>{{const[y,m,d]={selected}.split('-').map(Number);return new Date(y,m-1,d).toLocaleDateString('en-US',{{year:'numeric',month:'long',day:'numeric'}})}})():'{placeholder}'"
        case "multiple":
            return f"(()=>{{const a={selected}||[];return a.length?`${{a.length}} date${{a.length>1?'s':''}} selected`:'{placeholder}'}})()"
        case "range":
            fmt = "toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})"
            return f"(()=>{{const a={selected}||[];return a.length===2?(()=>{{const[y1,m1,d1]=a[0].split('-').map(Number);const[y2,m2,d2]=a[1].split('-').map(Number);return new Date(y1,m1-1,d1).{fmt}+' - '+new Date(y2,m2-1,d2).{fmt}}})():a.length===1?(()=>{{const[y,m,d]=a[0].split('-').map(Number);return new Date(y,m-1,d).{fmt}}})():'{placeholder}'}})()"


def _datetime_sync_effect(selected, cal_selected, hour_display, minute_display, pm, time, datetime) -> str:
    return f"const c={cal_selected}??'',p={selected}??'';if(c!==p){selected}=c;const h=parseInt({hour_display})||12,m=parseInt({minute_display})||0,pm={pm};const h24=pm?(h===12?12:h+12):(h===12?0:h);{time}=`${{h24.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}`;const d={selected};if(d&&{time}){{{datetime}=`${{d}}T${{{time}}}:00`}}"


def _input_sync_effect(selected, cal_selected, cal_month, cal_year, cal_month_display, input_ref) -> str:
    return f"const c={cal_selected}??'',i={input_ref},ps={selected}??'';if(i&&c&&c!==ps){{i.value=c;{selected}=c}}if(i){{const u=()=>{{const v=i.value;if(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(v)){{{selected}=v;{cal_selected}=v;const[y,m,d]=v.split('-').map(Number);{cal_month}=m;{cal_year}=y;const M={str(MONTHS)};{cal_month_display}=M[m-1]}}}};i.removeEventListener('change',u);i.addEventListener('change',u)}}"


def _input_close_effect(selected, content_ref) -> str:
    return f"const s={selected}??'',k='_prev_'+{selected},p=window[k];if(s&&s!==p&&{content_ref}?.matches(':popover-open')){{{content_ref}.hidePopover()}}window[k]=s"


def _circular_scroll_handler(base_count: int) -> str:
    return f"""const items=evt.currentTarget.children;if(items.length===0)return;const itemHeight=items[0].offsetHeight;const sectionHeight={base_count}*itemHeight;const scrollTop=evt.currentTarget.scrollTop;const threshold=itemHeight*2;if(scrollTop<threshold){{evt.currentTarget.scrollTop=sectionHeight+scrollTop}}else if(scrollTop>sectionHeight*2-threshold){{evt.currentTarget.scrollTop=scrollTop-sectionHeight}}"""


def _init_scroll_position(content_ref, base_count: int, display: str) -> str:
    return f"""const dropdown={content_ref};if(!dropdown||dropdown._scrollInit)return;if(dropdown.matches(':popover-open')){{const items=dropdown.children;if(items.length>0){{const itemHeight=items[0].offsetHeight;const baseCount={base_count};const currentVal={display};const targetIdx=baseCount+(currentVal?parseInt(currentVal)-(baseCount>12?0:1):0);if(items[targetIdx]){{dropdown.scrollTop=items[targetIdx].offsetTop-(dropdown.clientHeight/2)+(itemHeight/2)}}else{{dropdown.scrollTop=baseCount*itemHeight}}dropdown._scrollInit=true}}}}"""