"""
AlertDialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

TITLE = "Alert Dialog"
DESCRIPTION = "A modal dialog that interrupts the user with important content and expects a response."
CATEGORY = "overlay"
ORDER = 45
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Code, Ul, Li, Signal, js, get, Strong
from starui.registry.components.alert_dialog import (
    AlertDialog, AlertDialogTrigger, AlertDialogContent,
    AlertDialogHeader, AlertDialogFooter, AlertDialogTitle,
    AlertDialogDescription, AlertDialogAction, AlertDialogCancel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.input import InputWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from starui.registry.components.utils import cn
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview




@with_code
def hero_alert_dialog_example():
    return AlertDialog(
        AlertDialogTrigger("Delete Item", variant="destructive"),
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Are you absolutely sure?"),
                AlertDialogDescription(
                    "This action cannot be undone. This will permanently delete your item and remove it from our servers."
                )
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction("Delete", variant="destructive")
            )
        )
    )


@with_code
def basic_alert_dialog_example():
    return AlertDialog(
        AlertDialogTrigger("Show Alert"),
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Heads up!"),
                AlertDialogDescription(
                    "This is an important message that requires your attention."
                )
            ),
            AlertDialogFooter(
                AlertDialogCancel("Dismiss"),
                AlertDialogAction("Understood")
            )
        )
    )


@with_code
def destructive_alert_dialog_example():
        deletion_items = [
            "All source code and version history",
            "Issues, pull requests, and comments",
            "Wiki pages and project settings",
            "All collaborator associations"
        ]
        
        danger_info = Div(
            P("Delete Repository", cls="font-medium"),
            P("Once deleted, it will be gone forever",
              cls="text-sm text-muted-foreground mt-1"),
            cls="flex-1"
        )

        dialog_content = AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle(
                    Icon("lucide:alert-triangle", cls="h-6 w-6 mr-2 text-destructive"),
                    "Delete Repository"
                ),
                AlertDialogDescription(
                    "This action cannot be undone. This will permanently delete the repository and all of its contents."
                )
            ),
            Div(
                P("The following will be deleted:", cls="text-sm font-medium mb-2"),
                Ul(
                    *[Li(item, cls="text-sm text-muted-foreground") for item in deletion_items],
                    cls="list-disc list-inside space-y-1"
                ),
                cls="py-4"
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction("Delete Repository", variant="destructive")
            )
        )

        return Card(
            CardHeader(
                CardTitle("Danger Zone"),
                CardDescription("Irreversible actions")
            ),
            CardContent(
                Div(
                    danger_info,
                    AlertDialog(
                        AlertDialogTrigger(
                            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                            "Delete",
                            variant="destructive",
                            size="sm"
                        ),
                        dialog_content
                    ),
                    cls="flex items-end justify-between gap-6 p-6 border rounded-lg"
                )
            ),
            cls="max-w-lg"
        )


@with_code
def unsaved_changes_alert_dialog_example():
    return Card(
        (doc_title := Signal("doc_title", "My Document")),
        (doc_author := Signal("doc_author", "John Doe")),

        CardHeader(
            CardTitle("Document Editor"),
            CardDescription("Edit your document details")
        ),
        CardContent(
            Div(
                InputWithLabel(
                    label="Document Title",
                    value="My Document",
                    signal=doc_title
                ),
                InputWithLabel(
                    label="Author",
                    value="John Doe",
                    signal=doc_author,
                    cls="mt-4"
                ),
                P("Make changes to the document fields above and try to save.",
                  cls="text-sm text-muted-foreground italic mt-4")
            ),
            Div(
                AlertDialog(
                    AlertDialogTrigger("Save & Exit"),
                    AlertDialogContent(
                        AlertDialogHeader(
                            AlertDialogTitle("Save changes?"),
                            AlertDialogDescription("You have unsaved changes. What would you like to do?")
                        ),
                        Div(
                            Div(
                                Icon("lucide:save", cls="h-4 w-4 mr-2 text-blue-500"),
                                P("Your changes:", cls="text-sm font-medium"),
                                cls="flex items-center mb-2"
                            ),
                            Div(
                                P("Title: ", Span(data_text=doc_title, cls="font-mono"), cls="text-sm"),
                                P("Author: ", Span(data_text=doc_author, cls="font-mono"), cls="text-sm"),
                                cls="space-y-1 p-3 bg-muted rounded-md"
                            ),
                            cls="py-6"
                        ),
                        AlertDialogFooter(
                            AlertDialogAction(
                                "Discard Changes",
                                variant="destructive",
                                action=[
                                    doc_title.set("My Document"),
                                    doc_author.set("John Doe")
                                ]
                            ),
                            AlertDialogCancel("Keep Editing"),
                            AlertDialogAction("Save & Exit")
                        )
                    )
                ),
                cls="mt-4"
            )
        ),
        cls="max-w-md"
    )


@with_code
def session_timeout_alert_dialog_example():
    session_time = Signal("session_time", 15)
    logged_in = Signal("logged_in", False)
    timer_active = Signal("timer_active", False)

    reset_actions = [
        logged_in.set(False),
        timer_active.set(False),
        session_time.set(15)
    ]

    start_session_actions = [
        logged_in.set(True),
        session_time.set(15),
        timer_active.set(True)
    ]

    progress_bar = Div(
        Div(
            data_attr_style="width: " + (session_time / 15) * 100 + "%",
            cls="h-2 bg-orange-500 rounded-full transition-all duration-1000"
        ),
        cls="w-full bg-secondary rounded-full h-2 mt-2"
    )

    session_display = Div(
        P("Logged in as: user@example.com", cls="text-sm font-medium mb-2"),
        P(
            "Session expires in: ",
            Span(data_text=session_time, cls="font-mono font-bold text-lg"),
            " seconds",
            cls="text-sm"
        ),
        progress_bar,
        Button("Logout", data_on_click=reset_actions, variant="outline", size="sm", cls="mt-4"),
        data_show=logged_in,
        cls="space-y-2"
    )

    timer_effect = Div(
        data_effect=js("""
            if ($timer_active && $logged_in) {
                const timer = setInterval(() => {
                    if (!$timer_active || !$logged_in) {
                        clearInterval(timer);
                        return;
                    }
                    $session_time--;
                    if ($session_time === 5) $timeout_dialog?.showModal();
                    if ($session_time <= 0) {
                        clearInterval(timer);
                        $timeout_dialog?.close();
                        $logged_in = false;
                        $timer_active = false;
                        $session_time = 15;
                    }
                }, 1000);
                return () => clearInterval(timer);
            }
        """)
    )

    timeout_dialog = AlertDialog(
        AlertDialogContent(
            Icon("lucide:clock", cls="h-12 w-12 text-orange-500 mx-auto mb-4"),
            AlertDialogHeader(
                AlertDialogTitle("Session Expiring Soon"),
                AlertDialogDescription(
                    "Your session will expire in ",
                    Span(data_text=session_time, cls="font-bold text-orange-500"),
                    " seconds. Do you want to continue?"
                )
            ),
            AlertDialogFooter(
                AlertDialogAction("Logout Now", variant="destructive", action=reset_actions),
                AlertDialogAction("Continue Session", action=session_time.set(15))
            )
        ),
        signal="timeout_dialog"
    )

    return Div(
        Card(
            session_time,
            logged_in,
            timer_active,
            CardHeader(
                CardTitle("Session Management"),
                CardDescription("Auto-logout demonstration with warning")
            ),
            CardContent(
                Div(
                    Button("Login", data_on_click=start_session_actions, variant="default"),
                    data_show=~logged_in
                ),
                session_display,
                timer_effect,
                timeout_dialog
            ),
            cls="w-full max-w-lg"
        ),
        cls="w-full max-w-2xl"
    )


@with_code
def batch_operation_alert_dialog_example():
    files = [
        {"name": "file1.txt", "checked": True},
        {"name": "file2.pdf", "checked": True},
        {"name": "file3.jpg", "checked": False},
        {"name": "file4.doc", "checked": True},
    ]

    selected = Signal("batch_selected", [i for i, f in enumerate(files) if f["checked"]])
    visible = Signal("batch_visible", list(range(len(files))))

    file_checkboxes = [
        Div(
            CheckboxWithLabel(
                label=f["name"],
                checked=f["checked"],
                data_on_change=selected.toggle_in(i)
            ),
            data_show=visible.contains(i)
        )
        for i, f in enumerate(files)
    ]

    dialog_items = [
        Li(f["name"], data_show=selected.contains(i), cls="text-sm text-muted-foreground")
        for i, f in enumerate(files)
    ]

    delete_action = js("$batch_visible = $batch_visible.filter(v => !$batch_selected.includes(v)); $batch_selected = []")

    selection_count = P(
        Span(data_text=selected.length, cls="font-bold"),
        " items selected",
        cls="text-sm text-muted-foreground"
    )

    delete_dialog = AlertDialog(
        AlertDialogTrigger(
            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
            "Delete Selected",
            variant="destructive",
            data_attr_disabled=selected.length.eq(0)
        ),
        AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Delete Multiple Items"),
                AlertDialogDescription(
                    "You are about to delete ",
                    Span(data_text=selected.length, cls="font-bold text-destructive"),
                    " items. This action cannot be undone."
                )
            ),
            Div(
                P("The following items will be deleted:", cls="text-sm font-medium mb-2"),
                Ul(*dialog_items, cls="list-disc list-inside space-y-1"),
                cls="py-4"
            ),
            AlertDialogFooter(
                AlertDialogCancel("Cancel"),
                AlertDialogAction(
                    data_text="Delete " + selected.length + " Items",
                    variant="destructive",
                    action=delete_action
                )
            )
        )
    )

    return Card(
        selected,
        visible,
        CardHeader(
            CardTitle("Batch Operations"),
            CardDescription("Confirm actions on multiple items")
        ),
        CardContent(
            Div(*file_checkboxes, cls="space-y-2"),
            Div(selection_count, delete_dialog, cls="flex items-center gap-4 mt-4")
        ),
        cls="max-w-md"
    )


@with_code
def payment_confirmation_alert_dialog_example():
    def order_line(label, value, extra_cls=""):
        return Div(
            P(label, cls="text-sm text-muted-foreground"),
            P(value, cls="font-medium"),
            cls=cn("flex justify-between py-2", extra_cls)
        )
    
    order_summary = Div(
        order_line("Product:", "Premium Plan"),
        order_line("Price:", "$99.00"),
        order_line("Tax:", "$9.90", "border-b"),
        Div(
            P("Total:", cls="font-medium"),
            P("$108.90", cls="text-xl font-bold"),
            cls="flex justify-between py-2"
        )
    )
    
    security_badge = Div(
        Div(
            Icon("lucide:lock", cls="h-4 w-4 text-green-500"),
            P("Secure Payment", cls="text-sm font-medium"),
            cls="flex items-center gap-2"
        ),
        P("Your payment information is encrypted and secure", 
          cls="text-xs text-muted-foreground mt-1"),
        cls="p-3 bg-green-50 dark:bg-green-950/20 rounded-md mb-4"
    )
    
    payment_details = Div(
        P("Amount to charge: ", Span("$108.90", cls="font-bold text-lg")),
        P("Card ending in: ", Span("****4242", cls="font-mono")),
        cls="space-y-2"
    )
    
    return Card(
        CardHeader(
            CardTitle("Complete Purchase"),
            CardDescription("Review your order")
        ),
        CardContent(
            order_summary,
            AlertDialog(
                AlertDialogTrigger(
                    Icon("lucide:credit-card", cls="h-4 w-4 mr-2"),
                    "Complete Purchase",
                    cls="w-full"
                ),
                AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle(
                            Icon("lucide:shield-check", cls="h-6 w-6 mr-2 text-green-500"),
                            "Confirm Payment"
                        ),
                        AlertDialogDescription("Please review and confirm your purchase")
                    ),
                    Div(security_badge, payment_details, cls="py-4"),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction("Confirm Payment")
                    )
                )
            )
        ),
        cls="max-w-sm"
    )



EXAMPLES_DATA = [
    {"fn": hero_alert_dialog_example, "title": "Hero Alert Dialog", "description": "Confirmation dialog with destructive action"},
    {"fn": basic_alert_dialog_example, "title": "Basic Alert Dialog", "description": "Simple alert dialog with dismiss and confirm actions"},
    {"fn": destructive_alert_dialog_example, "title": "Destructive Action", "description": "Delete confirmation with detailed information"},
    {"fn": unsaved_changes_alert_dialog_example, "title": "Unsaved Changes", "description": "Prompt user about unsaved changes before exiting"},
    {"fn": session_timeout_alert_dialog_example, "title": "Session Timeout", "description": "Auto-triggered alert with countdown timer"},
    {"fn": batch_operation_alert_dialog_example, "title": "Batch Operations", "description": "Confirm actions on multiple selected items"},
    {"fn": payment_confirmation_alert_dialog_example, "title": "Payment Confirmation", "description": "Secure payment confirmation with order details"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("AlertDialog", "Container for alert dialog functionality"),
        Component("AlertDialogTrigger", "Button or element that opens the dialog"),
        Component("AlertDialogContent", "Main dialog content container"),
        Component("AlertDialogHeader", "Header section with title and description"),
        Component("AlertDialogTitle", "Dialog title text"),
        Component("AlertDialogDescription", "Dialog description or message"),
        Component("AlertDialogFooter", "Footer with action buttons"),
        Component("AlertDialogAction", "Primary action button (e.g., Confirm, Delete)"),
        Component("AlertDialogCancel", "Cancel/dismiss button"),
    ]
)



def create_alert_dialog_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)