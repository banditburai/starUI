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
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def basic_alert_dialog_example():
    dialog_content = AlertDialogContent(
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

    return AlertDialog(
        AlertDialogTrigger("Show Alert"),
        dialog_content,
        signal="basic_alert"
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
                    Icon("lucide:alert-triangle", width="24", height="24", 
                         cls="mr-2 text-destructive"),
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
                AlertDialogAction(
                    "Delete Repository",
                    variant="destructive"
                )
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
                        dialog_content,
                        signal="delete_repo"
                    ),
                    cls="flex items-end justify-between gap-6 p-6 border rounded-lg"
                )
            ),
            cls="max-w-lg"
        )


@with_code
def unsaved_changes_alert_dialog_example():
    return Card(            
        (doc_title := Signal("doc_title", "My Document", _ref_only=True)),
        (doc_author := Signal("doc_author", "John Doe", _ref_only=True)),

        CardHeader(
            CardTitle("Document Editor"),
            CardDescription("Edit your document details")
        ),
        CardContent(
            Div(
                InputWithLabel(
                    label="Document Title",
                    value="My Document",                    
                ),
                InputWithLabel(
                    label="Author",
                    value="John Doe",                    
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
    return Div(
        Card(
            (session_time := Signal("session_time", 15)),
            (logged_in := Signal("logged_in", False)),
            (timer_active := Signal("timer_active", False)),

            CardHeader(
                CardTitle("Session Management"),
                CardDescription("Auto-logout demonstration with warning")
            ),
            CardContent(
                Div(
                    Button(
                        "Login",
                        data_on_click=[
                            logged_in.set(True),
                            session_time.set(15),
                            timer_active.set(True)
                        ],
                        variant="default"
                    ),
                    data_show=~logged_in
                ),

                Div(
                    P("Logged in as: user@example.com", cls="text-sm font-medium mb-2"),
                    P(
                        "Session expires in: ",
                        Span(data_text=session_time, cls="font-mono font-bold text-lg"),
                        " seconds",
                        cls="text-sm"
                    ),

                    Div(
                        Div(
                            data_attr_style="width: " + (session_time / 15) * 100 + "%",
                            cls="h-2 bg-orange-500 rounded-full transition-all duration-1000"
                        ),
                        cls="w-full bg-secondary rounded-full h-2 mt-2"
                    ),

                    Button(
                        "Logout",
                        data_on_click=[
                            logged_in.set(False),
                            timer_active.set(False),
                            session_time.set(15)
                        ],
                        variant="outline",
                        size="sm",
                        cls="mt-4"
                    ),
                    data_show=logged_in,
                    cls="space-y-2"
                ),

                Div(
                    data_effect=js("""
                        if ($timer_active && $logged_in) {
                            const timer = setInterval(() => {
                                if (!$timer_active || !$logged_in) {
                                    clearInterval(timer);
                                    return;
                                }

                                $session_time = Math.max(0, $session_time - 1);

                                if ($session_time === 5) {
                                    document.getElementById('timeout_dialog')?.showModal();
                                }

                                if ($session_time === 0) {
                                    clearInterval(timer);
                                    document.getElementById('timeout_dialog')?.close();
                                    $logged_in = false;
                                    $timer_active = false;
                                    $session_time = 15;
                                }
                            }, 1000);

                            return () => clearInterval(timer);
                        }
                    """)
                ),

                AlertDialog(
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
                            AlertDialogAction(
                                "Logout Now",
                                variant="destructive",
                                action=[
                                    logged_in.set(False),
                                    timer_active.set(False),
                                    session_time.set(15)
                                ]
                            ),
                            AlertDialogAction(
                                "Continue Session",
                                action=session_time.set(15)
                            )
                        )
                    ),
                    signal="timeout_dialog"  # Needed for programmatic opening via JS
                )
            ),
            cls="w-full max-w-lg"
        ),
        cls="w-full max-w-2xl"
    )


@with_code
def batch_operation_alert_dialog_example():
    return Card(
        # Define all signals inline where they're collected
        (file1 := Signal("file1", True, _ref_only=True)),
        (file2 := Signal("file2", True, _ref_only=True)),
        (file3 := Signal("file3", False, _ref_only=True)),
        (file4 := Signal("file4", True, _ref_only=True)),
        (file1_exists := Signal("file1_exists", True)),
        (file2_exists := Signal("file2_exists", True)),
        (file3_exists := Signal("file3_exists", True)),
        (file4_exists := Signal("file4_exists", True)),

        CardHeader(
            CardTitle("Batch Operations"),
            CardDescription("Confirm actions on multiple items")
        ),
        CardContent(
            Div(
                Div(
                    Div(
                        CheckboxWithLabel(label="file1.txt", signal=file1, checked=True),
                        data_show=file1_exists
                    ),
                    Div(
                        CheckboxWithLabel(label="file2.pdf", signal=file2, checked=True),
                        data_show=file2_exists
                    ),
                    Div(
                        CheckboxWithLabel(label="file3.jpg", signal=file3, checked=False),
                        data_show=file3_exists
                    ),
                    Div(
                        CheckboxWithLabel(label="file4.doc", signal=file4, checked=True),
                        data_show=file4_exists
                    ),
                    cls="space-y-2"
                ),

                Div(
                    P(
                        Span(data_text=js("[$file1, $file2, $file3, $file4].filter(Boolean).length"), cls="font-bold"),
                        " items selected",
                        cls="text-sm text-muted-foreground"
                    ),
                    AlertDialog(
                        AlertDialogTrigger(
                            Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                            "Delete Selected",
                            variant="destructive",
                            data_attr_disabled=~(file1 | file2 | file3 | file4)
                        ),
                        AlertDialogContent(
                            AlertDialogHeader(
                                AlertDialogTitle("Delete Multiple Items"),
                                AlertDialogDescription(
                                    "You are about to delete ",
                                    Span(
                                        data_text=js("[$file1, $file2, $file3, $file4].filter(Boolean).length"),
                                        cls="font-bold text-destructive"
                                    ),
                                    " items. This action cannot be undone."
                                )
                            ),
                            Div(
                                P("The following items will be deleted:", cls="text-sm font-medium mb-2"),
                                Ul(
                                    Li("file1.txt", data_show=file1, cls="text-sm text-muted-foreground"),
                                    Li("file2.pdf", data_show=file2, cls="text-sm text-muted-foreground"),
                                    Li("file3.jpg", data_show=file3, cls="text-sm text-muted-foreground"),
                                    Li("file4.doc", data_show=file4, cls="text-sm text-muted-foreground"),
                                    cls="list-disc list-inside space-y-1"
                                ),
                                cls="py-4"
                            ),
                            AlertDialogFooter(
                                AlertDialogCancel("Cancel"),
                                AlertDialogAction(
                                    data_text=js("'Delete ' + [$file1, $file2, $file3, $file4].filter(Boolean).length + ' Items'"),
                                    variant="destructive",
                                    action=js("""
                                        if($file1) { $file1_exists=false; $file1=false; }
                                        if($file2) { $file2_exists=false; $file2=false; }
                                        if($file3) { $file3_exists=false; $file3=false; }
                                        if($file4) { $file4_exists=false; $file4=false; }
                                    """)
                                )
                            )
                        )
                    ),
                    cls="flex items-center gap-4 mt-4"
                ),
                cls="space-y-2"
            )
        ),
        cls="max-w-md"
    )


@with_code
def payment_confirmation_alert_dialog_example():
    def order_line(label, value, extra_cls=""):
        return Div(
            P(label, cls="text-sm text-muted-foreground"),
            P(value, cls="font-medium"),
            cls=f"flex justify-between py-2 {extra_cls}".strip()
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
    
    dialog_content = AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle(
                Icon("lucide:shield-check", width="24", height="24", 
                     cls="mr-2 text-green-500"),
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
                dialog_content
            )
        ),
        cls="max-w-sm"
    )


@with_code
def hero_alert_dialog_example():
    dialog_content = AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle("Are you absolutely sure?"),
            AlertDialogDescription(
                "This action cannot be undone. This will permanently delete your item and remove it from our servers."
            )
        ),
        AlertDialogFooter(
            AlertDialogCancel("Cancel"),
            AlertDialogAction(
                "Delete",
                variant="destructive"
            )
        )
    )

    return AlertDialog(
        AlertDialogTrigger(
            "Delete Item",
            variant="destructive"
        ),
        dialog_content
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        basic_alert_dialog_example(),
        basic_alert_dialog_example.code,
        title="Basic Alert",
        description="Simple informational alert with single action"
    )

    yield ComponentPreview(
        destructive_alert_dialog_example(),
        destructive_alert_dialog_example.code,
        title="Destructive Action",
        description="High-risk action with clear warnings and consequences"
    )

    yield ComponentPreview(
        unsaved_changes_alert_dialog_example(),
        unsaved_changes_alert_dialog_example.code,
        title="Unsaved Changes",
        description="Three-option dialog for handling unsaved work"
    )

    yield ComponentPreview(
        session_timeout_alert_dialog_example(),
        session_timeout_alert_dialog_example.code,
        title="Session Timeout",
        description="Auto-triggered alert with countdown timer"
    )

    yield ComponentPreview(
        batch_operation_alert_dialog_example(),
        batch_operation_alert_dialog_example.code,
        title="Batch Operations",
        description="Confirm actions on multiple selected items"
    )

    yield ComponentPreview(
        payment_confirmation_alert_dialog_example(),
        payment_confirmation_alert_dialog_example.code,
        title="Payment Confirmation",
        description="Secure payment confirmation with trust indicators"
    )


