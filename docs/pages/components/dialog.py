"""
Dialog component documentation — Native HTML dialog with modal and non-modal support.
"""

TITLE = "Dialog"
DESCRIPTION = "A modal dialog component using the native HTML dialog element for accessibility and performance."
CATEGORY = "overlay"
ORDER = 40
STATUS = "stable"

from starhtml import Div, P, H3, Icon, Signal
from starui.registry.components.dialog import (
    Dialog, DialogTrigger, DialogContent, DialogHeader, DialogFooter,
    DialogTitle, DialogDescription, DialogClose
)
from starui.registry.components.button import Button
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def edit_profile_example():
    return Dialog(
        DialogTrigger("Edit Profile", variant="outline"),
        DialogContent(
            DialogHeader(
                DialogTitle("Edit Profile"),
                DialogDescription("Update your display name and email address.")
            ),
            Div(
                InputWithLabel(label="Name", placeholder="Ada Lovelace", signal="profile_name"),
                InputWithLabel(label="Email", type="email", placeholder="ada@example.com", signal="profile_email"),
                cls="space-y-4 py-4"
            ),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                DialogClose("Save Changes")
            )
        )
    )


@with_code
def confirmation_example():
    return Dialog(
        DialogTrigger(
            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
            "Delete Account",
            variant="destructive"
        ),
        DialogContent(
            DialogHeader(
                DialogTitle("Are you absolutely sure?"),
                DialogDescription(
                    "This action cannot be undone. This will permanently delete your "
                    "account and remove your data from our servers."
                )
            ),
            Div(
                Icon("lucide:alert-triangle", cls="h-5 w-5 text-destructive shrink-0 mt-0.5"),
                P(
                    "All projects, files, and collaborator access will be permanently removed.",
                    cls="text-sm text-muted-foreground"
                ),
                cls="flex gap-3 py-4"
            ),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                DialogClose("Delete Account", variant="destructive", value="delete")
            )
        )
    )


@with_code
def scrollable_content_example():
    sections = [
        ("1. Acceptance of Terms", "By accessing and using this service, you accept and agree to be bound by these terms."),
        ("2. Use License", "Permission is granted to temporarily download one copy of the materials for personal, non-commercial viewing only."),
        ("3. Disclaimer", "Materials are provided on an 'as is' basis with no warranties, expressed or implied."),
        ("4. Limitations", "In no event shall we be liable for any damages arising from the use or inability to use our service."),
        ("5. Privacy", "Our privacy policy explains how we collect, use, and protect your data."),
        ("6. Termination", "We reserve the right to terminate accounts that violate these terms."),
    ]

    return Dialog(
        DialogTrigger("View Terms", variant="outline"),
        DialogContent(
            terms_accepted := Signal("terms_accepted", False),
            DialogHeader(
                DialogTitle("Terms of Service"),
                DialogDescription("Please review our terms before continuing")
            ),
            Div(
                *[Div(H3(title, cls="font-semibold mb-1"), P(body, cls="text-sm text-muted-foreground mb-4")) for title, body in sections],
                cls="max-h-[300px] overflow-y-auto py-4 px-4 my-4 border rounded-md"
            ),
            CheckboxWithLabel(label="I have read and agree to the terms", signal=terms_accepted),
            DialogFooter(
                DialogClose("Decline", variant="outline"),
                DialogClose("Accept", data_attr_disabled=~terms_accepted)
            )
        ),
        size="lg"
    )


@with_code
def sizes_example():
    sizes = [
        ("sm", "Small", "Compact confirmations and brief messages."),
        ("md", "Medium", "Standard forms and notifications."),
        ("lg", "Large", "Multi-section forms and detailed content."),
        ("xl", "Extra Large", "Data tables, comparisons, or complex layouts."),
    ]
    return Div(
        *[
            Dialog(
                DialogTrigger(label, variant="outline", size="sm"),
                DialogContent(
                    DialogHeader(
                        DialogTitle(label),
                        DialogDescription(desc)
                    ),
                    DialogFooter(DialogClose("Close"))
                ),
                size=size
            )
            for size, label, desc in sizes
        ],
        cls="flex flex-wrap gap-2"
    )


