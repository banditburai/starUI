from typing import Any, Literal

from starhtml import FT, Div, Input, Label, Output, P, Signal, Span

from .utils import cn, gen_id

__metadata__ = {"description": "Slider component for selecting values"}

SliderOrientation = Literal["horizontal", "vertical"]

_THUMB_CLS = (
    "pointer-events-none absolute z-10 size-4 shrink-0 rounded-full"
    " border border-primary bg-white shadow-sm ring-ring/50"
    " transition-[color,box-shadow] group-hover/slider:ring-4 group-has-[:focus]/slider:ring-4"
)

_INPUT_CLS = (
    "absolute inset-0 h-full w-full cursor-pointer appearance-none opacity-0 outline-none"
    " [&::-webkit-slider-thumb]:size-4 [&::-webkit-slider-thumb]:appearance-none"
    " [&::-webkit-slider-thumb]:pointer-events-auto [&::-webkit-slider-thumb]:cursor-pointer"
    " [&::-webkit-slider-thumb]:mt-[-5px]"
    " [&::-moz-range-thumb]:size-4 [&::-moz-range-thumb]:appearance-none"
    " [&::-moz-range-thumb]:pointer-events-auto [&::-moz-range-thumb]:cursor-pointer"
    " [&::-webkit-slider-runnable-track]:h-1.5 [&::-webkit-slider-runnable-track]:border-0 [&::-webkit-slider-runnable-track]:bg-transparent"
    " [&::-moz-range-track]:h-1.5 [&::-moz-range-track]:border-0 [&::-moz-range-track]:bg-transparent"
    " disabled:cursor-not-allowed"
)

_ROOT_CLS = (
    "relative flex grow touch-none items-center select-none group/slider"
    " data-[orientation='horizontal']:h-5"
    " data-[orientation='vertical']:w-5 data-[orientation='vertical']:flex-col"
)

_OUTER_CLS = (
    "flex w-full min-w-0 grow items-center gap-2"
    " data-[orientation='vertical']:flex-col"
    " data-[orientation='vertical']:min-h-44 data-[orientation='vertical']:w-auto"
    " data-[disabled]:cursor-not-allowed data-[disabled]:opacity-50"
)

_VALUE_CLS = "text-sm font-medium text-foreground tabular-nums"


def _pct(val, lo, hi) -> Any:
    if isinstance(val, int | float) and lo == hi:
        return 0.0
    return (val - lo) / (hi - lo) * 100


def _value_output(value, fr: str, suffix: str | None = None, cls: str = _VALUE_CLS) -> FT:
    return Output(
        Span(data_text=value),
        Span(f" {suffix}") if suffix else None,
        fr=fr,
        data_slot="slider-value",
        cls=cls,
    )


def SliderTrack(
    *children,
    orientation: SliderOrientation = "horizontal",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="slider-track",
        cls=cn(
            "relative grow overflow-hidden rounded-full bg-muted",
            "data-[orientation='horizontal']:h-1.5 data-[orientation='horizontal']:w-full",
            "data-[orientation='vertical']:h-full data-[orientation='vertical']:w-1.5",
            cls,
        ),
        data_orientation=orientation,
        **kwargs,
    )


def SliderRange(
    *children,
    orientation: SliderOrientation = "horizontal",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="slider-range",
        cls=cn(
            "absolute bg-primary",
            "data-[orientation='horizontal']:h-full",
            "data-[orientation='vertical']:bottom-0 data-[orientation='vertical']:w-full",
            cls,
        ),
        data_orientation=orientation,
        **kwargs,
    )


def _thumb(orientation: SliderOrientation, ssr_pct: float, signal_expr) -> FT:
    prop, cross, transl = (
        ("bottom", "left: 50%", "-50% 50%") if orientation == "vertical" else ("left", "top: 50%", "-50% -50%")
    )
    return Div(
        data_slot="slider-thumb",
        cls=_THUMB_CLS,
        data_orientation=orientation,
        style=f"{prop}: {ssr_pct}%; {cross}; translate: {transl}",
        **{f"data_style_{prop}": signal_expr},
    )


