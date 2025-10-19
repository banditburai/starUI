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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li, Style, Signal, switch
from starhtml.datastar import js, set_timeout, seq
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
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview



@with_code
def basic_dialog_example():
    return Dialog(
        DialogTrigger("Open Dialog"),
        DialogContent(
            DialogHeader(
                DialogTitle("Welcome to StarUI"),
                DialogDescription(
                    "This is a simple dialog demonstrating the basic structure and functionality."
                )
            ),
            P("Dialog content goes here. You can include any content you need.", cls="py-4"),
            DialogFooter(
                DialogClose("Got it")
            )
        )
    )


@with_code
def confirmation_dialog_example():
    def warning_section():
        consequences = [
            "All your projects will be deleted",
            "Your subscription will be cancelled",
            "You will lose access to all shared resources",
        ]

        return Div(
            Icon("lucide:alert-triangle", cls="h-6 w-6 text-destructive flex-shrink-0 mt-0.5"),
            Div(
                P("Warning: ", Span("This action is irreversible", cls="font-semibold"), cls="text-sm"),
                Ul(
                    *[Li(text, cls="text-sm") for text in consequences],
                    cls="list-disc list-inside mt-2 space-y-1 text-muted-foreground"
                ),
            ),
            cls="flex gap-3"
        )

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
            Div(warning_section(), cls="py-4"),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                DialogClose(
                    "Delete Account",
                    variant="destructive",
                    value="delete",
                    data_on_click="alert('Account deleted!')"
                )
            )
        )
    )


@with_code
def form_dialog_example():
    form_dialog = Signal("form_dialog", _ref_only=True)
    member_name = Signal("member_name", "")
    member_email = Signal("member_email", "")
    member_role = Signal("member_role", "viewer")
    member_role_value = Signal("member_role_value", "viewer", _ref_only=True)  # Reference to SelectWithLabel's internal signal
    send_invite = Signal("send_invite", True)
    send_welcome = Signal("send_welcome", True)

    def section_header(icon, title):
        return P(
            Icon(icon, cls="h-4 w-4 inline mr-2"),
            title,
            cls="text-sm font-semibold text-foreground mb-3 flex items-center"
        )

    def role_preview(role, icon, title, description, color):
        return Div(
            Icon(icon, cls=f"h-5 w-5 text-{color}-500"),
            Div(
                P(title, cls="font-medium text-sm"),
                P(description, cls="text-xs text-muted-foreground"),
                cls="ml-3"
            ),
            data_show=member_role_value == role,
            cls=f"flex items-center p-3 bg-{color}-50 dark:bg-{color}-950/20 rounded-md border border-{color}-200 dark:border-{color}-800"
        )

    def personal_info_section():
        return Div(
            section_header("lucide:user", "Personal Information"),
            InputWithLabel(
                label="Full Name",
                placeholder="Enter full name",
                signal=member_name,
                required=True,
                helper_text="This will be displayed in the team directory"
            ),
            InputWithLabel(
                label="Email Address",
                type="email",
                placeholder="Enter email address",
                signal=member_email,
                required=True,
                helper_text="Invitation will be sent to this email"
            ),
            cls="space-y-4"
        )

    def role_section():
        roles = [
            ("viewer", "lucide:eye", "Viewer Access", "Can view and comment on projects", "blue"),
            ("editor", "lucide:edit-3", "Editor Access", "Can edit, create, and manage projects", "green"),
            ("admin", "lucide:crown", "Admin Access", "Full control including user and billing management", "amber"),
        ]

        return Div(
            section_header("lucide:shield-check", "Access & Permissions"),
            SelectWithLabel(
                label="Role",
                options=[
                    ("viewer", "Viewer - Can view projects and files"),
                    ("editor", "Editor - Can edit projects and collaborate"),
                    ("admin", "Admin - Full administrative access")
                ],
                value="viewer",
                signal=member_role,
                helper_text="Choose the appropriate permission level for this user"
            ),
            Div(
                *[role_preview(*role) for role in roles],
                cls="mt-3"
            ),
            cls="space-y-4"
        )

    def notification_section():
        return Div(
            section_header("lucide:mail", "Notification Settings"),
            CheckboxWithLabel(
                label="Send invitation email immediately",
                checked=True,
                signal=send_invite,
                helper_text="The team member will receive an email invitation to join"
            ),
            CheckboxWithLabel(
                label="Send welcome email with getting started guide",
                checked=True,
                signal=send_welcome,
                helper_text="Include helpful resources for new team members"
            ),
            cls="space-y-3"
        )

    return Dialog(
        DialogTrigger(
            Icon("lucide:user-plus", cls="h-4 w-4 mr-2"),
            "Add Team Member"
        ),
        DialogContent(
            member_role_value,
            DialogHeader(
                DialogTitle("Invite Team Member"),
                DialogDescription("Add a new member to your team and assign their role")
            ),
            Form(
                member_name,
                member_email,
                personal_info_section(),
                Separator(cls="my-6"),
                role_section(),
                Separator(cls="my-6"),
                notification_section(),
                cls="space-y-6 py-4"
            ),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                Button(
                    Icon("lucide:send", cls="h-4 w-4 mr-2"),
                    "Send Invitation",
                    data_attr_disabled=~member_name | ~member_email,
                    data_on_click=[
                        "evt.preventDefault()",
                        f"alert('✅ Invitation sent to ' + {member_email} + ' as ' + {member_role_value})",
                        form_dialog.close(),
                        member_name.set(''),
                        member_email.set(''),
                        member_role_value.set('viewer'),
                        send_invite.set(True),
                        send_welcome.set(True)
                    ],
                    type="submit",
                    cls="bg-primary hover:bg-primary/90"
                )
            )
        ),
        signal=form_dialog,
        size="lg"
    )


