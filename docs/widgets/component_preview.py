import hashlib
from starhtml import FT, Div, P, H3, Iframe, Signal
from starui.registry.components.tabs import Tabs, TabsContent, TabsList, TabsTrigger
from starui.registry.components.code_block import CodeBlock as BaseCodeBlock
from starui.registry.components.utils import cn
from .copy_button import CopyButton

IFRAME_PREVIEW_REGISTRY = {}

def ComponentPreview(
    preview_content: FT,
    code_content: str,
    *,
    title: str | None = None,
    description: str | None = None,
    preview_class: str = "",
    copy_button: bool = True,
    default_tab: str = "preview",
    preview_id: str | None = None,
    include_imports: bool = True,
    use_iframe: bool = False,
    iframe_height: str = "400px",
    **attrs,
) -> FT:
    if include_imports and not code_content.strip().startswith(('from starhtml import', 'from starui import')):
        code_content = f"from starhtml import *\nfrom starui import *\n\n{code_content}"
    
    preview_id = preview_id or f"preview_{hashlib.md5(code_content.encode()).hexdigest()[:8]}"

    header = (
        Div(
            H3(title, cls="text-lg font-semibold mt-6") if title else None,
            P(description, cls="text-sm text-muted-foreground mt-1") if description else None,
            cls="mb-3"
        ) if title or description else None
    )

    if use_iframe:
        IFRAME_PREVIEW_REGISTRY[preview_id] = {'content': preview_content, 'class': preview_class}
        preview_component = Div(
            Iframe(
                src=f"/component-preview-iframe/{preview_id}",
                id=f"iframe_{preview_id}",
                cls="w-full border-0 rounded-lg bg-background",
                style=f"height: {iframe_height};",
                sandbox="allow-scripts allow-same-origin",  # Datastar reactivity & localStorage
                loading="lazy"
            ),
            cls="w-full"
        )
    else:
        preview_component = Div(
            preview_content,
            cls=cn("flex min-h-[200px] w-full items-center justify-center p-10", preview_class),
        )

    copied_signal_name = f"copied_{preview_id}"

    return Div(
        copy_button and (copied := Signal(copied_signal_name, False)),
        header,
        Div(
            Tabs(
                TabsList(
                    TabsTrigger("Preview", id="preview"),
                    TabsTrigger("Code", id="code"),
                ),
                TabsContent(
                    preview_component,
                    id="preview",
                    cls="mt-2"
                ),
                TabsContent(
                    Div(
                        BaseCodeBlock(
                            code_content,
                            language="python",
                            id=preview_id,
                            cls="max-h-[650px] overflow-auto",
                            style="scrollbar-width: thin;"
                        ),
                        CopyButton(preview_id, copied, variant="group-hover") if copy_button else None,
                        cls="relative group overflow-x-auto"
                    ),
                    id="code",
                    cls="mt-2 overflow-x-auto min-w-0 max-w-full"
                ),
                value=default_tab,
                signal=f"{preview_id}_tab",
                cls="w-full min-w-0"
            ),
            cls="rounded-lg border p-6 min-w-0 overflow-hidden",
        ),
        cls=cn("relative mb-8 w-full", attrs.get("cls", "")),
        **{k: v for k, v in attrs.items() if k != "cls"},
    )