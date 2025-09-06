from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from starhtml import Div, Icon, Input, Span
from starhtml.datastar import ds_effect, ds_on_click, ds_signals, value

from .button import Button
from .calendar import Calendar, CalendarMode
from .popover import Popover, PopoverContent, PopoverTrigger
from .utils import cn


def DatePicker(
    *,
    signal: str | None = None,
    mode: CalendarMode = "single",
    selected: str | list[str] | None = None,
    placeholder: str = "Select date",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    signal = signal or f"date_picker_{uuid4().hex[:8]}"

    initial_selected = (
        selected
        if isinstance(selected, list) and mode in ("multiple", "range")
        else selected
        if isinstance(selected, str) and mode == "single"
        else []
        if mode in ("multiple", "range")
        else ""
    )

    display_placeholder = placeholder
    calendar_signal = f"{signal}_calendar"

    # Create a custom calendar with the picker signal
    calendar_with_picker_sync = Div(
        Calendar(
            signal=calendar_signal,
            mode=mode,
            selected=initial_selected,
            disabled=disabled,
            cls="border-0 rounded-none",
        ),
        # Add a click handler that syncs to the picker signal
        ds_on_click(_calendar_to_picker_handler(signal, calendar_signal, mode))
        if not disabled
        else None,
    )

    return Div(
        Popover(
            PopoverTrigger(
                Icon("lucide:calendar", cls="absolute left-3 h-4 w-4 opacity-50"),
                Span(
                    display_placeholder,
                    data_picker_display=signal,
                    cls="flex-1 text-left",
                ),
                variant="outline",
                cls=cn(
                    "w-[240px] pl-9 justify-start text-left font-normal relative",
                    "data-[empty=true]:text-muted-foreground",
                ),
                data_empty="true",
                data_picker_trigger=signal,
                disabled=disabled,
            ),
            PopoverContent(
                calendar_with_picker_sync,
                cls="w-fit p-0",
                align="start",
            ),
        ),
        ds_signals(**{f"{signal}_selected": value(initial_selected)}),
        ds_effect(_display_effect(signal, mode, placeholder)),
        ds_effect(_selection_sync_to_calendar(signal, calendar_signal)),
        *(
            [ds_effect(effect)]
            if (effect := _close_on_select_effect(signal, mode))
            else []
        ),
        cls=cn("inline-block", class_name, cls),
        **attrs,
    )


def DatePickerWithPresets(
    *,
    signal: str | None = None,
    selected: str | None = None,
    placeholder: str = "Select date",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    signal = signal or f"date_picker_presets_{uuid4().hex[:8]}"

    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    week_later = today + timedelta(days=7)

    initial_selected = selected or ""
    calendar_signal = f"{signal}_calendar"

    presets = [
        ("Today", today.strftime("%Y-%m-%d")),
        ("Tomorrow", tomorrow.strftime("%Y-%m-%d")),
        ("In a week", week_later.strftime("%Y-%m-%d")),
    ]

    return Div(
        Popover(
            PopoverTrigger(
                Icon("lucide:calendar", cls="absolute left-3 h-4 w-4 opacity-50"),
                Span(
                    placeholder,
                    data_picker_display=signal,
                    cls="flex-1 text-left",
                ),
                variant="outline",
                cls=cn(
                    "w-[240px] pl-9 justify-start text-left font-normal relative",
                    "data-[empty=true]:text-muted-foreground",
                ),
                data_empty="true",
                data_picker_trigger=signal,
                disabled=disabled,
            ),
            PopoverContent(
                Div(
                    Div(
                        *[
                            Button(
                                label,
                                ds_on_click(f"{signal}_selected = '{date}'"),
                                variant="ghost",
                                size="sm",
                                cls="w-full justify-start",
                                disabled=disabled,
                            )
                            for label, date in presets
                        ],
                        cls="flex flex-col gap-1 border-r pr-2",
                    ),
                    Calendar(
                        signal=calendar_signal,
                        mode="single",
                        selected=initial_selected,
                        disabled=disabled,
                        cls="p-3 pl-2 border-0 rounded-none",
                    ),
                    cls="flex gap-2",
                ),
                cls="w-fit p-2",
                align="start",
            ),
        ),
        ds_signals(**{f"{signal}_selected": value(initial_selected)}),
        ds_effect(_display_effect(signal, "single", placeholder)),
        ds_effect(_selection_sync_to_calendar(signal, calendar_signal)),
        ds_effect(_selection_sync_from_calendar(signal, calendar_signal)),
        ds_effect(_close_on_select_effect(signal, "single")),
        cls=cn("inline-block", class_name, cls),
        **attrs,
    )


def DateRangePicker(
    *,
    signal: str | None = None,
    selected: list[str] | None = None,
    placeholder: str = "Select date range",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    return DatePicker(
        signal=signal,
        mode="range",
        selected=selected,
        placeholder=placeholder,
        disabled=disabled,
        class_name=class_name,
        cls=cls,
        **attrs,
    )


def DateTimePicker(
    *,
    signal: str | None = None,
    selected: str | None = None,
    placeholder: str = "Select date and time",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> Div:
    """Date and time picker component."""
    signal = signal or f"datetime_picker_{uuid4().hex[:8]}"

    initial_date = selected or ""
    initial_time = "00:00"
    if selected and "T" in selected:
        date_part, time_part = selected.split("T")
        initial_date = date_part
        initial_time = time_part[:5]  # HH:MM format

    calendar_signal = f"{signal}_calendar"

    return Div(
        Popover(
            PopoverTrigger(
                Icon("lucide:calendar-clock", cls="absolute left-3 h-4 w-4 opacity-50"),
                Span(
                    placeholder,
                    data_picker_display=signal,
                    cls="flex-1 text-left",
                ),
                variant="outline",
                cls=cn(
                    "w-[280px] pl-9 justify-start text-left font-normal relative",
                    "data-[empty=true]:text-muted-foreground",
                ),
                data_empty="true",
                data_picker_trigger=signal,
                disabled=disabled,
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
                    Div(
                        Div(
                            Span("Time", cls="text-sm font-medium"),
                            Input(
                                type="time",
                                value=initial_time,
                                data_time_input=signal,
                                cls="w-full",
                                disabled=disabled,
                            ),
                            cls="space-y-2",
                        ),
                        cls="p-3 border-t",
                    ),
                    cls="flex flex-col",
                ),
                cls="w-fit p-0",
                align="start",
            ),
        ),
        ds_signals(
            **{
                f"{signal}_selected": value(initial_date),
                f"{signal}_time": value(initial_time),
                f"{signal}_datetime": value(selected or ""),
            }
        ),
        ds_effect(_datetime_display_effect(signal, placeholder)),
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
    **attrs: Any,
) -> Div:
    """Date picker with manual input field."""
    signal = signal or f"date_input_{uuid4().hex[:8]}"

    initial_selected = selected or ""
    calendar_signal = f"{signal}_calendar"

    return Div(
        Div(
            Input(
                type="text",
                placeholder=format,
                value=initial_selected,
                data_date_input=signal,
                cls="w-[240px] pr-10",
                disabled=disabled,
            ),
            Popover(
                PopoverTrigger(
                    Icon("lucide:calendar", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                    cls="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent",
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
        ),
        ds_signals(**{f"{signal}_selected": value(initial_selected)}),
        ds_effect(_input_sync_effect(signal, calendar_signal)),
        ds_effect(_input_close_effect(signal)),
        cls=cn("inline-block", class_name, cls),
        **attrs,
    )


def _display_effect(signal: str, mode: CalendarMode, placeholder: str) -> str:
    if mode == "single":
        return f"""
            const el = document.querySelector('[data-picker-display="{signal}"]');
            const trigger = document.querySelector('[data-picker-trigger="{signal}"]');
            const selected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
            if (el) {{
                if (selected && selected !== '') {{
                    const d = new Date(selected);
                    const options = {{year: 'numeric', month: 'long', day: 'numeric'}};
                    el.textContent = d.toLocaleDateString('en-US', options);
                    trigger?.setAttribute('data-empty', 'false');
                }} else {{
                    el.textContent = '{placeholder}';
                    trigger?.setAttribute('data-empty', 'true');
                }}
            }}
        """
    elif mode == "multiple":
        return f"""
            const el = document.querySelector('[data-picker-display="{signal}"]');
            const trigger = document.querySelector('[data-picker-trigger="{signal}"]');
            const selected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : [];
            if (el) {{
                if (selected.length > 0) {{
                    el.textContent = selected.length + ' date' + (selected.length > 1 ? 's' : '') + ' selected';
                    trigger?.setAttribute('data-empty', 'false');
                }} else {{
                    el.textContent = '{placeholder}';
                    trigger?.setAttribute('data-empty', 'true');
                }}
            }}
        """
    else:
        return f"""
            const el = document.querySelector('[data-picker-display="{signal}"]');
            const trigger = document.querySelector('[data-picker-trigger="{signal}"]');
            const selected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : [];
            if (el) {{
                if (selected.length === 2) {{
                    const d1 = new Date(selected[0]);
                    const d2 = new Date(selected[1]);
                    const fmt = {{month: 'short', day: 'numeric', year: 'numeric'}};
                    el.textContent = d1.toLocaleDateString('en-US', fmt) + ' - ' + d2.toLocaleDateString('en-US', fmt);
                    trigger?.setAttribute('data-empty', 'false');
                }} else if (selected.length === 1) {{
                    const d = new Date(selected[0]);
                    el.textContent = d.toLocaleDateString('en-US', {{month: 'short', day: 'numeric', year: 'numeric'}});
                    trigger?.setAttribute('data-empty', 'false');
                }} else {{
                    el.textContent = '{placeholder}';
                    trigger?.setAttribute('data-empty', 'true');
                }}
            }}
        """


def _datetime_display_effect(signal: str, placeholder: str) -> str:
    return f"""
        const el = document.querySelector('[data-picker-display="{signal}"]');
        const trigger = document.querySelector('[data-picker-trigger="{signal}"]');
        const date = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
        const time = document.querySelector('[data-time-input="{signal}"]')?.value || '00:00';

        if (el) {{
            if (date && date !== '') {{
                const d = new Date(date);
                const options = {{year: 'numeric', month: 'long', day: 'numeric'}};
                const dateStr = d.toLocaleDateString('en-US', options);
                el.textContent = `${{dateStr}} at ${{time}}`;
                trigger?.setAttribute('data-empty', 'false');
                {signal}_datetime = `${{date}}T${{time}}:00`;
            }} else {{
                el.textContent = '{placeholder}';
                trigger?.setAttribute('data-empty', 'true');
                {signal}_datetime = '';
            }}
        }}
    """


def _datetime_sync_effect(signal: str, calendar_signal: str) -> str:
    return f"""
        const calSelected = typeof {calendar_signal}_selected !== 'undefined' ? {calendar_signal}_selected : '';
        const pickerSelected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
        if (calSelected !== pickerSelected) {{
            {signal}_selected = calSelected;
        }}

        // Update datetime when time changes
        const timeInput = document.querySelector('[data-time-input="{signal}"]');
        if (timeInput) {{
            const updateDateTime = () => {{
                const date = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
                const time = timeInput.value;
                if (date && time) {{
                    {signal}_time = time;
                    {signal}_datetime = `${{date}}T${{time}}:00`;
                }}
            }};
            timeInput.removeEventListener('change', updateDateTime);
            timeInput.addEventListener('change', updateDateTime);
        }}
    """


def _input_sync_effect(signal: str, calendar_signal: str) -> str:
    return f"""
        // Sync calendar to input
        const calSelected = typeof {calendar_signal}_selected !== 'undefined' ? {calendar_signal}_selected : '';
        const input = document.querySelector('[data-date-input="{signal}"]');
        const pickerSelected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
        if (input && calSelected && calSelected !== pickerSelected) {{
            input.value = calSelected;
            {signal}_selected = calSelected;
        }}

        // Sync input to calendar
        if (input) {{
            const updateCalendar = () => {{
                const value = input.value;
                // Basic date validation (YYYY-MM-DD format)
                if (/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(value)) {{
                    {signal}_selected = value;
                    {calendar_signal}_selected = value;
                }}
            }};
            input.removeEventListener('change', updateCalendar);
            input.addEventListener('change', updateCalendar);
        }}
    """


def _input_close_effect(signal: str) -> str:
    return f"""
        const selected = typeof {signal}_selected !== 'undefined' ? {signal}_selected : '';
        const prevSelected = window['_prev_{signal}_input_selected'];
        if (selected && selected !== prevSelected) {{
            const trigger = document.querySelector('[data-picker-trigger="{signal}"]');
            const popover = trigger?.getAttribute('popovertarget');
            if (popover) {{
                const content = document.getElementById(popover);
                if (content?.matches(':popover-open')) {{
                    content.hidePopover();
                }}
            }}
        }}
        window['_prev_{signal}_input_selected'] = selected;
    """


def _selection_sync_to_calendar(signal: str, calendar_signal: str) -> str:
    """Sync picker selection to calendar (for presets)"""
    return f"""
        // Only run if both signals are defined
        if (typeof {signal}_selected !== 'undefined' && typeof {calendar_signal}_selected !== 'undefined') {{
            // Only sync if not already syncing from calendar
            if (!window._syncingFromCalendar_{signal}) {{
                const pickerSelected = {signal}_selected;
                const calSelected = {calendar_signal}_selected;
                
                // Compare serialized values to avoid unnecessary updates
                const pickerStr = JSON.stringify(pickerSelected);
                const calStr = JSON.stringify(calSelected);
                
                if (pickerStr !== calStr) {{
                    window._syncingToCalendar_{signal} = true;
                    {calendar_signal}_selected = pickerSelected;
                    // Clear flag after next tick
                    setTimeout(() => {{
                        window._syncingToCalendar_{signal} = false;
                    }}, 0);
                }}
            }}
        }}
    """


def _selection_sync_from_calendar(signal: str, calendar_signal: str) -> str:
    """Sync calendar selection to picker"""
    return f"""
        // Only run if both signals are defined
        if (typeof {calendar_signal}_selected !== 'undefined' && typeof {signal}_selected !== 'undefined') {{
            // Only sync if not already syncing to calendar
            if (!window._syncingToCalendar_{signal}) {{
                const calSelected = {calendar_signal}_selected;
                const pickerSelected = {signal}_selected;
                
                // Compare serialized values to avoid unnecessary updates
                const calStr = JSON.stringify(calSelected);
                const pickerStr = JSON.stringify(pickerSelected);
                
                if (calStr !== pickerStr) {{
                    window._syncingFromCalendar_{signal} = true;
                    {signal}_selected = calSelected;
                    // Clear flag after next tick
                    setTimeout(() => {{
                        window._syncingFromCalendar_{signal} = false;
                    }}, 0);
                }}
            }}
        }}
    """


def _calendar_to_picker_handler(
    signal: str, calendar_signal: str, mode: CalendarMode
) -> str:
    """Handle clicks on calendar to update picker signal directly."""
    if mode == "single":
        return f"""
            // Check if click was on a calendar cell
            const cell = evt.target.closest('.cal-cell');
            if (!cell || cell.classList.contains('empty')) return;
            
            // Get the calendar's selected value after it updates
            setTimeout(() => {{
                if (typeof {calendar_signal}_selected !== 'undefined' && typeof {signal}_selected !== 'undefined') {{
                    const calSelected = {calendar_signal}_selected;
                    if (calSelected !== {signal}_selected) {{
                        {signal}_selected = calSelected;
                        
                        // For single mode, close popover immediately after selection
                        const trigger = document.querySelector('[data-picker-trigger="{signal}"][popovertarget]');
                        if (trigger) {{
                            const popoverId = trigger.getAttribute('popovertarget');
                            const content = document.getElementById(popoverId);
                            if (content?.matches(':popover-open')) {{
                                content.hidePopover();
                            }}
                        }}
                    }}
                }}
            }}, 0);
        """
    else:
        return f"""
            // Check if click was on a calendar cell
            const cell = evt.target.closest('.cal-cell');
            if (!cell || cell.classList.contains('empty')) return;
            
            // Get the calendar's selected value after it updates
            setTimeout(() => {{
                if (typeof {calendar_signal}_selected !== 'undefined' && typeof {signal}_selected !== 'undefined') {{
                    const calSelected = {calendar_signal}_selected;
                    const pickerSelected = {signal}_selected;
                    const calStr = JSON.stringify(calSelected);
                    const pickerStr = JSON.stringify(pickerSelected);
                    if (calStr !== pickerStr) {{
                        {signal}_selected = calSelected;
                        
                        // For range mode, close popover when range is complete (2 dates selected)
                        if (Array.isArray(calSelected) && calSelected.length === 2) {{
                            const trigger = document.querySelector('[data-picker-trigger="{signal}"][popovertarget]');
                            if (trigger) {{
                                const popoverId = trigger.getAttribute('popovertarget');
                                const content = document.getElementById(popoverId);
                                if (content?.matches(':popover-open')) {{
                                    content.hidePopover();
                                }}
                            }}
                        }}
                    }}
                }}
            }}, 0);
        """


def _close_on_select_effect(signal: str, mode: CalendarMode) -> str | None:
    if mode == "single":
        return f"""
            // Fallback close mechanism (primary closing is now handled in calendar click)
            if (typeof {signal}_selected !== 'undefined') {{
                const selected = {signal}_selected;
                const prevSelected = window['_prev_{signal}_selected'];
                
                if (selected && selected !== prevSelected) {{
                    // The trigger button has both data-picker-trigger and popovertarget attributes
                    const trigger = document.querySelector('[data-picker-trigger="{signal}"][popovertarget]');
                    if (trigger) {{
                        const popoverId = trigger.getAttribute('popovertarget');
                        const content = document.getElementById(popoverId);
                        if (content?.matches(':popover-open')) {{
                            content.hidePopover();
                        }}
                    }}
                }}
                window['_prev_{signal}_selected'] = selected;
            }}
        """
    elif mode == "range":
        return f"""
            if (typeof {signal}_selected !== 'undefined') {{
                const selected = {signal}_selected;
                const prevSelected = window['_prev_{signal}_selected'] || [];
                if (selected.length === 2 && prevSelected.length !== 2) {{
                    // The trigger button has both data-picker-trigger and popovertarget attributes
                    const trigger = document.querySelector('[data-picker-trigger="{signal}"][popovertarget]');
                    if (trigger) {{
                        const popoverId = trigger.getAttribute('popovertarget');
                        const content = document.getElementById(popoverId);
                        if (content?.matches(':popover-open')) {{
                            content.hidePopover();
                        }}
                    }}
                }}
                window['_prev_{signal}_selected'] = [...selected];
            }}
        """
    else:
        return None
