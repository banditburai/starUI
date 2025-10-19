TITLE = "Textarea"
DESCRIPTION = "A multi-line text input field for longer content like comments, messages, and descriptions."
CATEGORY = "form"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Form, Code, Button as HTMLButton, Script, Signal, js, switch, seq, clipboard
from starui.registry.components.textarea import Textarea, TextareaWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def basic_textarea_example():
    return Div(
        Textarea(placeholder="Type your message here..."),
        Textarea(
            placeholder="With initial value",
            value="This textarea starts with content that you can edit.",
            cls="mt-4"
        ),
        Textarea(
            placeholder="Disabled textarea",
            disabled=True,
            cls="mt-4"
        ),
        cls="space-y-4 w-full max-w-3xl mx-auto"
    )


@with_code
def contextual_textarea_examples():
    quick_note = Signal("quick_note", "")
    article_summary = Signal("article_summary", "")
    essay_draft = Signal("essay_draft", "")

    return Div(
        quick_note,
        article_summary,
        essay_draft,
        Card(
            CardHeader(
                CardTitle("Quick Note"),
                CardDescription("Brief message or reminder")
            ),
            CardContent(
                TextareaWithLabel(
                    label="Note",
                    placeholder="Jot down your thoughts...",
                    rows=2,
                    signal=quick_note,
                    helper_text="Perfect for short messages"
                ),
                Button(
                    Icon("lucide:save", cls="h-4 w-4 mr-2"),
                    "Save Note",
                    size="sm",
                    cls="mt-3",
                    data_attr_disabled=quick_note.length.eq(0)
                )
            ),
            cls="w-full"
        ),
        Card(
            CardHeader(
                CardTitle("Article Summary"),
                CardDescription("Summarize the key points")
            ),
            CardContent(
                TextareaWithLabel(
                    label="Summary",
                    placeholder="Write a concise summary of the main ideas...",
                    rows=4,
                    signal=article_summary,
                    helper_text="Aim for 2-3 sentences"
                ),
                Div(
                    Badge(
                        variant="secondary",
                        data_text=article_summary.split(' ').length + " words"
                    ),
                    cls="mt-2",
                    data_show=article_summary.length > 0
                )
            ),
            cls="w-full"
        ),
        Card(
            CardHeader(
                CardTitle("Essay Draft"),
                CardDescription("Long-form writing space")
            ),
            CardContent(
                TextareaWithLabel(
                    label="Content",
                    placeholder="Begin writing your essay or long-form content here...",
                    rows=8,
                    signal=essay_draft,
                    helper_text="Take your time to develop your ideas"
                ),
                Div(
                    P(
                        "Words: ",
                        Span(
                            cls="font-medium",
                            data_text=essay_draft.strip().split(js("/\\s+/")).length
                        ),
                        " | Characters: ",
                        Span(
                            cls="font-medium",
                            data_text=essay_draft.length
                        ),
                        cls="text-sm text-muted-foreground"
                    ),
                    cls="mt-2",
                    data_show=essay_draft.length > 0
                )
            ),
            cls="w-full"
        ),
        cls="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl mx-auto"
    )


@with_code
def character_counter_example():
    bio = Signal("bio", "")

    return Card(
        bio,
        CardHeader(
            CardTitle("Bio"),
            CardDescription("Tell us about yourself")
        ),
        CardContent(
            TextareaWithLabel(
                label="Your Bio",
                placeholder="Share your background, interests, and expertise...",
                rows=4,
                maxlength=280,
                signal=bio,
                helper_text="Max 280 characters"
            ),
            Div(
                Div(
                    Div(
                        cls="h-1 bg-primary rounded-full transition-all duration-300",
                        data_style_width=(bio.length >= 280).if_("100%", (bio.length / 280 * 100) + "%")
                    ),
                    cls="w-full bg-secondary rounded-full h-1"
                ),
                P(
                    Span(cls="font-mono font-medium", data_text=bio.length),
                    " / 280 characters",
                    cls="text-sm text-right",
                    data_attr_cls=switch([
                        (bio.length >= 280, "text-destructive"),
                        (bio.length >= 250, "text-orange-500")
                    ], default="text-muted-foreground")
                ),
                cls="space-y-2 mt-3"
            ),
            Button(
                "Save Bio",
                cls="w-full mt-4",
                data_attr_disabled=bio.length.eq(0)
            )
        ),
        cls="w-full max-w-3xl"
    )


