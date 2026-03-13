from starhtml import FT, Button, Div, Signal

from .utils import cn, gen_id, inject_context, merge_actions

__metadata__ = {"description": "Expandable/collapsible content section"}


def Collapsible(
    *children,
    open: bool = False,
    disabled: bool = False,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("collapsible")
    open_state = Signal(sig, open, ifmissing=not open)
    ctx = {
        "sig": sig,
        "open_state": open_state,
        "is_default_open": open,
        "disabled": disabled,
    }

    return Div(
        open_state,
        *[inject_context(child, **ctx) for child in children],
        data_slot="collapsible",
        data_state="open" if open else "closed",
        data_attr_data_state=open_state.if_("open", "closed"),
        data_disabled="" if disabled else None,
        cls=cls,
        **kwargs,
    )


def CollapsibleTrigger(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, sig, open_state, is_default_open, disabled, **_):
        return Button(
            *children,
            data_on_click=merge_actions(open_state.toggle(), kwargs=kwargs) if not disabled else None,
            type="button",
            id=f"{sig}-trigger",
            data_slot="collapsible-trigger",
            aria_controls=f"{sig}-content",
            aria_expanded="true" if is_default_open else "false",
            data_attr_aria_expanded=open_state.if_("true", "false"),
            data_state="open" if is_default_open else "closed",
            data_attr_data_state=open_state.if_("open", "closed"),
            disabled=disabled,
            cls=cn(
                "cursor-pointer outline-none "
                "focus-visible:rounded-sm focus-visible:ring-[3px] focus-visible:ring-ring/50 "
                "disabled:pointer-events-none disabled:opacity-50",
                cls,
            ),
            **kwargs,
        )

    return _


def CollapsibleContent(
    *children,
    cls: str = "",
    role: str = "region",
    **kwargs,
) -> FT:
    def _(*, sig, open_state, is_default_open, **_):
        return Div(
            Div(
                Div(*children, cls=cls),
                cls="min-h-0 overflow-hidden transition-[visibility] duration-200 [[data-state=closed]_&]:invisible",
            ),
            data_slot="collapsible-content",
            role=role,
            id=f"{sig}-content",
            aria_labelledby=f"{sig}-trigger",
            style="grid-template-rows: 1fr" if is_default_open else "grid-template-rows: 0fr",
            data_state="open" if is_default_open else "closed",
            cls="grid transition-[grid-template-rows] duration-200 ease-out",
            data_attr_style=open_state.if_("grid-template-rows: 1fr", "grid-template-rows: 0fr"),
            data_attr_data_state=open_state.if_("open", "closed"),
            **kwargs,
        )

    return _
