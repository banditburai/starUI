TITLE = "Input OTP"
DESCRIPTION = "One-time password input with individual character slots. Accepts digits only by default."
CATEGORY = "form"
ORDER = 12
STATUS = "stable"

from starhtml import Div, Form, P, Signal, Span

from components.button import Button
from components.input_otp import (
    InputOTP,
    InputOTPGroup,
    InputOTPSeparator,
    InputOTPSlot,
)
from utils import Component, Prop, auto_generate_page, build_api_reference, with_code


@with_code
def hero_input_otp_example():
    return InputOTP(
        InputOTPGroup(
            InputOTPSlot(0),
            InputOTPSlot(1),
            InputOTPSlot(2),
        ),
        InputOTPSeparator(),
        InputOTPGroup(
            InputOTPSlot(3),
            InputOTPSlot(4),
            InputOTPSlot(5),
        ),
    )


@with_code
def alphanumeric_example():
    from components.input_otp import REGEXP_ONLY_DIGITS_AND_CHARS

    return InputOTP(
        InputOTPGroup(
            InputOTPSlot(0),
            InputOTPSlot(1),
            InputOTPSlot(2),
        ),
        InputOTPSeparator(),
        InputOTPGroup(
            InputOTPSlot(3),
            InputOTPSlot(4),
            InputOTPSlot(5),
        ),
        value="A3F",
        allow=REGEXP_ONLY_DIGITS_AND_CHARS,
        input_mode="text",
    )


@with_code
def disabled_example():
    return InputOTP(
        InputOTPGroup(
            InputOTPSlot(0),
            InputOTPSlot(1),
            InputOTPSlot(2),
            InputOTPSlot(3),
            InputOTPSlot(4),
            InputOTPSlot(5),
        ),
        value="123",
        disabled=True,
    )


@with_code
def controlled_example():
    otp = Signal("otp_ctrl", "42")  #: hide
    return Div(
        otp,  #: hide
        InputOTP(
            InputOTPGroup(
                InputOTPSlot(0),
                InputOTPSlot(1),
                InputOTPSlot(2),
            ),
            InputOTPSeparator(),
            InputOTPGroup(
                InputOTPSlot(3),
                InputOTPSlot(4),
                InputOTPSlot(5),
            ),
            value="42",
            signal=otp,
        ),
        P(
            "Entered: ",
            Span(data_text=otp, cls="font-mono font-medium tracking-widest"),
            cls="text-sm text-muted-foreground mt-3",
        ),
    )


@with_code
def form_example():
    return Form(
        P("Enter the code sent to your email", cls="text-sm text-muted-foreground"),
        InputOTP(
            InputOTPGroup(
                InputOTPSlot(0),
                InputOTPSlot(1),
                InputOTPSlot(2),
                InputOTPSlot(3),
                InputOTPSlot(4),
                InputOTPSlot(5),
            ),
            name="otp",
        ),
        Button("Verify", type="submit", cls="w-fit"),
        cls="space-y-4",
    )


EXAMPLES_DATA = [
    {"fn": hero_input_otp_example},
    {
        "fn": alphanumeric_example,
        "title": "Alphanumeric",
        "description": "Accepts both letters and digits instead of digits only.",
    },
    {
        "fn": disabled_example,
        "title": "Disabled",
        "description": "Pre-filled partial value with disabled state.",
    },
    {
        "fn": controlled_example,
        "title": "Controlled",
        "description": "Signal-bound input with reactive display of the entered value.",
    },
    {
        "fn": form_example,
        "title": "Form",
        "description": "Inside a form with name attribute for submission.",
    },
]


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("max_length", "int", "Maximum number of characters", "6"),
        Prop("value", "str", "Initial OTP value", "''"),
        Prop("signal", "str | Signal", "Datastar signal name for reactive binding", "auto-generated"),
        Prop("allow", "str | None", "Regex character class for input filtering (e.g. r'\\d' for digits). None disables filtering", "REGEXP_ONLY_DIGITS"),
        Prop("input_mode", "str", "Mobile keyboard type (numeric, text, etc.)", "'numeric'"),
        Prop("disabled", "bool", "Disables the input", "False"),
        Prop("name", "str | None", "Form field name for submission", "None"),
        Prop("autocomplete", "str", "Autocomplete hint for the browser", "'one-time-code'"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ],
    components=[
        Component("InputOTP", "Root container with hidden input and signal management"),
        Component("InputOTPGroup", "Groups slots with shared borders (passthrough closure)"),
        Component("InputOTPSlot", "Displays a single character at the given index with caret animation (closure). Requires index: int"),
        Component("InputOTPSeparator", "Visual divider between groups. Defaults to a minus icon, override with *children"),
    ],
)


def create_input_otp_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
