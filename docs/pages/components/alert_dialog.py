"""
AlertDialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Alert Dialog"
DESCRIPTION = "A modal dialog that interrupts the user with important content and expects a response."
CATEGORY = "overlay"
ORDER = 45
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Code, Ul, Li
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style
)
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


def examples():
    """Generate alert dialog examples using ComponentPreview with tabs."""
    
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
                AlertDialogCancel("Dismiss", ref_id="basic_alert"),
                AlertDialogAction("Understood", ref_id="basic_alert")
            )
        )
        
        return AlertDialog(
            AlertDialogTrigger("Show Alert", ref_id="basic_alert"),
            dialog_content,
            ref_id="basic_alert"
        )
    
    yield ComponentPreview(
        basic_alert_dialog_example(),
        basic_alert_dialog_example.code,
        title="Basic Alert",
        description="Simple alert dialog with cancel and action buttons"
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
                AlertDialogCancel("Cancel", ref_id="delete_repo"),
                AlertDialogAction(
                    "Delete Repository",
                    ref_id="delete_repo",
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
                            ref_id="delete_repo",
                            variant="destructive",
                            size="sm"
                        ),
                        dialog_content,
                        ref_id="delete_repo"
                    ),
                    cls="flex items-end justify-between gap-6 p-6 border rounded-lg"
                )
            ),
            cls="max-w-lg"
        )
    
    yield ComponentPreview(
        destructive_alert_dialog_example(),
        destructive_alert_dialog_example.code,
        title="Destructive Action",
        description="High-risk action with clear warnings and consequences"
    )
    
    @with_code
    def unsaved_changes_alert_dialog_example():
        editor_form = Div(
            InputWithLabel(   
                label="Document Title",
                value="My Document",
                signal="doc_title"                                                                              
            ),
            InputWithLabel(
                label="Author",
                value="John Doe",
                signal="doc_author",
                cls="mt-4"                                                                            
            ),
            P("Make changes to the document fields above and try to save.", 
              cls="text-sm text-muted-foreground italic mt-4")
        )
        
        changes_preview = Div(
            Div(
                Icon("lucide:save", cls="h-4 w-4 mr-2 text-blue-500"),
                P("Your changes:", cls="text-sm font-medium"),
                cls="flex items-center mb-2"
            ),
            Div(
                P("Title: ", Span(ds_text("$doc_title"), cls="font-mono"), cls="text-sm"),
                P("Author: ", Span(ds_text("$doc_author"), cls="font-mono"), cls="text-sm"),
                cls="space-y-1 p-3 bg-muted rounded-md"
            ),
            cls="py-6"
        )
        
        dialog_content = AlertDialogContent(
            AlertDialogHeader(
                AlertDialogTitle("Save changes?"),
                AlertDialogDescription("You have unsaved changes. What would you like to do?")
            ),
            changes_preview,
            AlertDialogFooter(
                AlertDialogAction(
                    "Discard Changes",
                    ref_id="unsaved_dialog",
                    variant="destructive",
                    action="$doc_title='My Document'; $doc_author='John Doe'"
                ),
                AlertDialogCancel("Keep Editing", ref_id="unsaved_dialog"),
                AlertDialogAction("Save & Exit", ref_id="unsaved_dialog")
            )
        )
        
        return Card(
            CardHeader(
                CardTitle("Document Editor"),
                CardDescription("Edit your document details")
            ),
            CardContent(
                editor_form,
                Div(
                    Button("Cancel", ds_on_click("$changes_made = true"), variant="outline"),
                    AlertDialog(
                        AlertDialogTrigger("Save & Exit", ref_id="unsaved_dialog"),
                        dialog_content,
                        ref_id="unsaved_dialog"
                    ),
                    cls="flex gap-2 mt-4"
                ),
                ds_signals(
                    doc_title=value("My Document"),
                    doc_author=value("John Doe"),
                    changes_made=False
                )
            ),
            cls="max-w-md"
        )
    
    yield ComponentPreview(
        unsaved_changes_alert_dialog_example(),
        unsaved_changes_alert_dialog_example.code,
        title="Unsaved Changes",
        description="Three-option dialog for handling unsaved work"
    )
    
    @with_code
    def session_timeout_alert_dialog_example():
        return Div(
            Card(
                CardHeader(
                    CardTitle("Session Management"),
                    CardDescription("Auto-logout demonstration with warning")
                ),
                CardContent(
                    Div(
                        ds_signals(
                            session_time=15,
                            logged_in=False,
                            timer_active=False
                        ),
                    
                    Div(
                        Button(
                            "Login",
                            ds_on_click("$logged_in = true; $session_time = 15; $timer_active = true"),
                            variant="default"
                        ),
                        ds_show("!$logged_in")
                    ),
                    
                    Div(
                        P("Logged in as: user@example.com", cls="text-sm font-medium mb-2"),
                        P(
                            "Session expires in: ",
                            Span(ds_text("$session_time"), cls="font-mono font-bold text-lg"),
                            " seconds",
                            cls="text-sm"
                        ),
                        
                        Div(
                            Div(
                                ds_style(width="`${($session_time / 15) * 100}%`"),
                                cls="h-2 bg-orange-500 rounded-full transition-all duration-1000"
                            ),
                            cls="w-full bg-secondary rounded-full h-2 mt-2"
                        ),
                        
                        Button(
                            "Logout",
                            ds_on_click("$logged_in = false; $timer_active = false; $session_time = 15"),
                            variant="outline",
                            size="sm",
                            cls="mt-4"
                        ),
                        ds_show("$logged_in"),
                        cls="space-y-2"
                    ),
                    
                    Div(
                        ds_effect("""
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
                        Div(),
                        AlertDialogContent(
                            Icon("lucide:clock", cls="h-12 w-12 text-orange-500 mx-auto mb-4"),
                            AlertDialogHeader(
                                AlertDialogTitle("Session Expiring Soon"),
                                AlertDialogDescription(
                                    "Your session will expire in ",
                                    Span(ds_text("$session_time"), cls="font-bold text-orange-500"),
                                    " seconds. Do you want to continue?"
                                )
                            ),
                            AlertDialogFooter(
                                AlertDialogAction(
                                    "Logout Now",
                                    ref_id="timeout_dialog",
                                    variant="destructive",
                                    action="$logged_in = false; $timer_active = false; $session_time = 15"
                                ),
                                AlertDialogAction(
                                    "Continue Session",
                                    ref_id="timeout_dialog",
                                    action="$session_time = 15"
                                )
                            )
                        ),
                        ref_id="timeout_dialog"
                    )
                )
            ),
            cls="w-full max-w-lg"
        ),
        cls="w-full max-w-2xl"
    )
    
    yield ComponentPreview(
        session_timeout_alert_dialog_example(),
        session_timeout_alert_dialog_example.code,
        title="Session Timeout",
        description="Auto-triggered alert with countdown timer"
    )
    
    @with_code
    def batch_operation_alert_dialog_example():
        files = [
            {"name": "file1.txt", "signal": "file1", "checked": True},
            {"name": "file2.pdf", "signal": "file2", "checked": True},
            {"name": "file3.jpg", "signal": "file3", "checked": False},
            {"name": "file4.doc", "signal": "file4", "checked": True}
        ]
        
        return Card(
            CardHeader(
                CardTitle("Batch Operations"),
                CardDescription("Confirm actions on multiple items")
            ),
            CardContent(
                Div(
                    Div(
                        *[Div(
                            CheckboxWithLabel(
                                label=file["name"],
                                signal=file["signal"],
                                checked=file["checked"]
                            ),
                            ds_show(f"${file['signal']}_exists")
                        ) for file in files],
                        cls="space-y-2"
                    ),
                    
                    Div(
                        P(
                            Span(ds_text(f"[${', $'.join(file['signal'] for file in files)}].filter(Boolean).length"), cls="font-bold"),
                            " items selected",
                            cls="text-sm text-muted-foreground"
                        ),
                        AlertDialog(
                            AlertDialogTrigger(
                                Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                                "Delete Selected",
                                variant="destructive",
                                ref_id="batch_dialog",
                                ds_disabled=f"!({' || '.join('$' + file['signal'] for file in files)})"
                            ),
                            AlertDialogContent(
                                AlertDialogHeader(
                                    AlertDialogTitle("Delete Multiple Items"),
                                    AlertDialogDescription(
                                        "You are about to delete ",
                                        Span(
                                            ds_text(f"[${', $'.join(file['signal'] for file in files)}].filter(Boolean).length"),
                                            cls="font-bold text-destructive"
                                        ),
                                        " items. This action cannot be undone."
                                    )
                                ),
                                Div(
                                    P("The following items will be deleted:", cls="text-sm font-medium mb-2"),
                                    Ul(
                                        *[Li(
                                            file["name"],
                                            ds_show(f"${file['signal']}"),
                                            cls="text-sm text-muted-foreground"
                                        ) for file in files],
                                        cls="list-disc list-inside space-y-1"
                                    ),
                                    cls="py-4"
                                ),
                                AlertDialogFooter(
                                    AlertDialogCancel("Cancel", ref_id="batch_dialog"),
                                    AlertDialogAction(
                                        ds_text(f"'Delete ' + [${', $'.join(file['signal'] for file in files)}].filter(Boolean).length + ' Items'"),
                                        ref_id="batch_dialog",
                                        variant="destructive",
                                        action="; ".join(f"if(${file['signal']}) ${file['signal']}_exists=false; ${file['signal']}=false" for file in files)
                                    )
                                )
                            ),
                            ref_id="batch_dialog"
                        ),
                        cls="flex items-center gap-4 mt-4"
                    ),
                    ds_signals(
                        **{file["signal"]: file["checked"] for file in files},
                        **{f"{file['signal']}_exists": True for file in files}
                    ),
                    cls="space-y-2"
                )
            ),
            cls="max-w-md"
        )
    
    yield ComponentPreview(
        batch_operation_alert_dialog_example(),
        batch_operation_alert_dialog_example.code,
        title="Batch Operations",
        description="Confirm actions on multiple selected items"
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
                AlertDialogCancel("Cancel", ref_id="payment_dialog"),
                AlertDialogAction("Confirm Payment", ref_id="payment_dialog")
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
                        ref_id="payment_dialog",
                        cls="w-full"
                    ),
                    dialog_content,
                    ref_id="payment_dialog"
                )
            ),
            cls="max-w-sm"
        )
    
    yield ComponentPreview(
        payment_confirmation_alert_dialog_example(),
        payment_confirmation_alert_dialog_example.code,
        title="Payment Confirmation",
        description="Secure payment confirmation with trust indicators"
    )


def create_alert_dialog_docs():
    """Create alert dialog documentation page using convention-based approach."""
    
    # For AlertDialog, users need to understand the building blocks (sub-components)
    # rather than the main props, since examples show usage patterns clearly
    api_reference = build_api_reference(
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
                AlertDialogCancel("Cancel", ref_id="hero_alert"),
                AlertDialogAction(
                    "Delete",
                    ref_id="hero_alert",
                    variant="destructive"
                )
            )
        )
        
        return AlertDialog(
            AlertDialogTrigger(
                "Delete Item",
                ref_id="hero_alert",
                variant="destructive"
            ),
            dialog_content,
            ref_id="hero_alert"
        )
    
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
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="alert-dialog"
    )