def Slider(
    value: list[float] | float | None = None,
    default_value: list[float] | float | None = None,
    signal: str | Signal | None = None,
    min: float = 0,
    max: float = 100,
    step: float = 1,
    orientation: SliderOrientation = "horizontal",
    disabled: bool = False,
    name: str | None = None,
    show_value: bool = False,
    value_text: str | list[str] | None = None,
    aria_label: str | None = None,
    cls: str = "",
    id: str | None = None,
    **kwargs,
) -> FT:
    slider_id = id or gen_id("slider")
    sig = getattr(signal, "_id", signal) or slider_id

    raw = value if value is not None else (default_value or min)
    values = raw if isinstance(raw, list) else [raw]

    if len(values) >= 2:
        return RangeSlider(
            value=values if value is not None else None,
            default_value=values if value is None else None,
            signal=signal,
            min=min,
            max=max,
            step=step,
            orientation=orientation,
            disabled=disabled,
            name=name,
            show_value=show_value,
            value_text=value_text,
            aria_label=aria_label,
            cls=cls,
            id=slider_id,
            **kwargs,
        )

    s = Signal(sig, values[0])
    ssr_pct = _pct(values[0], min, max)
    pct_expr = _pct(s, min, max) + "%"

    dim = "height" if orientation == "vertical" else "width"
    range_kwargs = {"style": f"{dim}: {ssr_pct}%", f"data_style_{dim}": pct_expr}
    suffix = value_text[0] if isinstance(value_text, list) else value_text

    return Div(
        s,
        Div(
            SliderTrack(
                SliderRange(orientation=orientation, **range_kwargs),
                orientation=orientation,
            ),
            _thumb(orientation, ssr_pct, pct_expr),
            Input(
                type="range",
                min=str(min),
                max=str(max),
                step=str(step),
                data_bind=s,
                id=slider_id,
                data_slot="slider",
                name=name,
                disabled=disabled or None,
                aria_label=aria_label,
                aria_valuemin=str(min),
                aria_valuemax=str(max),
                data_attr_aria_valuenow=s,
                data_attr_aria_valuetext=(s + f" {suffix}") if suffix else None,
                aria_orientation=orientation,
                data_orientation=orientation,
                cls=_INPUT_CLS,
                style="writing-mode: vertical-lr; direction: rtl" if orientation == "vertical" else None,
                **kwargs,
            ),
            data_slot="slider-root",
            cls=_ROOT_CLS,
            data_orientation=orientation,
        ),
        _value_output(s, slider_id, suffix, cn(_VALUE_CLS, "pointer-events-none min-w-8 text-right select-none"))
        if show_value
        else None,
        data_orientation=orientation,
        data_disabled="true" if disabled else None,
        cls=cn(_OUTER_CLS, cls),
    )