@with_code
def comment_box_live_preview_example():
    comment_text = Signal("comment_text", "")

    def create_format_button(icon, action, title):
        return HTMLButton(
            Icon(icon, cls="h-4 w-4"),
            type="button",
            title=title,
            cls="p-2 rounded-md hover:bg-accent transition-colors border",
            data_on_click=js(action)
        )

    return Div(
        Card(
            comment_text,
            CardHeader(
                CardTitle("Comment Box with Live Preview"),
                CardDescription("Rich text editor with real-time preview")
            ),
            CardContent(
                Script(r"""
                    window.renderMd = (text) => {
                        if (!text) return '<span class="text-muted-foreground">Start typing to see a preview...</span>';
                        let html = text
                            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\*(.+?)\*/g, '<em>$1</em>')
                            .replace(/`([^`]+)`/g, '<code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">$1</code>')
                            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-primary underline">$1</a>')
                            .replace(/^> (.*$)/gim, '<blockquote class="border-l-4 border-gray-300 pl-4 italic">$1</blockquote>')
                            .replace(/^- (.*$)/gim, '<li>$1</li>')
                            .replace(/\n/g, '<br>');
                        return html.replace(/(<li>.*<\/li>(<br>)?)+/g, m => '<ul class="list-disc pl-5">' + m.replace(/<br>/g, '') + '</ul>');
                    };

                    window.fmt = (pre, suf, def, cursorPos) => {
                        const el = document.querySelector('[data-bind="comment_text"]');
                        if (!el) return;
                        const start = el.selectionStart, end = el.selectionEnd;
                        const sel = el.value.substring(start, end);
                        const txt = sel ? pre + sel + suf : pre + (def || '') + suf;
                        el.value = el.value.substring(0, start) + txt + el.value.substring(end);
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        setTimeout(() => {
                            el.focus();
                            if (cursorPos === 'link') {
                                const linkStart = start + txt.indexOf('](') + 2;
                                const linkEnd = start + txt.lastIndexOf(')');
                                el.setSelectionRange(linkStart, linkEnd);
                            } else {
                                el.setSelectionRange(start + txt.length, start + txt.length);
                            }
                        }, 10);
                    };
                """),
                Form(
                    # Stacked layout
                    Div(
                        # Editor section
                        Div(
                            # Formatting toolbar
                            Div(
                                Div(
                                    create_format_button("lucide:bold", "fmt('**', '**', 'bold text')", "Bold (Ctrl+B)"),
                                    create_format_button("lucide:italic", "fmt('*', '*', 'italic text')", "Italic (Ctrl+I)"),
                                    create_format_button("lucide:link", "fmt('[', '](https://example.com)', 'link text', 'link')", "Insert Link"),
                                    create_format_button("lucide:code", "fmt('`', '`', 'code')", "Inline Code"),
                                    create_format_button("lucide:list", "fmt('- ', '\\n', '')", "Bullet List"),
                                    create_format_button("lucide:quote", "fmt('> ', '\\n', 'Quote text')", "Quote"),
                                    cls="flex gap-1"
                                ),
                                P(
                                    cls="text-xs font-mono",
                                    data_attr_cls=switch([
                                        (comment_text.length >= 1000, "text-destructive"),
                                        (comment_text.length >= 500, "text-orange-500")
                                    ], default="text-muted-foreground"),
                                    data_text=comment_text.length + " characters"
                                ),
                                cls="flex items-center justify-between p-3 border rounded-t-md bg-muted/30 border-b-0"
                            ),

                            Textarea(
                                placeholder="What are your thoughts? Supports **bold**, *italic*, `code`, [links](url), lists, and > quotes",
                                rows=6,
                                signal=comment_text,
                                style="outline: none !important; box-shadow: none !important; border: none !important;",
                                cls="rounded-t-none border-t-0 min-h-[150px] resize-none focus:outline-none focus:ring-0 focus:border-input focus-visible:outline-none focus-visible:ring-0 focus-visible:border-input !border-none"
                            ),
                            cls="flex-1"
                        ),

                        Div(
                            Div(
                                P("Live Preview", cls="text-sm font-semibold mb-2"),
                                Div(
                                    cls="min-h-[150px] p-4 border rounded-md bg-background/50 prose prose-sm max-w-none overflow-auto whitespace-pre-wrap leading-relaxed",
                                    data_effect=js("el.innerHTML = renderMd($comment_text)")
                                )
                            ),
                            cls="w-full"
                        ),
                        cls="flex flex-col gap-4"
                    ),

                    Div(
                        Button(
                            Icon("lucide:x", cls="h-4 w-4 mr-2"),
                            "Cancel",
                            variant="outline",
                            type="button",
                            data_on_click=comment_text.set(''),
                            data_attr_disabled=comment_text.length.eq(0)
                        ),
                        Button(
                            Icon("lucide:send", cls="h-4 w-4 mr-2"),
                            "Post Comment",
                            type="submit",
                            data_attr_disabled=comment_text.length.eq(0),
                            data_on_click=js("""
                                evt.preventDefault();
                                if ($comment_text.trim().length > 0) {
                                    $comment_text = '';
                                }
                            """)
                        ),
                        cls="flex gap-3 justify-end mt-6"
                    )
                )
            ),
            cls="w-full max-w-6xl"
        ),
        cls="w-full"
    )