@with_code
def scrollable_content_example():
    return Dialog(
        DialogTrigger("View Terms"),
        DialogContent(
            terms_accepted := Signal("terms_accepted", False),
            DialogHeader(
                DialogTitle("Terms of Service"),
                DialogDescription("Please review our terms and conditions")
            ),
            Div(
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

                    cls="py-4 px-4"
                ),
                cls="max-h-[300px] overflow-y-auto my-4 border rounded-md"
            ),
            CheckboxWithLabel(
                label="I have read and agree to the terms",
                signal=terms_accepted
            ),
            DialogFooter(
                DialogClose("Decline", variant="outline"),
                DialogClose(
                    "Accept",
                    data_attr_disabled=~terms_accepted,
                    variant="default"
                )
            )
        ),
        size="lg"
    )


@with_code
def loading_async_dialog_example():
    uploading = Signal("uploading", False)
    upload_complete = Signal("upload_complete", False)
    upload_progress = Signal("upload_progress", 0)
    file_selected = Signal("file_selected", False)
    doc_title = Signal("doc_title", "")

    def file_dropzone():
        return Div(
            P("Choose file to upload:", cls="text-sm font-medium mb-2"),
            Div(
                Span(Icon("lucide:file-text", cls="w-8 h-8 text-muted-foreground mb-2"), data_show=~file_selected),
                Span(Icon("lucide:file-check", cls="w-8 h-8 text-green-500 mb-2"), data_show=file_selected),
                P(
                    data_text=file_selected.if_("project-proposal.pdf", "Click to select file or drag and drop"),
                    data_style_color=file_selected.if_("hsl(var(--foreground))", "hsl(var(--muted-foreground))"),
                    cls="text-sm font-medium mb-1",
                ),
                P(data_text=file_selected.if_("2.4 MB", "PDF, DOC, TXT up to 10MB"), cls="text-xs text-muted-foreground"),
                data_on_click=file_selected.set(True),
                data_style_border_color=file_selected.if_("hsl(var(--border))", "hsl(var(--muted))"),
                data_style_background_color=file_selected.if_("hsl(var(--muted)/0.3)", "transparent"),
                cls="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200",
            ),
            cls="mb-4"
        )

    def upload_form():
        return Div(
            InputWithLabel(
                label="Document Title",
                placeholder="Enter a title for your document",
                signal=doc_title,
                required=True,
                helper_text="Required - give your document a descriptive name"
            ),
            file_dropzone(),
            data_show=~uploading & ~upload_complete,
            cls="py-4 space-y-4"
        )

    def uploading_state():
        return Div(
            Icon("lucide:loader", cls="w-8 h-8 text-primary animate-spin mx-auto mb-4"),
            P("Uploading document...", cls="text-center font-medium mb-2"),
            P(data_text=upload_progress + "% complete", cls="text-center text-sm text-muted-foreground mb-4"),
            Div(
                Div(data_style_width=upload_progress + "%", cls="h-2 bg-primary rounded-full transition-all duration-300"),
                cls="w-full bg-muted rounded-full h-2"
            ),
            data_show=uploading & ~upload_complete,
            cls="text-center py-8"
        )

    def complete_state():
        return Div(
            Icon("lucide:check-circle", cls="w-8 h-8 text-green-500 mx-auto mb-4"),
            P("Upload Complete!", cls="text-center font-medium text-green-600 mb-2"),
            P(data_text="Successfully uploaded: " + doc_title.or_("Document"), cls="text-center text-sm text-muted-foreground"),
            data_show=upload_complete,
            cls="text-center py-8"
        )

    def start_upload():
        return [
            upload_complete.set(False),
            uploading.set(True),
            upload_progress.set(0),
            *[set_timeout(upload_progress.set(i * 20), i * 200) for i in range(1, 6)],
            set_timeout(upload_complete.set(True), 1200)
        ]

    def reset_form():
        return [
            uploading.set(False),
            upload_complete.set(False),
            upload_progress.set(0),
            file_selected.set(False),
            doc_title.set('')
        ]

    return Dialog(
        DialogTrigger(Icon("lucide:cloud-upload", cls="h-4 w-4 mr-2"), "Upload File"),
        DialogContent(
            uploading,
            upload_complete,
            upload_progress,
            file_selected,
            doc_title,
            DialogHeader(
                DialogTitle("Upload Document"),
                DialogDescription("Upload and process your document")
            ),
            upload_form(),
            uploading_state(),
            complete_state(),
            DialogFooter(
                DialogClose("Cancel", data_show=~uploading, variant="outline"),
                Button(
                    "Start Upload",
                    data_attr_disabled=~doc_title | ~file_selected,
                    data_show=~uploading & ~upload_complete,
                    data_on_click=start_upload()
                ),
                DialogClose("Done", data_show=upload_complete, data_on_click=reset_form())
            )
        )
    )


