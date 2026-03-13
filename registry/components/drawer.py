from typing import Literal

from starhtml import FT, Div, Icon, P, Signal, Span, Style, js
from starhtml import H2 as HTMLH2
from starhtml import Dialog as HTMLDialog
from starhtml.datastar import document, evt, seq

from .utils import cn, gen_id, inject_context, merge_actions

__metadata__ = {"description": "Draggable drawer panel"}

DrawerDirection = Literal["top", "right", "bottom", "left"]

_DRAG_CONFIG = {
    "bottom": ("Y", 1),
    "top": ("Y", -1),
    "right": ("X", 1),
    "left": ("X", -1),
}

_DRAWER_STYLES = """
dialog[data-drawer]{
  --_dur-in:500ms;--_dur-out:500ms;--_ease:cubic-bezier(0.32,0.72,0,1);
  position:fixed;margin:0;max-height:none;z-index:50;
  transition:translate var(--_dur-out) var(--_ease),display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-drawer][open]{transition-duration:var(--_dur-in)}
dialog[data-drawer]:not([open]){display:none}
dialog[data-drawer]::backdrop{
  background:rgb(0 0 0/.5);
  transition:background var(--_dur-out) var(--_ease),display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-drawer]:not([open])::backdrop{background:rgb(0 0 0/0)}
dialog[data-drawer="right"]{inset:0 0 0 auto}
dialog[data-drawer="right"]:not([open]){translate:100% 0}
dialog[data-drawer="right"][open]{@starting-style{translate:100% 0}}
dialog[data-drawer="left"]{inset:0 auto 0 0}
dialog[data-drawer="left"]:not([open]){translate:-100% 0}
dialog[data-drawer="left"][open]{@starting-style{translate:-100% 0}}
dialog[data-drawer="top"]{inset:0 0 auto 0;max-width:none}
dialog[data-drawer="top"]:not([open]){translate:0 -100%}
dialog[data-drawer="top"][open]{@starting-style{translate:0 -100%}}
dialog[data-drawer="bottom"]{inset:auto 0 0 0;max-width:none}
dialog[data-drawer="bottom"]:not([open]){translate:0 100%}
dialog[data-drawer="bottom"][open]{@starting-style{translate:0 100%}}
dialog[data-drawer][open]::backdrop{@starting-style{background:rgb(0 0 0/0)}}
@media(prefers-reduced-motion:reduce){dialog[data-drawer],dialog[data-drawer]::backdrop{transition-duration:0ms!important}}
"""

_DISMISS_THRESHOLD = 100


def _render_handle(sig, direction):
    axis, sign = _DRAG_CONFIG[direction]
    ds, dy, dg = f"${sig}_ds", f"${sig}_dy", f"${sig}_dg"
    clamp = "Math.max(0,raw)" if sign > 0 else "Math.min(0,raw)"

    if direction in ("top", "bottom"):
        bar_cls = "h-1.5 w-12 rounded-full bg-muted-foreground/20"
        container_cls = "flex cursor-grab touch-none justify-center py-3 select-none active:cursor-grabbing"
    else:
        bar_cls = "h-12 w-1.5 rounded-full bg-muted-foreground/20"
        container_cls = (
            "flex cursor-grab touch-none items-center justify-center px-3 select-none active:cursor-grabbing"
        )

    return Div(
        Div(cls=bar_cls),
        data_on_pointerdown=js(
            f"{ds}=evt.client{axis};{dy}=0;{dg}=1;evt.currentTarget.setPointerCapture(evt.pointerId)"
        ),
        data_on_pointermove=js(f"if({dg}){{var raw=evt.client{axis}-{ds};{dy}={clamp}}}"),
        data_on_pointerup=js(
            f"if({dg}){{var wasDelta=Math.abs({dy});{dg}=0;{dy}=0;"
            f"if(wasDelta>{_DISMISS_THRESHOLD}){{evt.currentTarget.closest('dialog').close()}}}}"
        ),
        data_on_pointercancel=js(f"if({dg}){{{dg}=0;{dy}=0}}"),
        aria_hidden="true",
        data_slot="drawer-handle",
        cls=container_cls,
    )