@with_code
def auto_expanding_textarea_example():
    auto_expand = Signal("auto_expand", "")

    return Card(
        auto_expand,
        CardHeader(
            CardTitle("Auto-Expanding"),
            CardDescription("Grows with your content")
        ),
        CardContent(
            TextareaWithLabel(
                label="Message",
                placeholder="Start typing and watch it grow...",
                signal=auto_expand,
                helper_text="This textarea expands as you type",
                cls="[&_textarea]:field-sizing-content [&_textarea]:min-h-[60px] [&_textarea]:max-h-[300px]"
            ),
            P(
                "Lines: ",
                Span(
                    cls="font-mono font-medium",
                    data_text=auto_expand.split('\n').length
                ),
                cls="text-sm text-muted-foreground mt-2"
            )
        ),
        cls="w-full max-w-3xl"
    )


@with_code
def enhanced_feedback_form_example():
    feedback = Signal("feedback", "")
    suggestions = Signal("suggestions", "")
    feedback_rating = Signal("feedback_rating", 0)
    hover_rating = Signal("hover_rating", 0)
    feedback_submitted = Signal("feedback_submitted", False)

    return Card(
        feedback,
        suggestions,
        feedback_rating,
        hover_rating,
        feedback_submitted,
        CardHeader(
            CardTitle("Customer Feedback"),
            CardDescription("Help us improve our service")
        ),
        CardContent(
            Form(
                TextareaWithLabel(
                    label="How was your experience?",
                    placeholder="Tell us what you think...",
                    required=True,
                    rows=4,
                    signal=feedback,
                    error_text=None,
                    helper_text="Share your honest thoughts (10-1000 characters)"
                ),
                Div(
                    P(
                        "Feedback is required",
                        cls="text-sm text-destructive"
                    ),
                    data_show=feedback_submitted & feedback.strip().length.eq(0)
                ),
                Div(
                    P(
                        "Please provide at least 10 characters",
                        cls="text-sm text-destructive"
                    ),
                    data_show=feedback_submitted & (feedback.strip().length > 0) & (feedback.length < 10)
                ),
                Div(
                    P(
                        "Feedback cannot exceed 1000 characters",
                        cls="text-sm text-destructive"
                    ),
                    data_show=feedback.length > 1000
                ),
                Div(
                    P(
                        "Rate your experience",
                        cls="text-sm font-medium mb-3"
                    ),
                    Div(
                        *[
                            HTMLButton(
                                "★",
                                type="button",
                                cls="text-3xl transition-colors",
                                data_attr_cls=((feedback_rating >= i+1) | (hover_rating >= i+1)).if_("text-yellow-500", "text-gray-300"),
                                data_on_click=feedback_rating.toggle(i+1, 0),
                                data_on_mouseenter=hover_rating.set(i+1),
                                data_on_mouseleave=hover_rating.set(0)
                            )
                            for i in range(5)
                        ],
                        cls="flex gap-1 mb-2"
                    ),
                    P(
                        "Rating: ",
                        Span(
                            cls="font-medium",
                            data_text=(feedback_rating > 0).if_(feedback_rating, "Not selected")
                        ),
                        cls="text-sm text-muted-foreground"
                    ),
                    cls="border rounded-lg p-4 bg-muted/30 my-6"
                ),
                TextareaWithLabel(
                    label="Additional suggestions",
                    placeholder="Any specific improvements you'd like to see? (optional)",
                    rows=3,
                    signal=suggestions,
                    helper_text="This helps us prioritize improvements"
                ),
                Div(
                    Badge(
                        Icon("lucide:clock", cls="h-3 w-3 mr-1"),
                        "Draft",
                        variant="secondary",
                        data_show=(feedback.strip().length > 0) & (feedback.length < 10)
                    ),
                    Badge(
                        Icon("lucide:check-circle", cls="h-3 w-3 mr-1"),
                        "Ready to submit",
                        variant="default",
                        data_show=(feedback.length >= 10) & (feedback.length <= 1000) & feedback_rating.eq(0)
                    ),
                    Badge(
                        Icon("lucide:star", cls="h-3 w-3 mr-1"),
                        "Complete",
                        variant="default",
                        data_show=(feedback.length >= 10) & (feedback_rating > 0)
                    ),
                    cls="flex flex-wrap gap-2 mb-4"
                ),
                Div(
                    Button(
                        "Clear Form",
                        variant="outline",
                        type="button",
                        data_on_click=[
                            feedback.set(''),
                            suggestions.set(''),
                            feedback_rating.set(0),
                            hover_rating.set(0),
                            feedback_submitted.set(False),
                        ],
                        data_attr_disabled=feedback.length.eq(0) & suggestions.length.eq(0) & feedback_rating.eq(0)
                    ),
                    Button(
                        Icon("lucide:send", cls="h-4 w-4 mr-2"),
                        "Submit Feedback",
                        type="submit",
                        data_attr_disabled=(feedback.length < 10) | feedback_rating.eq(0) | (feedback.length > 1000),
                        data_on_click=[
                            dict(prevent=True),
                            feedback_submitted.set(True),
                            ((feedback.length >= 10) & (feedback_rating > 0) & (feedback.length <= 1000)).then(
                                seq(
                                    js("alert(`Thank you for your ${$feedback_rating}-star feedback!`)"),
                                    feedback.set(''),
                                    suggestions.set(''),
                                    feedback_rating.set(0),
                                    feedback_submitted.set(False)
                                )
                            )
                        ]
                    ),
                    cls="flex gap-2 justify-end"
                )
            )
        ),
        cls="w-full max-w-3xl"
    )