@with_code
def multi_step_wizard_example():
    step = Signal("step", 1)
    project_type = Signal("project_type", "")
    project_name = Signal("project_name", "")
    project_desc = Signal("project_desc", "")
    wizard_ref = Signal("wizard_dialog", _ref_only=True)

    def step_indicator(number, label):
        return Div(
            Div(
                Span(Icon("lucide:check", cls="w-3 h-3 text-white"), data_show=step > number),
                Span(str(number), data_show=step <= number),
                data_style_background_color=(step >= number).if_('rgb(59, 130, 246)', 'rgb(203, 213, 225)'),
                data_style_color=(step >= number).if_('white', 'rgb(71, 85, 105)'),
                cls="w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold"
            ),
            P(label,
                data_style_color=(step >= number).if_('hsl(var(--foreground))', 'hsl(var(--muted-foreground))'),
                cls="text-xs font-medium mt-2 text-center"
            ),
            cls="flex flex-col items-center"
        )

    def project_type_button(icon, title, description, type_value):
        return Button(
            Icon(icon, cls="h-8 w-8 mb-2"),
            P(title, cls="font-semibold"),
            P(description, cls="text-xs text-muted-foreground"),
            data_on_click=[project_type.set(type_value), step.set(2)],
            variant="outline",
            cls="h-auto flex-col p-4 w-full"
        )

    def progress_bar():
        return Div(
            Div(cls="absolute top-3 left-0 w-full h-1 bg-muted rounded-full"),
            Div(
                data_style_width=(step == 1).if_('0%', (step == 2).if_('50%', '100%')),
                cls="absolute top-3 left-0 h-1 bg-primary rounded-full transition-all duration-500"
            ),
            Div(
                step_indicator(1, "Project Type"),
                step_indicator(2, "Configuration"),
                step_indicator(3, "Review"),
                cls="flex justify-between items-start relative z-10"
            ),
            cls="relative w-full mb-8 px-8"
        )

    def step1_content():
        return Div(
            Div(
                project_type_button("lucide:globe", "Web Application", "React, Vue, or vanilla JS", "web"),
                project_type_button("lucide:smartphone", "Mobile App", "iOS or Android", "mobile"),
                project_type_button("lucide:server", "API Service", "REST or GraphQL", "api"),
                cls="grid grid-cols-3 gap-3"
            ),
            data_show=step == 1,
            cls="py-4"
        )

    def step2_content():
        return Div(
            InputWithLabel(label="Project Name", placeholder="my-awesome-project", signal=project_name, required=True),
            TextareaWithLabel(label="Description", placeholder="Describe your project...", rows=3, signal=project_desc),
            data_show=step == 2,
            cls="space-y-4 py-4"
        )

    def step3_content():
        return Div(
            Div(
                P("Project Type: ", Span(data_text=project_type, cls="font-semibold")),
                P("Name: ", Span(data_text=project_name.or_("Not specified"), cls="font-semibold")),
                P("Description: ", Span(data_text=project_desc.or_("Not specified"), cls="font-semibold")),
                cls="space-y-2 p-4 bg-muted rounded-md"
            ),
            data_show=step == 3,
            cls="py-4"
        )

    def handle_next():
        return switch([
            ((step == 1) & project_type, step.set(2)),
            ((step == 2) & project_name, step.set(3)),
            (step == 3, seq(
                set_timeout(js("alert(`Creating ${$project_type} project: ${$project_name}`)"), 100),
                set_timeout(seq(
                    step.set(1),
                    project_type.set(''),
                    project_name.set(''),
                    project_desc.set(''),
                    wizard_ref.close()
                ), 200)
            ))
        ])

    return Dialog(
        DialogTrigger(Icon("lucide:rocket", cls="h-4 w-4 mr-2"), "Start Setup"),
        DialogContent(
            step,
            project_type,
            project_name,
            project_desc,
            DialogHeader(
                DialogTitle("Project Setup"),
                DialogDescription(
                    data_text=(step == 1).if_('Choose your project type', (step == 2).if_('Configure settings', 'Review and confirm'))
                )
            ),
            progress_bar(),
            step1_content(),
            step2_content(),
            step3_content(),
            DialogFooter(
                Button(
                    "Previous",
                    data_on_click=step.set((step - 1).max(1)),
                    data_attr_disabled=step == 1,
                    variant="outline"
                ),
                Button(
                    data_text=(step == 3).if_('Create Project', 'Next'),
                    data_on_click=handle_next(),
                    data_attr_disabled=((step == 1) & ~project_type) | ((step == 2) & ~project_name)
                )
            )
        ),
        signal="wizard_dialog",
        size="lg"
    )