def Drawer(
    *children,
    signal: str | Signal = "",
    modal: bool = True,
    default_open: bool = False,
    dismissible: bool = True,
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("drawer")
    drawer_open = Signal(f"{sig}_open", default_open)
    dialog_ref = Signal(sig, _ref_only=True)

    trigger = next((c for c in children if getattr(c, "__name__", None) == "trigger"), None)
    content = next((c for c in children if getattr(c, "__name__", None) == "content"), None)

    direction = getattr(content, "_direction", "bottom")
    show_handle = getattr(content, "_show_handle", True)
    content_cls = getattr(content, "_cls", "")
    content_kwargs = getattr(content, "_kwargs", {})

    ctx = {
        "sig": sig,
        "drawer_open": drawer_open,
        "dialog_ref": dialog_ref,
        "modal": modal,
        "dismissible": dismissible,
    }

    direction_cls = {
        "right": "h-full w-3/4 border-l sm:max-w-sm",
        "left": "h-full w-3/4 border-r sm:max-w-sm",
        "top": "mx-auto w-full max-w-lg rounded-b-xl border-b",
        "bottom": "mx-auto w-full max-w-lg rounded-t-xl border-t",
    }[direction]

    show_action = dialog_ref.showModal() if modal else dialog_ref.show()

    drag_style_attrs = {}
    if show_handle and dismissible:
        dy = f"${sig}_dy"
        translate_js = f"'0 '+{dy}+'px'" if direction in ("top", "bottom") else f"{dy}+'px 0'"
        drag_style_attrs["data_style_translate"] = js(f"${sig}_dg ? {translate_js} : ''")
        drag_style_attrs["data_style_transition"] = js(f"${sig}_dg ? 'none' : ''")

    return Div(
        Style(_DRAWER_STYLES),
        drawer_open,
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=drawer_open.set(False),
            data_on_click=(evt.target == evt.currentTarget).then(seq(dialog_ref.close(), drawer_open.set(False)))
            if modal and dismissible
            else None,
            data_drawer=direction,
            id=f"{sig}_content",
            aria_labelledby=f"{sig}_content-title",
            aria_describedby=f"{sig}_content-description",
            cls=cn(
                "bg-background bg-clip-padding text-foreground shadow-lg",
                "flex flex-col gap-0 p-0 outline-none",
                direction_cls,
                "overflow-y-auto",
                content_cls,
            ),
            **drag_style_attrs,
            **content_kwargs,
        ),
        Div(
            data_effect=[
                (drawer_open & ~dialog_ref.open).then(show_action),
                (~drawer_open & dialog_ref.open).then(dialog_ref.close()),
            ],
            style="display: none;",
        ),
        Div(
            data_effect=document.body.style.overflow.set(drawer_open.if_("hidden", "")),
            style="display: none;",
        )
        if modal
        else None,
        cls=cls,
        **kwargs,
    )


def DrawerTrigger(
    *children,
    variant: str = "outline",
    cls: str = "",
    **kwargs,
) -> FT:
    def trigger(*, sig, drawer_open, dialog_ref, modal, **_):
        from .button import Button

        return Button(
            *children,
            data_on_click=merge_actions(
                dialog_ref.showModal() if modal else dialog_ref.show(), drawer_open.set(True), kwargs=kwargs
            ),
            id=f"{sig}_trigger",
            data_attr_aria_expanded=drawer_open.if_("true", "false"),
            aria_haspopup="dialog",
            aria_controls=f"{sig}_content",
            data_slot="drawer-trigger",
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return trigger


def DrawerContent(
    *children,
    direction: DrawerDirection = "bottom",
    show_close: bool = False,
    show_handle: bool | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    _show_handle = show_handle if show_handle is not None else (direction == "bottom")

    def content(*, sig, drawer_open, dialog_ref, dismissible, **ctx):
        all_ctx = dict(sig=sig, drawer_open=drawer_open, dialog_ref=dialog_ref, dismissible=dismissible, **ctx)
        return Div(
            _render_handle(sig, direction) if _show_handle and dismissible else None,
            DrawerClose(
                Icon("lucide:x", cls="size-4"),
                Span("Close", cls="sr-only"),
                size="icon",
                cls="absolute top-4 right-4 opacity-70 transition-opacity hover:opacity-100",
            )(**all_ctx)
            if show_close
            else None,
            *[inject_context(child, **all_ctx) for child in children],
            cls="relative flex flex-1 flex-col",
        )

    content._direction = direction
    content._show_handle = _show_handle
    content._cls = cls
    content._kwargs = kwargs
    return content


def DrawerClose(
    *children,
    variant: str = "ghost",
    size: str = "sm",
    cls: str = "",
    **kwargs,
) -> FT:
    def _(*, drawer_open, dialog_ref, **_):
        from .button import Button

        return Button(
            *children,
            data_on_click=merge_actions(kwargs=kwargs, after=[drawer_open.set(False), dialog_ref.close()]),
            data_slot="drawer-close",
            variant=variant,
            size=size,
            cls=cls,
            **kwargs,
        )

    return _


def DrawerHeader(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="drawer-header",
            cls=cn("flex flex-col gap-1.5 p-4", cls),
            **kwargs,
        )

    return _


def DrawerFooter(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="drawer-footer",
            cls=cn("mt-auto flex flex-col gap-2 p-4", cls),
            **kwargs,
        )

    return _


def DrawerTitle(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sig, **_):
        return HTMLH2(
            *children,
            id=f"{sig}_content-title",
            data_slot="drawer-title",
            cls=cn("font-semibold text-foreground", cls),
            **kwargs,
        )

    return _


def DrawerDescription(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sig, **_):
        return P(
            *children,
            id=f"{sig}_content-description",
            data_slot="drawer-description",
            cls=cn("text-sm text-muted-foreground", cls),
            **kwargs,
        )

    return _
