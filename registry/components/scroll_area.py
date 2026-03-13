from typing import Literal

from starhtml import FT, Div, Script, Style

from .utils import cn, gen_id

__metadata__ = {"description": "Scrollable viewport with styled scrollbars"}

_SCROLL_AREA_BASE_STYLES = """
[data-slot="scroll-area-viewport"]{scrollbar-width:thin;scrollbar-color:var(--color-border) transparent}
[data-slot="scroll-area-viewport"]::-webkit-scrollbar{width:10px;height:10px}
[data-slot="scroll-area-viewport"]::-webkit-scrollbar-track{background:transparent}
[data-slot="scroll-area-viewport"]::-webkit-scrollbar-thumb{background-color:var(--color-border);background-clip:content-box;border:2px solid transparent;border-radius:9999px}
[data-slot="scroll-area-viewport"]::-webkit-scrollbar-corner{background:transparent}
[data-scroll-area-hidden="true"]::-webkit-scrollbar{width:0;height:0}
[data-scroll-area-hidden="true"]::-webkit-scrollbar-track{background:transparent}
[data-scroll-area-hidden="true"]::-webkit-scrollbar-thumb{background:transparent;border:0}
[data-scroll-area-hidden="true"]{scrollbar-color:transparent transparent;-ms-overflow-style:none;scrollbar-width:none}
[data-scroll-area-hidden="true"] *{overflow:hidden !important}
[data-scroll-area-hidden="true"]::-webkit-scrollbar{display:none}
[data-slot="scroll-area-corner"]{position:absolute;right:0;bottom:0;height:10px;width:10px;background:transparent}
[data-slot="scroll-area-corner"][data-dir="rtl"]{right:auto;left:0}
"""

_OVERFLOW_CLASSES = {
    "vertical": "overflow-x-hidden overflow-y-auto",
    "horizontal": "overflow-x-auto overflow-y-hidden",
    "both": "overflow-auto",
}

_AUTO_HIDE_SCRIPT = (
    "(function(){const v=document.getElementById('%s');"
    "if(!v)return;let h;const d=%d,"
    "s=()=>{clearTimeout(h);v.setAttribute('data-scroll-area-hidden','false')},"
    "x=()=>{clearTimeout(h);h=setTimeout(()=>v.setAttribute('data-scroll-area-hidden','true'),d)};"
    "'mouseenter mousemove wheel touchstart touchmove pointerenter pointerdown focus'.split(' ').forEach(e=>v.addEventListener(e,s));"
    "'mouseleave pointerleave blur'.split(' ').forEach(e=>v.addEventListener(e,x));"
    "v.addEventListener('scroll',()=>{s();x()});"
    "v.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','PageUp','PageDown','Home','End'].includes(e.key))s()});"
    "x()})()"
)


def ScrollArea(
    *children,
    orientation: Literal["vertical", "horizontal", "both"] = "vertical",
    dir: Literal["ltr", "rtl"] = "ltr",
    auto_hide: bool = False,
    scroll_hide_delay: int = 600,
    aria_label: str | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    viewport_id = f"{gen_id('scroll')}_viewport"

    return Div(
        Style(_SCROLL_AREA_BASE_STYLES),
        Div(
            *children,
            data_slot="scroll-area-viewport",
            id=viewport_id,
            tabindex="0",
            dir=dir,
            role="region",
            aria_label=aria_label or "Scrollable content",
            cls=cn("size-full rounded-[inherit]", _OVERFLOW_CLASSES[orientation]),
        ),
        Div(data_slot="scroll-area-corner", data_dir=dir) if orientation == "both" else None,
        Script(_AUTO_HIDE_SCRIPT % (viewport_id, scroll_hide_delay)) if auto_hide else None,
        data_slot="scroll-area",
        cls=cn("relative", cls),
        **kwargs,
    )