@with_code
def settings_dialog_example():
    settings_tab = Signal("settings_tab", "profile")
    profile_name = Signal("profile_name", "John Doe")
    profile_email = Signal("profile_email", "john@example.com")
    profile_bio = Signal("profile_bio", "")
    profile_timezone = Signal("profile_timezone", "utc")
    notify_email = Signal("notify_email", True)
    notify_push = Signal("notify_push", False)
    notify_marketing = Signal("notify_marketing", False)
    notify_frequency = Signal("notify_frequency", "weekly")
    security_2fa = Signal("security_2fa", False)
    security_login_notify = Signal("security_login_notify", True)
    settings_ref = Signal("settings_dialog", _ref_only=True)

    def tab_button(icon, label, tab_id):
        return Button(
            Icon(icon, cls="h-4 w-4 mr-2"),
            label,
            data_on_click=settings_tab.set(tab_id),
            data_style_background_color=(settings_tab == tab_id).if_('#f1f5f9', 'transparent'),
            data_style_color=(settings_tab == tab_id).if_('#0f172a', '#71717a'),
            data_style_box_shadow=(settings_tab == tab_id).if_('0 1px 2px rgba(0,0,0,0.1)', 'none'),
            variant="ghost",
            size="sm",
            cls="flex-1"
        )

    def profile_tab():
        return Div(
            InputWithLabel(label="Display Name", placeholder="John Doe", signal=profile_name),
            InputWithLabel(label="Email", type="email", placeholder="john@example.com", signal=profile_email),
            TextareaWithLabel(label="Bio", placeholder="Tell us about yourself...", rows=3, signal=profile_bio),
            SelectWithLabel(
                label="Time Zone",
                options=[
                    ("utc", "UTC"),
                    ("pst", "Pacific Standard Time"),
                    ("est", "Eastern Standard Time"),
                    ("cet", "Central European Time")
                ],
                signal=profile_timezone
            ),
            data_show=settings_tab == "profile",
            cls="space-y-4"
        )

    def notifications_tab():
        return Div(
            CheckboxWithLabel(
                label="Email notifications",
                helper_text="Receive updates and announcements via email",
                signal=notify_email
            ),
            CheckboxWithLabel(
                label="Push notifications",
                helper_text="Get notified about important events",
                signal=notify_push
            ),
            CheckboxWithLabel(
                label="Marketing emails",
                helper_text="Receive product updates and promotional content",
                signal=notify_marketing
            ),
            Separator(cls="my-4"),
            P("Notification Frequency", cls="text-sm font-medium mb-2"),
            SelectWithLabel(
                label="Email Digest",
                options=[
                    ("never", "Never"),
                    ("daily", "Daily"),
                    ("weekly", "Weekly"),
                    ("monthly", "Monthly")
                ],
                signal=notify_frequency,
                helper_text="How often you'd like to receive summary emails"
            ),
            data_show=settings_tab == "notifications",
            cls="space-y-4"
        )

    def security_tab():
        return Div(
            P("Password", cls="text-sm font-medium mb-2"),
            Div(
                P("Last changed: 2 months ago", cls="text-sm text-muted-foreground mb-2"),
                Button(
                    "Change Password",
                    data_on_click=js("alert('Password change dialog would open')"),
                    variant="outline",
                    size="sm"
                ),
                cls="mb-4"
            ),
            CheckboxWithLabel(
                label="Two-factor authentication",
                helper_text="Add an extra layer of security to your account",
                signal=security_2fa
            ),
            CheckboxWithLabel(
                label="Login notifications",
                helper_text="Get notified when someone signs into your account",
                signal=security_login_notify
            ),
            Separator(cls="my-4"),
            P("Session Management", cls="text-sm font-medium mb-2"),
            Div(
                P("Active sessions: 3 devices", cls="text-sm text-muted-foreground mb-2"),
                Button(
                    "View All Sessions",
                    data_on_click=js("alert('Sessions dialog would open')"),
                    variant="outline",
                    size="sm"
                ),
                cls="mb-4"
            ),
            data_show=settings_tab == "security",
            cls="space-y-4"
        )

    return Dialog(
        DialogTrigger(Icon("lucide:settings", cls="h-4 w-4 mr-2"), "Settings"),
        DialogContent(
            settings_tab,
            DialogHeader(
                DialogTitle("Settings"),
                DialogDescription("Manage your account and application preferences")
            ),
            Div(
                tab_button("lucide:user", "Profile", "profile"),
                tab_button("lucide:bell", "Notifications", "notifications"),
                tab_button("lucide:shield", "Security", "security"),
                cls="flex gap-1 mb-6 p-1 bg-muted/30 rounded-lg"
            ),
            profile_tab(),
            notifications_tab(),
            security_tab(),
            DialogFooter(
                DialogClose("Cancel", variant="outline"),
                Button(
                    "Save Changes",
                    data_on_click=settings_ref.close()
                )
            ),
            cls="pb-2"
        ),
        signal="settings_dialog",
        size="lg"
    )


