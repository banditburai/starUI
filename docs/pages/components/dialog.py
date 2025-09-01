"""
Dialog component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Dialog"
DESCRIPTION = "A modal dialog component using the native HTML dialog element for accessibility and performance."
CATEGORY = "overlay"
ORDER = 40
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle
)
from starui.registry.components.dialog import (
    Dialog, DialogTrigger, DialogContent, DialogHeader, DialogFooter,
    DialogTitle, DialogDescription, DialogClose
)
from starui.registry.components.button import Button
from starui.registry.components.input import Input as UIInput, InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.select import SelectWithLabel
from starui.registry.components.checkbox import CheckboxWithLabel
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate dialog examples using ComponentPreview with tabs."""
    
    # Basic dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger("Open Dialog", ref_id="basic_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Welcome to StarUI"),
                    DialogDescription(
                        "This is a simple dialog demonstrating the basic structure and functionality."
                    )
                ),
                P("Dialog content goes here. You can include any content you need.", cls="py-4"),
                DialogFooter(
                    DialogClose("Got it", ref_id="basic_dialog")
                )
            ),
            ref_id="basic_dialog"
        ),
        '''Dialog(
    DialogTrigger("Open Dialog", ref_id="basic_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Welcome to StarUI"),
            DialogDescription("This is a simple dialog...")
        ),
        P("Dialog content goes here."),
        DialogFooter(
            DialogClose("Got it", ref_id="basic_dialog")
        )
    ),
    ref_id="basic_dialog"
)''',
        title="Basic Dialog",
        description="Simple dialog with title, description, and close button"
    )
    
    # Confirmation dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:trash-2", cls="h-4 w-4 mr-2"),
                "Delete Account",
                ref_id="confirm_dialog",
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
                    P(
                        Icon("lucide:alert-triangle", cls="h-4 w-4 inline mr-2 text-destructive"),
                        "Warning: ",
                        Span("This action is irreversible", cls="font-semibold"),
                        cls="text-sm"
                    ),
                    Ul(
                        Li("All your projects will be deleted", cls="text-sm"),
                        Li("Your subscription will be cancelled", cls="text-sm"),
                        Li("You will lose access to all shared resources", cls="text-sm"),
                        cls="list-disc list-inside mt-2 space-y-1 text-muted-foreground"
                    ),
                    cls="py-4"
                ),
                DialogFooter(
                    DialogClose("Cancel", ref_id="confirm_dialog", variant="outline"),
                    DialogClose(
                        "Delete Account",
                        ref_id="confirm_dialog",
                        variant="destructive",
                        value="delete",
                        ds_on_click="alert('Account deleted!')"
                    )
                )
            ),
            ref_id="confirm_dialog"
        ),
        '''Dialog(
    DialogTrigger(
        Icon("lucide:trash-2"),
        "Delete Account",
        ref_id="confirm_dialog",
        variant="destructive"
    ),
    DialogContent(
        DialogHeader(
            DialogTitle("Are you absolutely sure?"),
            DialogDescription("This action cannot be undone...")
        ),
        Div(
            P(Icon("lucide:alert-triangle"), "Warning: This is irreversible"),
            Ul(
                Li("All projects will be deleted"),
                Li("Subscription will be cancelled"),
                Li("Access will be revoked")
            )
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Delete Account", variant="destructive", value="delete")
        )
    ),
    ref_id="confirm_dialog"
)''',
        title="Confirmation Dialog",
        description="Destructive action confirmation with warnings"
    )
    
    # Form dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:user-plus", cls="h-4 w-4 mr-2"),
                "Add Team Member",
                ref_id="form_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Invite Team Member"),
                    DialogDescription("Add a new member to your team")
                ),
                Form(
                    InputWithLabel(
                        label="Name",
                        placeholder="John Doe",
                        signal="member_name",
                        required=True
                    ),
                    InputWithLabel(
                        label="Email",
                        type="email",
                        placeholder="john@example.com",
                        signal="member_email",
                        required=True
                    ),
                    SelectWithLabel(
                        label="Role",
                        options=[
                            ("viewer", "Viewer - Can view projects"),
                            ("editor", "Editor - Can edit projects"),
                            ("admin", "Admin - Full access")
                        ],
                        value="viewer",
                        signal="member_role",
                        helper_text="Choose the appropriate permission level"
                    ),
                    CheckboxWithLabel(
                        label="Send invitation email",
                        checked=True,
                        signal="send_invite",
                        helper_text="Notify the user via email"
                    ),
                    DialogFooter(
                        DialogClose("Cancel", ref_id="form_dialog", variant="outline"),
                        Button(
                            "Send Invitation",
                            type="submit",
                            ds_on_click="""
                                event.preventDefault();
                                if ($member_name && $member_email) {
                                    alert(`Invitation sent to ${$member_email} as ${$member_role_label}`);
                                    $form_dialog.close();
                                    $member_name = '';
                                    $member_email = '';
                                }
                            """
                        )
                    ),
                    ds_signals(
                        member_name=value(""),
                        member_email=value(""),
                        member_role=value("viewer"),
                        send_invite=True
                    ),
                    cls="space-y-4"
                )
            ),
            ref_id="form_dialog"
        ),
        '''Dialog(
    DialogTrigger("Add Team Member", ref_id="form_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Invite Team Member"),
            DialogDescription("Add a new member to your team")
        ),
        Form(
            InputWithLabel(label="Name", signal="member_name", required=True),
            InputWithLabel(label="Email", type="email", signal="member_email", required=True),
            SelectWithLabel(
                label="Role",
                options=[("viewer", "Viewer"), ("editor", "Editor"), ("admin", "Admin")],
                signal="member_role"
            ),
            CheckboxWithLabel(label="Send invitation email", signal="send_invite"),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                Button("Send Invitation", type="submit", ds_on_click="submitForm()")
            ),
            ds_signals(member_name="", member_email="", member_role="viewer")
        )
    ),
    ref_id="form_dialog"
)''',
        title="Form Dialog",
        description="Complex form with multiple input types in a dialog"
    )
    
    # Scrollable content dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger("View Terms", ref_id="scroll_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Terms of Service"),
                    DialogDescription("Please review our terms and conditions")
                ),
                Div(
                    H3("1. Acceptance of Terms", cls="font-semibold mb-2"),
                    P("By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement.", cls="text-sm text-muted-foreground mb-4"),
                    
                    H3("2. Use License", cls="font-semibold mb-2"),
                    P("Permission is granted to temporarily download one copy of the materials for personal, non-commercial transitory viewing only.", cls="text-sm text-muted-foreground mb-4"),
                    
                    H3("3. Disclaimer", cls="font-semibold mb-2"),
                    P("The materials on this service are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.", cls="text-sm text-muted-foreground mb-4"),
                    
                    H3("4. Limitations", cls="font-semibold mb-2"),
                    P("In no event shall our company or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on our service.", cls="text-sm text-muted-foreground mb-4"),
                    
                    H3("5. Privacy Policy", cls="font-semibold mb-2"),
                    P("Your privacy is important to us. Our privacy policy explains how we collect, use, and protect your data.", cls="text-sm text-muted-foreground mb-4"),
                    
                    H3("6. Account Termination", cls="font-semibold mb-2"),
                    P("We reserve the right to terminate accounts that violate our terms of service.", cls="text-sm text-muted-foreground"),
                    
                    cls="max-h-[300px] overflow-y-auto py-4 px-1"
                ),
                CheckboxWithLabel(
                    label="I have read and agree to the terms",
                    signal="terms_accepted"
                ),
                DialogFooter(
                    DialogClose("Decline", ref_id="scroll_dialog", variant="outline"),
                    Button(
                        "Accept",
                        ds_disabled="!$terms_accepted",
                        ds_on_click="$terms_accepted && ($scroll_dialog.close(), alert('Terms accepted!'))"
                    )
                ),
                ds_signals(terms_accepted=False)
            ),
            ref_id="scroll_dialog",
            size="lg"
        ),
        '''Dialog(
    DialogTrigger("View Terms", ref_id="scroll_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Terms of Service"),
            DialogDescription("Please review our terms")
        ),
        Div(
            // Long scrollable content
            H3("1. Acceptance of Terms"),
            P("By accessing this service..."),
            // ... more sections
            cls="max-h-[300px] overflow-y-auto"
        ),
        CheckboxWithLabel(label="I agree to the terms", signal="terms_accepted"),
        DialogFooter(
            DialogClose("Decline", variant="outline"),
            Button("Accept", ds_disabled="!$terms_accepted")
        ),
        ds_signals(terms_accepted=False)
    ),
    ref_id="scroll_dialog",
    size="lg"
)''',
        title="Scrollable Content",
        description="Dialog with scrollable content and conditional actions"
    )
    
    # Multi-step dialog
    yield ComponentPreview(
        Dialog(
            DialogTrigger(
                Icon("lucide:rocket", cls="h-4 w-4 mr-2"),
                "Start Setup",
                ref_id="wizard_dialog"
            ),
            DialogContent(
                DialogHeader(
                    DialogTitle("Project Setup"),
                    DialogDescription(
                        ds_text("$step === 1 ? 'Choose your project type' : $step === 2 ? 'Configure settings' : 'Review and confirm'")
                    )
                ),
                # Step indicators
                Div(
                    Div(
                        Div(
                            "1",
                            ds_class(**{
                                "bg-primary text-primary-foreground": "$step >= 1",
                                "bg-muted text-muted-foreground": "$step < 1"
                            }),
                            cls="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                        ),
                        Div(
                            ds_class(**{
                                "bg-primary": "$step > 1",
                                "bg-muted": "$step <= 1"
                            }),
                            cls="flex-1 h-1"
                        ),
                        Div(
                            "2",
                            ds_class(**{
                                "bg-primary text-primary-foreground": "$step >= 2",
                                "bg-muted text-muted-foreground": "$step < 2"
                            }),
                            cls="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                        ),
                        Div(
                            ds_class(**{
                                "bg-primary": "$step > 2",
                                "bg-muted": "$step <= 2"
                            }),
                            cls="flex-1 h-1"
                        ),
                        Div(
                            "3",
                            ds_class(**{
                                "bg-primary text-primary-foreground": "$step >= 3",
                                "bg-muted text-muted-foreground": "$step < 3"
                            }),
                            cls="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                        ),
                        cls="flex items-center w-full mb-6"
                    )
                ),
                # Step 1: Project Type
                Div(
                    Div(
                        Button(
                            Icon("lucide:globe", cls="h-8 w-8 mb-2"),
                            P("Web Application", cls="font-semibold"),
                            P("React, Vue, or vanilla JS", cls="text-xs text-muted-foreground"),
                            variant="outline",
                            ds_on_click="$project_type = 'web'; $step = 2",
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        Button(
                            Icon("lucide:smartphone", cls="h-8 w-8 mb-2"),
                            P("Mobile App", cls="font-semibold"),
                            P("iOS or Android", cls="text-xs text-muted-foreground"),
                            variant="outline",
                            ds_on_click="$project_type = 'mobile'; $step = 2",
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        Button(
                            Icon("lucide:server", cls="h-8 w-8 mb-2"),
                            P("API Service", cls="font-semibold"),
                            P("REST or GraphQL", cls="text-xs text-muted-foreground"),
                            variant="outline",
                            ds_on_click="$project_type = 'api'; $step = 2",
                            cls="h-auto flex-col p-4 w-full"
                        ),
                        cls="grid grid-cols-3 gap-3"
                    ),
                    ds_show="$step === 1",
                    cls="py-4"
                ),
                # Step 2: Configuration
                Div(
                    InputWithLabel(
                        label="Project Name",
                        placeholder="my-awesome-project",
                        signal="project_name",
                        required=True
                    ),
                    TextareaWithLabel(
                        label="Description",
                        placeholder="Describe your project...",
                        rows=3,
                        signal="project_desc"
                    ),
                    ds_show="$step === 2",
                    cls="space-y-4 py-4"
                ),
                # Step 3: Review
                Div(
                    Div(
                        P("Project Type: ", Span(ds_text("$project_type"), cls="font-semibold")),
                        P("Name: ", Span(ds_text("$project_name || 'Not specified'"), cls="font-semibold")),
                        P("Description: ", Span(ds_text("$project_desc || 'Not specified'"), cls="font-semibold")),
                        cls="space-y-2 p-4 bg-muted rounded-md"
                    ),
                    ds_show="$step === 3",
                    cls="py-4"
                ),
                DialogFooter(
                    Button(
                        "Previous",
                        variant="outline",
                        ds_on_click="$step = Math.max(1, $step - 1)",
                        ds_disabled="$step === 1"
                    ),
                    Button(
                        ds_text="$step === 3 ? 'Create Project' : 'Next'",
                        ds_on_click="""
                            if ($step === 1 && $project_type) $step = 2;
                            else if ($step === 2 && $project_name) $step = 3;
                            else if ($step === 3) {
                                alert(`Creating ${$project_type} project: ${$project_name}`);
                                $wizard_dialog.close();
                                $step = 1;
                                $project_type = '';
                                $project_name = '';
                                $project_desc = '';
                            }
                        """,
                        ds_disabled="($step === 1 && !$project_type) || ($step === 2 && !$project_name)"
                    )
                ),
                ds_signals(
                    step=1,
                    project_type=value(""),
                    project_name=value(""),
                    project_desc=value("")
                )
            ),
            ref_id="wizard_dialog",
            size="lg"
        ),
    '''Dialog(
    DialogTrigger("Start Setup", ref_id="wizard_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Project Setup"),
            DialogDescription(ds_text("Step description based on $step"))
        ),
        // Step indicators
        Div(/* step bubbles and progress bars */),
        // Step 1
        Div(/* project type selection */, ds_show="$step === 1"),
        // Step 2
        Div(/* configuration form */, ds_show="$step === 2"),
        // Step 3
        Div(/* review and confirm */, ds_show="$step === 3"),
        DialogFooter(
            Button("Previous", ds_on_click="$step--", ds_disabled="$step === 1"),
            Button(
                ds_text("$step === 3 ? 'Create' : 'Next'"),
                ds_on_click="handleStep()"
            )
        ),
        ds_signals(step=1, project_type="", project_name="")
    ),
    ref_id="wizard_dialog"
)''',
    title="Multi-Step Wizard",
    description="Complex wizard flow with step indicators and validation"
    )
    
    # Custom styled dialog with sizes
    yield ComponentPreview(
        Div(
            Dialog(
                DialogTrigger("Small", ref_id="small_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Small Dialog"),
                        DialogDescription("This is a small dialog (max-width: sm)")
                    ),
                    P("Compact content area.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="small_dialog"))
                ),
                ref_id="small_dialog",
                size="sm"
            ),
            Dialog(
                DialogTrigger("Medium", ref_id="medium_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Medium Dialog"),
                        DialogDescription("This is a medium dialog (max-width: lg)")
                    ),
                    P("Standard content area.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="medium_dialog"))
                ),
                ref_id="medium_dialog",
                size="md"
            ),
            Dialog(
                DialogTrigger("Large", ref_id="large_dialog", variant="outline", cls="mr-2"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Large Dialog"),
                        DialogDescription("This is a large dialog (max-width: 2xl)")
                    ),
                    P("Spacious content area for complex forms or content.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="large_dialog"))
                ),
                ref_id="large_dialog",
                size="lg"
            ),
            Dialog(
                DialogTrigger("Extra Large", ref_id="xl_dialog", variant="outline"),
                DialogContent(
                    DialogHeader(
                        DialogTitle("Extra Large Dialog"),
                        DialogDescription("This is an extra large dialog (max-width: 4xl)")
                    ),
                    P("Very spacious content area for tables or detailed views.", cls="py-4"),
                    DialogFooter(DialogClose("Close", ref_id="xl_dialog"))
                ),
                ref_id="xl_dialog",
                size="xl"
            ),
            cls="flex flex-wrap gap-2"
        ),
        '''// Different dialog sizes
Dialog(DialogTrigger("Small"), DialogContent(...), ref_id="small", size="sm")
Dialog(DialogTrigger("Medium"), DialogContent(...), ref_id="medium", size="md")
Dialog(DialogTrigger("Large"), DialogContent(...), ref_id="large", size="lg")
Dialog(DialogTrigger("XL"), DialogContent(...), ref_id="xl", size="xl")''',
        title="Dialog Sizes",
        description="Different dialog sizes for various content needs"
    )


def create_dialog_docs():
    """Create dialog documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "trigger",
                "type": "FT",
                "description": "The trigger element (usually DialogTrigger)"
            },
            {
                "name": "content",
                "type": "FT",
                "description": "The dialog content (usually DialogContent)"
            },
            {
                "name": "ref_id",
                "type": "str",
                "description": "Unique identifier for the dialog instance"
            },
            {
                "name": "modal",
                "type": "bool",
                "default": "True",
                "description": "Whether dialog is modal (blocks interaction with rest of page)"
            },
            {
                "name": "size",
                "type": "Literal['sm', 'md', 'lg', 'xl', 'full']",
                "default": "'md'",
                "description": "Size of the dialog"
            }
        ],
        "sub_components": [
            {
                "name": "DialogTrigger",
                "description": "Button that opens the dialog",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the Dialog's ref_id"
                    },
                    {
                        "name": "variant",
                        "type": "str",
                        "default": "'default'",
                        "description": "Button variant"
                    }
                ]
            },
            {
                "name": "DialogContent",
                "description": "Container for dialog content",
                "props": [
                    {
                        "name": "show_close_button",
                        "type": "bool",
                        "default": "True",
                        "description": "Whether to show the X close button"
                    }
                ]
            },
            {
                "name": "DialogHeader",
                "description": "Container for title and description"
            },
            {
                "name": "DialogTitle",
                "description": "The dialog's title"
            },
            {
                "name": "DialogDescription",
                "description": "Subtitle or description text"
            },
            {
                "name": "DialogFooter",
                "description": "Container for action buttons"
            },
            {
                "name": "DialogClose",
                "description": "Button that closes the dialog",
                "props": [
                    {
                        "name": "ref_id",
                        "type": "str",
                        "description": "Must match the Dialog's ref_id"
                    },
                    {
                        "name": "value",
                        "type": "str",
                        "default": "''",
                        "description": "Return value when dialog closes"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Dialog(
            DialogTrigger("Open Dialog", ref_id="hero_dialog"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Edit Profile"),
                    DialogDescription("Make changes to your profile here. Click save when you're done.")
                ),
                Div(
                    InputWithLabel(
                        label="Username",
                        placeholder="@username",
                        signal="username"
                    ),
                    InputWithLabel(
                        label="Email",
                        type="email",
                        placeholder="email@example.com",
                        signal="email"
                    ),
                    ds_signals(username=value(""), email=value("")),
                    cls="space-y-4 py-4"
                ),
                DialogFooter(
                    DialogClose("Cancel", ref_id="hero_dialog", variant="outline"),
                    DialogClose("Save Changes", ref_id="hero_dialog", ds_on_click="alert('Profile saved!')")
                )
            ),
            ref_id="hero_dialog"
        ),
        '''Dialog(
    DialogTrigger("Open Dialog", ref_id="hero_dialog"),
    DialogContent(
        DialogHeader(
            DialogTitle("Edit Profile"),
            DialogDescription("Make changes to your profile...")
        ),
        Div(
            InputWithLabel(label="Username", signal="username"),
            InputWithLabel(label="Email", type="email", signal="email")
        ),
        DialogFooter(
            DialogClose("Cancel", variant="outline"),
            DialogClose("Save Changes")
        )
    ),
    ref_id="hero_dialog"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add dialog",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="dialog"
    )