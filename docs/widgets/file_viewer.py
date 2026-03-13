import hashlib
import re

from starhtml import Div, FT, Icon, Signal, Span
from components.code_block import CodeBlock as BaseCodeBlock
from components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from components.utils import cn
from .copy_button import CopyButton

_CODE_CLS = "!border-none !bg-transparent !rounded-none"
_CONTAINER_CLS = "bg-muted/30 border border-border rounded-lg overflow-hidden"


def _traffic_lights() -> FT:
    return Div(
        Span(cls="size-2.5 rounded-full bg-[#ff5f57]"),
        Span(cls="size-2.5 rounded-full bg-[#febc2e]"),
        Span(cls="size-2.5 rounded-full bg-[#28c840]"),
        cls="flex gap-1.5 items-center px-3 shrink-0",
    )


def _make_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def FileViewer(
    files: list[dict[str, str]],
    *,
    signal: str = "",
    cls: str = "",
    **attrs,
) -> FT:
    """Editor-chrome code viewer with traffic lights, file tabs, and copy button.

    Args:
        files: List of {"name": "filename.py", "content": "..."} dicts.
        signal: Optional signal name for active tab state.
        cls: Additional CSS classes for the outer container.
    """
    if not files:
        return Div("No files provided.", cls="text-muted-foreground p-4")

    combined = "|".join(f["name"] for f in files)
    sig_name = signal or f"fv_{hashlib.md5(combined.encode()).hexdigest()[:8]}"
    slugs = [_make_slug(f["name"]) for f in files]
    multi = len(files) > 1

    # One reference for tab-state visibility (only used in multi-file mode)
    tab_state = Signal(sig_name, slugs[0]) if multi else None

    copy_signals = []
    copy_buttons = []
    for f, slug in zip(files, slugs):
        code_id = f"fv_code_{sig_name}_{slug}"
        copied = Signal(f"fv_cp_{sig_name}_{slug}", False)
        copy_signals.append(copied)
        btn = CopyButton(code_id, copied, variant="embedded")
        if multi:
            btn = Div(btn, data_show=tab_state == slug)
        copy_buttons.append(btn)

    copy_area = Div(*copy_buttons, cls="ml-auto px-2 shrink-0 flex items-center")

    if multi:
        triggers = [
            TabsTrigger(
                Icon("lucide:file-code-2", cls="size-3 shrink-0 opacity-60"),
                f["name"],
                id=slug,
                cls="font-mono text-xs font-normal rounded-none flex-none h-9 px-3 border-r border-border/50",
            )
            for f, slug in zip(files, slugs)
        ]

        contents = [
            TabsContent(
                BaseCodeBlock(f["content"], "python", id=f"fv_code_{sig_name}_{slug}", cls=_CODE_CLS),
                id=slug,
                cls="mt-0 max-h-[600px] overflow-y-auto",
            )
            for f, slug in zip(files, slugs)
        ]

        return Div(
            *copy_signals,
            Tabs(
                TabsList(
                    _traffic_lights(),
                    *triggers,
                    copy_area,
                    cls="h-auto rounded-none bg-muted/50 p-0 w-full justify-start gap-0 border-b border-border",
                ),
                *contents,
                variant="line",
                signal=sig_name,
                cls="w-full",
            ),
            cls=cn(_CONTAINER_CLS, cls),
            **attrs,
        )

    f, slug = files[0], slugs[0]
    code_id = f"fv_code_{sig_name}_{slug}"

    return Div(
        *copy_signals,
        Div(
            _traffic_lights(),
            Span(f["name"], cls="text-xs font-mono text-muted-foreground truncate"),
            copy_area,
            cls="flex items-center bg-muted/50 h-9 border-b border-border",
        ),
        Div(
            BaseCodeBlock(f["content"], "python", id=code_id, cls=_CODE_CLS),
            cls="max-h-[600px] overflow-y-auto",
        ),
        cls=cn(_CONTAINER_CLS, cls),
        **attrs,
    )