# Dialog sizes example
@with_code
def dialog_sizes_example():
    return Div(
        Dialog(
            DialogTrigger("Small", variant="outline", cls="mr-2"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Small Dialog"),
                    DialogDescription("This is a small dialog (max-width: sm)")
                ),
                P("Compact content area.", cls="py-4"),
                DialogFooter(DialogClose("Close"))
            ),
            size="sm"
        ),
        Dialog(
            DialogTrigger("Medium", variant="outline", cls="mr-2"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Medium Dialog"),
                    DialogDescription("This is a medium dialog (max-width: lg)")
                ),
                P("Standard content area.", cls="py-4"),
                DialogFooter(DialogClose("Close"))
            ),
            size="md"
        ),
        Dialog(
            DialogTrigger("Large", variant="outline", cls="mr-2"),
            DialogContent(
                DialogHeader(
                    DialogTitle("Large Dialog"),
                    DialogDescription("This is a large dialog (max-width: 2xl)")
                ),
                P("Spacious content area for complex forms or content.", cls="py-4"),
                DialogFooter(DialogClose("Close"))
            ),
            size="lg"
        ),
        cls="flex flex-wrap"
    )



EXAMPLES_DATA = [
    {"title": "Basic Dialog", "description": "Simple dialog with title, description, and close button", "fn": basic_dialog_example},
    {"title": "Confirmation Dialog", "description": "Destructive action confirmation with warnings", "fn": confirmation_dialog_example},
    {"title": "Form Dialog", "description": "Complex form with multiple input types in a dialog", "fn": form_dialog_example},
    {"title": "Scrollable Content", "description": "Dialog with scrollable content and conditional actions", "fn": scrollable_content_example},
    {"title": "Loading/Async Dialog", "description": "Dialog with loading states, progress tracking, and async operations", "fn": loading_async_dialog_example},
    {"title": "Multi-Step Wizard", "description": "Complex wizard flow with step indicators and validation", "fn": multi_step_wizard_example},
    {"title": "Settings Dialog", "description": "Tabbed interface for managing different categories of settings", "fn": settings_dialog_example},
    {"title": "Dialog Sizes", "description": "Different dialog sizes for various content needs", "fn": dialog_sizes_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Dialog", "The main dialog container with modal behavior and backdrop"),
        Component("DialogTrigger", "Button that opens the dialog when clicked"),
        Component("DialogContent", "Container for all dialog content with proper styling and positioning"),
        Component("DialogHeader", "Header section containing title and description"),
        Component("DialogTitle", "Main heading for the dialog"),
        Component("DialogDescription", "Supporting text that describes the dialog purpose"),
        Component("DialogFooter", "Footer section for action buttons and controls"),
        Component("DialogClose", "Button that closes the dialog and optionally returns a value"),
    ]
)


def create_dialog_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)