@with_code
def code_editor_textarea_example():
    code_editor = Signal("code_editor", "def hello_world():\n    print('Hello, World!')\n    return True")
    code_copied = Signal("code_copied", False)

    return Card(
        code_editor,
        code_copied,
        CardHeader(
            CardTitle("Code Editor"),
            CardDescription("Write and format code")
        ),
        CardContent(
            Div(
                Div(
                    P("Language: ", cls="text-sm text-muted-foreground"),
                    Badge("Python", variant="outline"),
                    cls="flex items-center justify-between mb-2"
                ),
                Textarea(
                    placeholder="# Enter your code here...",
                    signal=code_editor,
                    rows=8,
                    cls="font-mono text-sm",
                    resize="vertical"
                ),
                Div(
                    P(
                        "Lines: ",
                        Span(
                            cls="font-mono",
                            data_text=code_editor.split('\n').length
                        ),
                        " | Characters: ",
                        Span(
                            cls="font-mono",
                            data_text=code_editor.length
                        ),
                        cls="text-xs text-muted-foreground"
                    ),
                    Button(
                        Span(Icon("lucide:check", cls="h-4 w-4 mr-2"), data_show=code_copied),
                        Span(Icon("lucide:copy", cls="h-4 w-4 mr-2"), data_show=code_copied.eq(False)),
                        Span("Copied!", data_show=code_copied),
                        Span("Copy", data_show=code_copied.eq(False)),
                        size="sm",
                        variant="outline",
                        data_on_click=clipboard(code_editor, signal=code_copied)
                    ),
                    cls="flex items-center justify-between mt-2"
                )
            )
        ),
        cls="w-full max-w-3xl"
    )