@with_code
def non_modal_example():
    return Dialog(
        DialogTrigger("Open Non-Modal", variant="outline"),
        DialogContent(
            DialogHeader(
                DialogTitle("Non-Modal Dialog"),
                DialogDescription(
                    "No backdrop, no focus trap — the page behind stays fully interactive."
                )
            ),
            P(
                "Try clicking outside this dialog. It stays open without blocking the page.",
                cls="text-sm text-muted-foreground py-4"
            ),
            DialogFooter(DialogClose("Dismiss"))
        ),
        modal=False
    )


@with_code
def programmatic_example():
    dialog_ref = Signal("prog_dialog", _ref_only=True)
    is_open = Signal("prog_dialog_open", False)

    return Div(
        is_open,
        Button(
            "Open via Signal",
            variant="outline",
            data_on_click=[dialog_ref.showModal(), is_open.set(True)]
        ),
        P(
            data_text=is_open.if_("Dialog is open", "Dialog is closed"),
            cls="text-sm text-muted-foreground mt-2"
        ),
        Dialog(
            DialogContent(
                DialogHeader(
                    DialogTitle("Signal-Controlled"),
                    DialogDescription("Opened programmatically without a DialogTrigger.")
                ),
                DialogFooter(DialogClose("Done")),
                show_close_button=False
            ),
            signal="prog_dialog"
        )
    )


EXAMPLES_DATA = [
    {
        "title": "Edit Profile",
        "description": "Standard dialog with form fields, header/footer layout, and a built-in close button. DialogClose handles both 'Cancel' and 'Save Changes' exit paths.",
        "fn": edit_profile_example,
    },
    {
        "title": "Confirmation",
        "description": "Destructive action with a warning and two exit paths. The delete button passes value='delete' to DialogClose so the close event carries the user's intent.",
        "fn": confirmation_example,
    },
    {
        "title": "Scrollable Content",
        "description": "Long content in a scrollable container with a checkbox-gated accept button. Uses size='lg' for breathing room and data_attr_disabled to block acceptance until checked.",
        "fn": scrollable_content_example,
    },
    {
        "title": "Sizes",
        "description": "Four width variants from compact (sm) to spacious (xl). All sizes cap at max-h-[85vh] and add horizontal margin on mobile via max-w-[calc(100%-2rem)].",
        "fn": sizes_example,
    },
    {
        "title": "Non-Modal",
        "description": "Set modal=False to skip the backdrop overlay and focus trap. The dialog stays open while users interact with the page — useful for persistent panels or side information.",
        "fn": non_modal_example,
    },
    {
        "title": "Programmatic Control",
        "description": "Open a dialog via signal reference instead of DialogTrigger — useful for custom logic or external events. The open state is tracked reactively. show_close_button=False removes the corner X.",
        "fn": programmatic_example,
    },
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("signal", "str | Signal", "Signal ID for the dialog element ref and open state tracking", "''"),
        Prop("modal", "bool", "Whether the dialog blocks page interaction with a backdrop overlay", "True"),
        Prop("size", "DialogSize", "Width variant — 'sm', 'md', 'lg', 'xl', or 'full'", "'md'"),
    ],
    components=[
        Component("DialogTrigger", "Button that opens the dialog on click"),
        Component("DialogContent", "Content container with optional close button (show_close_button=True)"),
        Component("DialogHeader", "Flex column for title and description"),
        Component("DialogTitle", "Dialog heading rendered as H2"),
        Component("DialogDescription", "Muted supporting text below the title"),
        Component("DialogFooter", "Right-aligned footer for action buttons"),
        Component("DialogClose", "Button that closes the dialog, with optional return value"),
    ]
)


def create_dialog_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