def RangeSlider(
    value: list[float] | None = None,
    default_value: list[float] | None = None,
    signal: str | Signal | None = None,
    min: float = 0,
    max: float = 100,
    step: float = 1,
    orientation: SliderOrientation = "horizontal",
    disabled: bool = False,
    name: str | None = None,
    show_value: bool = False,
    value_text: str | list[str] | None = None,
    aria_label: str | tuple[str, str] | None = None,
    cls: str = "",
    id: str | None = None,
    aria_invalid: str | None = None,
    aria_describedby: str | None = None,
    **kwargs,
) -> FT:
    slider_id = id or gen_id("slider")
    sig = getattr(signal, "_id", signal) or slider_id

    raw = value if value is not None else (default_value or [min, max])
    min_val, max_val = sorted(raw if isinstance(raw, list) and len(raw) >= 2 else [min, max])[:2]

    s_min = Signal(f"{sig}_min", min_val)
    s_max = Signal(f"{sig}_max", max_val)

    ssr_min_pct, ssr_max_pct = _pct(min_val, min, max), _pct(max_val, min, max)
    min_pct, max_pct = _pct(s_min, min, max) + "%", _pct(s_max, min, max) + "%"

    is_vertical = orientation == "vertical"
    pos, dim = ("bottom", "height") if is_vertical else ("left", "width")
    range_pct = (s_max - s_min) / (max - min) * 100 + "%"
    range_kwargs = {
        "style": f"{pos}: {ssr_min_pct}%; {dim}: {ssr_max_pct - ssr_min_pct}%",
        f"data_style_{pos}": min_pct,
        f"data_style_{dim}": range_pct,
    }

    min_label, max_label = (
        (aria_label, aria_label) if isinstance(aria_label, str) else aria_label or ("Minimum value", "Maximum value")
    )
    sfx = [value_text, value_text] if isinstance(value_text, str) else (value_text or [])
    min_suffix, max_suffix = (sfx[0] if sfx else None), (sfx[1] if len(sfx) > 1 else None)

    shared_input = dict(
        type="range",
        min=str(min),
        max=str(max),
        step=str(step),
        data_slot="slider",
        disabled=disabled or None,
        aria_valuemin=str(min),
        aria_valuemax=str(max),
        aria_orientation=orientation,
        data_orientation=orientation,
        cls=cn(_INPUT_CLS, "pointer-events-none"),
        aria_invalid=aria_invalid,
        aria_describedby=aria_describedby,
        style="writing-mode: vertical-lr; direction: rtl" if is_vertical else None,
    )

    return Div(
        s_min,
        s_max,
        Div(
            SliderTrack(
                SliderRange(orientation=orientation, **range_kwargs),
                orientation=orientation,
            ),
            _thumb(orientation, ssr_min_pct, min_pct),
            _thumb(orientation, ssr_max_pct, max_pct),
            Input(
                data_bind=s_min,
                data_on_input=s_min.set(s_min.min(s_max)),
                id=f"{slider_id}-min",
                name=f"{name}_min" if name else None,
                aria_label=min_label,
                data_attr_aria_valuenow=s_min,
                data_attr_aria_valuetext=(s_min + f" {min_suffix}") if min_suffix else None,
                **shared_input,
            ),
            Input(
                data_bind=s_max,
                data_on_input=s_max.set(s_max.max(s_min)),
                id=f"{slider_id}-max",
                name=f"{name}_max" if name else None,
                aria_label=max_label,
                data_attr_aria_valuenow=s_max,
                data_attr_aria_valuetext=(s_max + f" {max_suffix}") if max_suffix else None,
                **shared_input,
            ),
            data_slot="slider-root",
            cls=_ROOT_CLS,
            data_orientation=orientation,
        ),
        Div(
            _value_output(s_min, f"{slider_id}-min", min_suffix),
            Span(" – ", cls="text-muted-foreground"),
            _value_output(s_max, f"{slider_id}-max", max_suffix),
            cls="pointer-events-none min-w-16 text-right select-none",
        )
        if show_value
        else None,
        data_orientation=orientation,
        data_disabled="true" if disabled else None,
        data_slot="range-slider",
        cls=cn(_OUTER_CLS, cls),
        **kwargs,
    )


def SliderWithLabel(
    *children,
    label: str,
    show_value: bool = True,
    disabled: bool = False,
    helper_text: str | None = None,
    error_text: str | None = None,
    cls: str = "",
    label_cls: str = "",
    slider_cls: str = "",
    **kwargs,
) -> FT:
    slider_id = kwargs.pop("id", None) or gen_id("slider")

    vals = v if (v := kwargs.get("value")) is not None else kwargs.get("default_value")
    is_range = isinstance(vals, list) and len(vals) >= 2
    label_for = f"{slider_id}-min" if is_range else slider_id
    desc_id = f"{slider_id}-desc" if error_text or helper_text else None

    return Div(
        *children,
        Label(
            label,
            fr=label_for,
            cls=cn(
                "text-sm font-medium",
                "cursor-pointer" if not disabled else "cursor-not-allowed opacity-50",
                label_cls,
            ),
        ),
        Slider(
            show_value=show_value,
            disabled=disabled,
            id=slider_id,
            cls=slider_cls,
            aria_invalid="true" if error_text else None,
            aria_describedby=desc_id,
            **kwargs,
        ),
        P(error_text, id=desc_id, cls="text-sm text-destructive") if error_text else None,
        P(helper_text, id=desc_id, cls="text-sm text-muted-foreground") if helper_text and not error_text else None,
        data_slot="slider-with-label",
        cls=cn("grid gap-2", cls),
    )
