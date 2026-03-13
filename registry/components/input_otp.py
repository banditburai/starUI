from starhtml import FT, Div, Icon, Signal, Style, js, set_timeout
from starhtml import Input as HTMLInput
from starhtml.datastar import evt

from .utils import cn, gen_id, inject_context

__metadata__ = {"description": "One-time password input"}

REGEXP_ONLY_DIGITS = r"\d"
REGEXP_ONLY_CHARS = r"a-zA-Z"
REGEXP_ONLY_DIGITS_AND_CHARS = r"a-zA-Z0-9"

_OTP_STYLES = """\
@keyframes caret-blink {
  0%, 70%, 100% { opacity: 1 }
  20%, 50% { opacity: 0 }
}
.animate-caret-blink { animation: caret-blink 1.25s ease-out infinite }
[data-slot=input-otp-slot]:not(:focus-within) [data-slot=input-otp-caret] { display: none !important }
@media (prefers-reduced-motion: reduce) {
  .animate-caret-blink { animation: none }
}
"""


def InputOTP(
    *children,
    max_length: int = 6,
    value: str = "",
    signal: str | Signal = "",
    allow: str | None = REGEXP_ONLY_DIGITS,
    input_mode: str = "numeric",
    disabled: bool = False,
    name: str | None = None,
    autocomplete: str = "one-time-code",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("input_otp")

    slot_signals = [Signal(f"{sig}_{i}", value[i] if i < len(value) else "", ifmissing=True) for i in range(max_length)]
    slot_refs = [Signal(f"{sig}_{i}_ref", _ref_only=True) for i in range(max_length)]
    otp = Signal(sig, value, ifmissing=not value)

    aria_invalid = kwargs.pop("aria_invalid", None)
    aria_describedby = kwargs.pop("aria_describedby", None)

    ctx = {
        "sig": sig,
        "slot_signals": slot_signals,
        "slot_refs": slot_refs,
        "max_length": max_length,
        "allow": allow,
        "input_mode": input_mode,
        "disabled": disabled,
        "autocomplete": autocomplete,
        "aria_invalid": aria_invalid,
        "aria_describedby": aria_describedby,
    }

    return Div(
        Style(_OTP_STYLES),
        otp,
        HTMLInput(type="hidden", name=name, data_bind=otp) if name else None,
        *slot_signals,
        *[inject_context(child, **ctx) for child in children],
        data_slot="input-otp",
        data_disabled="" if disabled else None,
        cls=cn("flex items-center gap-2 has-[:disabled]:opacity-50", cls),
        **kwargs,
    )


def InputOTPGroup(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="input-otp-group",
            cls=cn("flex items-center", cls),
            **kwargs,
        )

    return _


def InputOTPSlot(
    index: int,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(
        *,
        sig,
        slot_signals,
        slot_refs,
        max_length,
        allow,
        input_mode,
        disabled,
        autocomplete,
        aria_invalid,
        aria_describedby,
        **_,
    ):
        slot_sig, slot_ref = slot_signals[index], slot_refs[index]
        s = f"${sig}_{index}"
        sync_composite = f"${sig} = {' + '.join(f'${sig}_{i}' for i in range(max_length))}"

        next_ref = f"${sig}_{index + 1}_ref" if index < max_length - 1 else None
        prev_ref = f"${sig}_{index - 1}_ref" if index > 0 else None

        replace = f"{s}.replace(/[^{allow}]/g, '')" if allow else s
        advance = (
            f"if ({s}.length > 0) {{ {next_ref}.focus(); {next_ref}.select() }}" if next_ref else "evt.target.select()"
        )
        input_handler = js(f"{s} = {replace}.slice(0, 1); {sync_composite}; {advance}")

        keydown_handler = js(
            "; ".join(
                [
                    "if (evt.isComposing || evt.keyCode === 229) return",
                    *(
                        [
                            f"if (evt.key.length === 1 && !evt.ctrlKey && !evt.metaKey && !/[{allow}]/.test(evt.key)) "
                            f"{{ evt.preventDefault() }}"
                        ]
                        if allow
                        else []
                    ),
                    *(
                        [
                            f"if (evt.key === 'Backspace' && {s}.length === 0) "
                            f"{{ evt.preventDefault(); {prev_ref}.focus(); {prev_ref}.select() }}",
                            f"if (evt.key === 'ArrowLeft') "
                            f"{{ evt.preventDefault(); {prev_ref}.focus(); {prev_ref}.select() }}",
                        ]
                        if prev_ref
                        else []
                    ),
                    *(
                        [
                            f"if (evt.key === 'ArrowRight') "
                            f"{{ evt.preventDefault(); {next_ref}.focus(); {next_ref}.select() }}"
                        ]
                        if next_ref
                        else []
                    ),
                ]
            )
        )

        focus_routing = "; ".join(f"if (fi === {i}) ${sig}_{i}_ref.focus()" for i in range(index, max_length))
        paste_handler = js(
            "; ".join(
                [
                    "evt.preventDefault()",
                    "let t = (evt.clipboardData || window.clipboardData).getData('text')",
                    *([f"t = t.replace(/[^{allow}]/g, '')"] if allow else []),
                    f"let chars = t.slice(0, {max_length - index}).split('')",
                    *(f"${sig}_{i} = chars[{i - index}] || ''" for i in range(index, max_length)),
                    sync_composite,
                    f"let fi = Math.min({index} + chars.length, {max_length - 1}); {focus_routing}",
                ]
            )
        )

        char_label = "Digit" if allow == REGEXP_ONLY_DIGITS else "Character"

        return Div(
            slot_ref,
            HTMLInput(
                type="text",
                data_bind=slot_sig,
                data_ref=slot_ref,
                maxlength="1",
                inputmode=input_mode,
                autocomplete=autocomplete if index == 0 else "off",
                disabled=disabled or None,
                data_on_input=input_handler,
                data_on_keydown=keydown_handler,
                data_on_paste=paste_handler,
                data_on_focus=set_timeout(evt.target.select(), 0),
                data_on_mouseup=evt.target.select(),
                aria_invalid=aria_invalid,
                aria_describedby=aria_describedby if index == 0 else None,
                aria_label=f"{char_label} {index + 1} of {max_length}",
                data_slot="input-otp-input",
                cls="absolute inset-0 h-full w-full bg-transparent text-center "
                "border-0 text-sm shadow-none outline-none "
                "[caret-color:transparent] selection:bg-transparent "
                "disabled:cursor-not-allowed",
            ),
            Div(
                Div(cls="h-4 w-px bg-foreground animate-caret-blink"),
                data_slot="input-otp-caret",
                cls="pointer-events-none absolute inset-0 flex items-center justify-center",
                data_show=slot_sig.length.eq(0),
            ),
            data_slot="input-otp-slot",
            data_attr_data_filled=(slot_sig.length > 0),
            cls=cn(
                "relative flex size-9 items-center justify-center",
                "border-y border-r border-input text-sm shadow-xs transition-all",
                "first:rounded-l-md first:border-l last:rounded-r-md",
                "dark:bg-input/30",
                "has-[:focus]:z-10 has-[:focus]:border-ring has-[:focus]:ring-[3px] has-[:focus]:ring-ring/50",
                "aria-[invalid=true]:border-destructive aria-[invalid=true]:ring-destructive/20 "
                "has-[:focus]:aria-[invalid=true]:border-destructive "
                "has-[:focus]:aria-[invalid=true]:ring-destructive/20 "
                "dark:has-[:focus]:aria-[invalid=true]:ring-destructive/40",
                cls,
            ),
            **kwargs,
        )

    return _


def InputOTPSeparator(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    def _(**_):
        return Div(
            *(children or (Icon("lucide:minus"),)),
            role="separator",
            data_slot="input-otp-separator",
            cls=cn("flex items-center", cls),
            **kwargs,
        )

    return _