@with_code
def email_template_composer_example():
    email_subject = Signal("email_subject", "Welcome to {{company_name}}, {{first_name}}!")
    email_body = Signal("email_body", "Hi {{first_name}},\n\nWelcome to {{company_name}}! We're excited to have you on board.\n\nBest regards,\n{{sender_name}}")

    def create_variable_button(var_name):
        return HTMLButton(
            f"{{{{{var_name}}}}}",
            type="button",
            cls="px-2 py-1 text-xs bg-muted hover:bg-accent rounded border",
            data_on_click=js("insertVariable")(var_name)
        )

    return Card(
        email_subject,
        email_body,
        CardHeader(
            CardTitle("Email Template Composer"),
            CardDescription("Create professional email templates with variables")
        ),
        CardContent(
            Form(
                Div(
                    TextareaWithLabel(
                        label="Subject Line",
                        placeholder="Welcome to {{company_name}}, {{first_name}}!",
                        rows=1,
                        signal=email_subject,
                        helper_text="Use {{variable}} syntax for dynamic content",
                        wrap="soft"
                    ),
                    cls="mb-4"
                ),
                TextareaWithLabel(
                    label="Email Body",
                    placeholder="Hi {{first_name}},\n\nWelcome to {{company_name}}! We're excited to have you on board.\n\nBest regards,\n{{sender_name}}",
                    rows=8,
                    signal=email_body,
                    helper_text="Available variables: {{first_name}}, {{last_name}}, {{company_name}}, {{sender_name}}",
                    wrap="soft"
                ),

                # Variable insertion toolbar with script for cursor position
                Script(r"""
                    let lastFocused = null;

                    window.previewVars = (text) => text ? text.replace(/{{([^}]+)}}/g, (m,p1) => '[' + p1 + ']') : '';

                    document.addEventListener('DOMContentLoaded', () => {
                        const body = document.querySelector('[data-bind="email_body"]');
                        const subject = document.querySelector('[data-bind="email_subject"]');

                        [body, subject].forEach(el => {
                            if (el) el.addEventListener('focus', () => lastFocused = el);
                        });

                        lastFocused = body;
                    });

                    window.insertVariable = (varName) => {
                        const target = lastFocused || document.querySelector('[data-bind="email_body"]');
                        if (!target) return;

                        const start = target.selectionStart;
                        const variable = `{{${varName}}}`;
                        target.value = target.value.substring(0, start) + variable + target.value.substring(target.selectionEnd);
                        target.dispatchEvent(new Event('input', {bubbles: true}));

                        setTimeout(() => {
                            target.focus();
                            target.setSelectionRange(start + variable.length, start + variable.length);
                        }, 10);
                    };
                """),
                Div(
                    P("Quick Variables:", cls="text-sm font-medium mb-2"),
                    Div(
                        create_variable_button("first_name"),
                        create_variable_button("last_name"),
                        create_variable_button("company_name"),
                        create_variable_button("sender_name"),
                        cls="flex flex-wrap gap-2"
                    ),
                    cls="p-3 border rounded-md bg-muted/30 mb-4"
                ),

                Div(
                    P("Preview", cls="text-sm font-medium mb-2"),
                    Div(
                        Div(
                            P("Subject:", cls="text-xs text-muted-foreground"),
                            P(
                                cls="font-medium text-sm mb-2",
                                data_text=js("previewVars")(email_subject.or_("No subject"))
                            ),
                            Separator(cls="my-2"),
                            P(
                                cls="text-sm whitespace-pre-wrap",
                                data_text=js("previewVars")(email_body.or_("No content"))
                            )
                        ),
                        cls="p-3 bg-background border rounded-md min-h-[120px]"
                    ),
                    P("Variables will be replaced with actual values when sent", cls="text-xs text-muted-foreground mt-1"),
                    cls="mb-4",
                    data_show=(email_subject.length > 0) | (email_body.length > 0)
                ),

                Div(
                    Button(
                        Icon("lucide:eye", cls="h-4 w-4 mr-2"),
                        "Test Send",
                        variant="outline",
                        type="button",
                        data_attr_disabled=email_subject.length.eq(0) | email_body.length.eq(0),
                        data_on_click=js("alert('Test email sent to your email address!')")
                    ),
                    Button(
                        Icon("lucide:save", cls="h-4 w-4 mr-2"),
                        "Save Template",
                        type="submit",
                        data_attr_disabled=email_subject.length.eq(0) | email_body.length.eq(0),
                        data_on_click=js("""
                            evt.preventDefault();
                            alert('Template saved successfully!');
                        """)
                    ),
                    cls="flex gap-2 justify-end"
                )
            )
        ),
        cls="w-full max-w-3xl"
    )


