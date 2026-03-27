from typing import Literal

from starhtml import FT, Div, Li, P, Signal, Span, Ul
from starhtml import Fieldset as HTMLFieldset
from starhtml import Label as HTMLLabel
from starhtml import Legend as HTMLLegend

from .separator import Separator
from .utils import cn, inject_context, with_signals

__metadata__ = {"description": "Accessible form field composition", "dependencies": ["separator"]}

_FIELD_ORIENTATION = {
    "vertical": "flex-col [&>*]:w-full [&>.sr-only]:w-auto",
    "horizontal": (
        "flex-row items-center [&>[data-slot=field-label]]:flex-auto"
        " has-[>[data-slot=field-content]]:items-start"
        " has-[>[data-slot=field-content]]:[&>[role=checkbox],[role=radio]]:mt-px"
    ),
    "responsive": (
        "flex-col @md/field-group:flex-row @md/field-group:items-center"
        " [&>*]:w-full @md/field-group:[&>*]:w-auto [&>.sr-only]:w-auto"
        " @md/field-group:[&>[data-slot=field-label]]:flex-auto"
        " @md/field-group:has-[>[data-slot=field-content]]:items-start"
        " @md/field-group:has-[>[data-slot=field-content]]:[&>[role=checkbox],[role=radio]]:mt-px"
    ),
}

_DISABLED_FIELD = "group-data-[disabled=true]/field:pointer-events-none group-data-[disabled=true]/field:opacity-50"


def Field(
    *children,
    name: str | None = None,
    orientation: Literal["vertical", "horizontal", "responsive"] = "vertical",
    invalid: bool | Signal | None = None,
    validate=None,
    signal: Signal | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    field_signal = None
    if validate is not None and name:
        field_signal = signal or Signal(name.replace("-", "_"), "")
        fn, *rest = validate if isinstance(validate, tuple) else (validate,)
        kw = rest.pop() if rest and isinstance(rest[-1], dict) else {}
        field_signal.validate(fn, *rest, **kw)
        invalid = field_signal.err

    children = tuple(inject_context(child, name=name, signal=field_signal) for child in children)
    if name and (
        inp := next(
            (c for c in children if isinstance(c, FT) and c.tag in {"input", "textarea"} and not c.get("id")), None
        )
    ):
        inp.list[2] |= {"id": name, "aria-describedby": f"{name}-desc {name}-error"}
        if field_signal:
            for k, v in field_signal._validate_html.items():
                inp.list[2].setdefault(k, v)

    result = Div(
        field_signal,  # .err auto-included by ft_datastar for validated signals
        *children,
        role="group",
        data_slot="field",
        data_orientation=orientation,
        data_invalid="true" if invalid is True else None,
        data_attr_data_invalid=invalid.if_("true") if isinstance(invalid, Signal) else None,
        cls=cn(
            "flex w-full gap-2 group/field",
            "data-[invalid=true]:text-destructive",
            _FIELD_ORIENTATION[orientation],
            cls,
        ),
        **kwargs,
    )
    return with_signals(result, signal=field_signal) if field_signal else result


def FieldSet(*children, cls: str = "", **kwargs) -> FT:
    return HTMLFieldset(
        *(inject_context(child) for child in children),
        data_slot="field-set",
        cls=cn(
            "flex flex-col gap-4 border-none p-0",
            "has-[>[data-slot=checkbox-group]]:gap-3",
            "has-[>[data-slot=radio-group]]:gap-3",
            cls,
        ),
        **kwargs,
    )


def FieldLegend(
    *children,
    variant: Literal["legend", "label"] = "legend",
    cls: str = "",
    **kwargs,
) -> FT:
    return HTMLLegend(
        *children,
        data_slot="field-legend",
        data_variant=variant,
        cls=cn("mb-1.5 font-medium", "data-[variant=legend]:text-base", "data-[variant=label]:text-sm", cls),
        **kwargs,
    )


def FieldGroup(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="field-group",
        cls=cn(
            "@container/field-group flex w-full flex-col gap-5 group/field-group",
            "data-[slot=checkbox-group]:gap-3",
            "[&>[data-slot=field-group]]:gap-4",
            cls,
        ),
        **kwargs,
    )


def FieldContent(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="field-content",
        cls=cn("flex min-w-0 flex-1 flex-col gap-0.5 leading-snug group/field-content", cls),
        **kwargs,
    )


def FieldLabel(*children, fr: str | None = None, cls: str = "", **kwargs):
    def _(*, name=None, **_):
        return HTMLLabel(
            *children,
            data_slot="field-label",
            fr=fr or name or None,
            cls=cn(
                "flex min-w-0 items-center gap-2 text-sm font-medium select-none",
                "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
                "group/field-label peer/field-label w-fit leading-snug",
                _DISABLED_FIELD,
                "has-[>[data-slot=field]]:w-full has-[>[data-slot=field]]:flex-col",
                "has-[>[data-slot=field]]:rounded-lg has-[>[data-slot=field]]:border",
                "[&>*]:data-[slot=field]:p-2.5",
                "has-data-[state=checked]:border-primary/30 has-data-[state=checked]:bg-primary/5",
                "dark:has-data-[state=checked]:border-primary/20 dark:has-data-[state=checked]:bg-primary/10",
                cls,
            ),
            **kwargs,
        )

    return _


def FieldTitle(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="field-label",
        cls=cn(
            "flex w-fit min-w-0 items-center gap-2 text-sm leading-snug font-medium",
            _DISABLED_FIELD,
            cls,
        ),
        **kwargs,
    )


def FieldDescription(*children, cls: str = "", **kwargs):
    def _(*, name=None, **_):
        return P(
            *children,
            data_slot="field-description",
            id=f"{name}-desc" if name else None,
            cls=cn(
                "min-w-0 text-sm leading-normal font-normal break-words text-muted-foreground",
                "group-has-[[data-orientation=horizontal]]/field:text-balance",
                "last:mt-0 nth-last-2:-mt-1 [[data-variant=legend]+&]:-mt-1.5",
                "[&>a]:underline [&>a]:underline-offset-4 [&>a:hover]:text-primary",
                cls,
            ),
            **kwargs,
        )

    return _


def FieldSeparator(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        Separator(cls="absolute inset-0 top-1/2"),
        Span(
            *children,
            data_slot="field-separator-content",
            cls="relative mx-auto block w-fit bg-background px-2 text-muted-foreground",
        )
        if children
        else None,
        data_slot="field-separator",
        data_content="true" if children else None,
        cls=cn("relative -my-2 h-5 text-sm", "group-data-[variant=outline]/field-group:-mb-2", cls),
        **kwargs,
    )


def FieldError(*children, signal: Signal | None = None, errors: list | None = None, cls: str = "", **kwargs):
    _user_signal = signal

    def _(*, name=None, signal=None, **_kw):
        sig = _user_signal if _user_signal is not None else signal
        if not children and errors == []:
            return None
        cs = children
        if not cs and errors:
            errs = list(dict.fromkeys(errors))
            cs = (errs[0],) if len(errs) == 1 else (Ul(*(Li(e) for e in errs), cls="list-disc pl-4"),)
        err = sig and sig.err
        return Div(
            *cs,
            data_slot="field-error",
            role="alert",
            id=f"{name}-error" if name else None,
            data_text=err,
            data_show=err,
            cls=cn("min-w-0 text-sm font-normal break-words text-destructive", cls),
            **kwargs,
        )

    return _