# ============================================================================
# MODULE EXPORTS (for markdown generation)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Alert", "description": "Simple informational alert with single action", "code": basic_alert_dialog_example.code},
    {"title": "Destructive Action", "description": "High-risk action with clear warnings and consequences", "code": destructive_alert_dialog_example.code},
    {"title": "Unsaved Changes", "description": "Three-option dialog for handling unsaved work", "code": unsaved_changes_alert_dialog_example.code},
    {"title": "Session Timeout", "description": "Auto-triggered alert with countdown timer", "code": session_timeout_alert_dialog_example.code},
    {"title": "Batch Operations", "description": "Confirm actions on multiple selected items", "code": batch_operation_alert_dialog_example.code},
    {"title": "Payment Confirmation", "description": "Secure payment confirmation with trust indicators", "code": payment_confirmation_alert_dialog_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("AlertDialog", "Main container component that manages dialog state"),
        Component("AlertDialogTrigger", "Button that opens the alert dialog"),
        Component("AlertDialogContent", "Container for all dialog content"),
        Component("AlertDialogHeader", "Container for title and description"),
        Component("AlertDialogTitle", "Primary heading text for the alert"),
        Component("AlertDialogDescription", "Supporting description text"),
        Component("AlertDialogFooter", "Container for action buttons"),
        Component("AlertDialogAction", "Primary action button (confirms/proceeds)"),
        Component("AlertDialogCancel", "Secondary button (dismisses dialog)"),
    ]
)


# ============================================================================
# DOCS PAGE
# ============================================================================

def create_alert_dialog_docs():
    """Create alert dialog documentation page using convention-based approach."""
    hero_example = ComponentPreview(
        hero_alert_dialog_example(),
        hero_alert_dialog_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add alert-dialog",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="alert-dialog"
    )