EXAMPLES_DATA = [
    {"title": "Basic Textarea", "description": "Simple textarea with different states", "fn": basic_textarea_example},
    {"title": "Contextual Usage", "description": "Textarea sizes matched to specific use cases", "fn": contextual_textarea_examples},
    {"title": "Character Counter", "description": "Track character count with visual feedback", "fn": character_counter_example},
    {"title": "Comment Box with Live Preview", "description": "Rich text editor with real-time preview and formatting toolbar", "fn": comment_box_live_preview_example},
    {"title": "Auto-Expanding", "description": "Textarea that grows with content", "fn": auto_expanding_textarea_example},
    {"title": "Feedback Form", "description": "Multi-field form with validation", "fn": enhanced_feedback_form_example},
    {"title": "Code Editor", "description": "Code input with monospace font and utilities", "fn": code_editor_textarea_example},
    {"title": "Email Template Composer", "description": "Professional template system with variable substitution", "fn": email_template_composer_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("placeholder", "str | None", "Placeholder text shown when empty", "None"),
        Prop("value", "str | None", "Initial text value", "None"),
        Prop("signal", "str | None", "Datastar signal for two-way binding", "None"),
        Prop("rows", "int | None", "Number of visible text rows", "None"),
        Prop("maxlength", "int | None", "Maximum number of characters", "None"),
        Prop("resize", "Literal['none','both','horizontal','vertical'] | None", "Controls textarea resizing behavior", "None"),
        Prop("disabled", "bool", "Whether the textarea is disabled", "False"),
        Prop("required", "bool", "Whether the textarea is required", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_textarea_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)