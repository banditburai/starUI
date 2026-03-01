TITLE = "Select"
DESCRIPTION = "Displays a list of options for the user to pick from—triggered by a button."
CATEGORY = "form"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Code, Label, Form, Signal, js
from starui.registry.components.select import (
    Select, SelectTrigger, SelectValue, SelectContent, SelectItem,
    SelectLabel, SelectSeparator, SelectWithLabel
)
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def default_example():
    status_value = Signal("status_value", "")
    return Div(
        status_value,
        Select(
            SelectTrigger(
                SelectValue(placeholder="Set status"),
                cls="w-[200px]",
                aria_label="Set status",
            ),
            SelectContent(
                SelectLabel("Active"),
                SelectItem("Draft", value="draft"),
                SelectItem("In Review", value="review"),
                SelectItem("Published", value="published"),
                SelectSeparator(),
                SelectLabel("Closed"),
                SelectItem("Archived", value="archived"),
            ),
            signal="status",
        ),
        P(
            "Selected: ",
            Code(data_text=status_value.or_("none")),
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-sm"
    )


@with_code
def grouped_options_example():
    return SelectWithLabel(
        label="Timezone",
        options=[
            {"group": "North America", "items": [
                ("est", "Eastern Time (EST)"),
                ("cst", "Central Time (CST)"),
                ("mst", "Mountain Time (MST)"),
                ("pst", "Pacific Time (PST)")
            ]},
            {"group": "Europe", "items": [
                ("gmt", "Greenwich Mean Time (GMT)"),
                ("cet", "Central European Time (CET)"),
                ("eet", "Eastern European Time (EET)")
            ]},
            {"group": "Asia", "items": [
                ("jst", "Japan Standard Time (JST)"),
                ("cst_china", "China Standard Time (CST)"),
                ("ist", "India Standard Time (IST)")
            ]}
        ],
        value="pst",
        placeholder="Select a timezone",
        select_cls="w-[240px]"
    )


@with_code
def states_example():
    return Div(
        SelectWithLabel(
            label="Placeholder",
            options=["Option A", "Option B", "Option C"],
            placeholder="Pick one...",
        ),
        SelectWithLabel(
            label="Disabled",
            options=["Option A", "Option B", "Option C"],
            value="Option B",
            disabled=True,
        ),
        SelectWithLabel(
            label="Required",
            options=["Option A", "Option B", "Option C"],
            placeholder="Pick one...",
            required=True,
        ),
        SelectWithLabel(
            label="Error",
            options=["Option A", "Option B", "Option C"],
            error_text="Please select an option",
            disabled=True,
        ),
        cls="grid w-full max-w-sm gap-6"
    )


@with_code
def form_example():
    template_value = Signal("project_template_value", "")
    return Card(
        CardHeader(
            CardTitle("New Project"),
            CardDescription("Choose a starting template and visibility")
        ),
        CardContent(
            Form(
                template_value,
                SelectWithLabel(
                    label="Template",
                    options=[
                        ("blank", "Blank"),
                        ("blog", "Blog"),
                        ("dashboard", "Dashboard"),
                        ("api", "API"),
                    ],
                    placeholder="Select a template",
                    required=True,
                    signal="project_template",
                    select_cls="w-full"
                ),
                SelectWithLabel(
                    label="Visibility",
                    options=[
                        ("public", "Public"),
                        ("private", "Private"),
                        ("team", "Team"),
                    ],
                    value="private",
                    helper_text="Controls who can see this project",
                    select_cls="w-full"
                ),
                Button(
                    "Create Project",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=~template_value,
                    data_on_click=(js("alert(`Template: ${$project_template_label}`)"), dict(prevent=True))
                ),
                cls="space-y-4"
            )
        ),
        cls="max-w-md"
    )


@with_code
def dependent_selects_example():
    make_value = Signal("vehicle_make_value", "")
    make_label = Signal("vehicle_make_label", "")
    model_value = Signal("vehicle_model_value", "")
    model_label = Signal("vehicle_model_label", "")

    invalid_toyota = (make_value == "toyota") & ~((model_value == "camry") | (model_value == "corolla") | (model_value == "rav4"))
    invalid_honda = (make_value == "honda") & ~((model_value == "civic") | (model_value == "accord") | (model_value == "crv"))
    invalid_ford = (make_value == "ford") & ~((model_value == "mustang") | (model_value == "f150") | (model_value == "explorer"))
    should_clear = ~make_value | invalid_toyota | invalid_honda | invalid_ford

    return Card(
        CardHeader(
            CardTitle("Vehicle Selection"),
            CardDescription("Choose a make and model")
        ),
        CardContent(
            Div(
                make_value, make_label, model_value, model_label,
                SelectWithLabel(
                    label="Make",
                    options=[
                        ("toyota", "Toyota"),
                        ("honda", "Honda"),
                        ("ford", "Ford"),
                    ],
                    placeholder="Select make",
                    signal="vehicle_make",
                    select_cls="w-full"
                ),
                Div(
                    Label("Model", fr="vehicle_model_trigger", cls="block text-sm font-medium mb-1.5"),
                    Select(
                        SelectTrigger(
                            SelectValue(placeholder="Select model"),
                            data_attr_disabled=~make_value,
                            cls="w-full",
                            id="vehicle_model_trigger",
                        ),
                        SelectContent(
                            Div(
                                SelectItem("Camry", value="camry"),
                                SelectItem("Corolla", value="corolla"),
                                SelectItem("RAV4", value="rav4"),
                                data_show=make_value == "toyota"
                            ),
                            Div(
                                SelectItem("Civic", value="civic"),
                                SelectItem("Accord", value="accord"),
                                SelectItem("CR-V", value="crv"),
                                data_show=make_value == "honda"
                            ),
                            Div(
                                SelectItem("Mustang", value="mustang"),
                                SelectItem("F-150", value="f150"),
                                SelectItem("Explorer", value="explorer"),
                                data_show=make_value == "ford"
                            ),
                        ),
                        signal="vehicle_model"
                    ),
                    cls="space-y-1.5"
                ),
                P(
                    "Selected: ",
                    Code(data_text=make_label + " " + model_label),
                    cls="text-sm text-muted-foreground mt-2",
                    data_show=make_value & model_value
                ),
                data_effect=[
                    model_value.set(should_clear.if_("", model_value)),
                    model_label.set(should_clear.if_("", model_label))
                ],
                cls="space-y-4"
            )
        ),
        cls="w-full max-w-md"
    )


@with_code
def inline_selects_example():
    font_value = Signal("inline_font_value", "sans")
    size_value = Signal("inline_size_value", "medium")
    return Div(
        font_value, size_value,
        Div(
            SelectWithLabel(
                label="Font",
                options=[
                    ("sans", "Sans"),
                    ("serif", "Serif"),
                    ("mono", "Mono"),
                ],
                value="sans",
                signal="inline_font",
                select_cls="w-[120px]"
            ),
            SelectWithLabel(
                label="Size",
                options=[
                    ("small", "Small"),
                    ("medium", "Medium"),
                    ("large", "Large"),
                ],
                value="medium",
                signal="inline_size",
                select_cls="w-[120px]"
            ),
            cls="flex gap-4"
        ),
        P(
            Code(data_text=font_value),
            " / ",
            Code(data_text=size_value),
            cls="text-sm text-muted-foreground mt-3"
        ),
    )


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Bare Select API with labels, separator, and reactive signal display"},
    {"fn": grouped_options_example, "title": "Grouped Options", "description": "Convenience wrapper organizing options into labeled groups"},
    {"fn": states_example, "title": "States", "description": "Disabled, required, and error states"},
    {"fn": form_example, "title": "Form Integration", "description": "Project creation form with required fields and conditional submit"},
    {"fn": dependent_selects_example, "title": "Dependent Selects", "description": "Cascading selects where child options depend on parent selection"},
    {"fn": inline_selects_example, "title": "Inline Selects", "description": "Side-by-side selects with immediate effect, no form submission"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Select", "Main container managing selected state via Datastar signals"),
        Component("SelectTrigger", "Button that opens the dropdown menu"),
        Component("SelectValue", "Displays current selection or placeholder"),
        Component("SelectContent", "Dropdown panel listing available items"),
        Component("SelectItem", "Individual selectable option with value and label"),
        Component("SelectGroup", "Group related options for easier scanning"),
        Component("SelectLabel", "Label heading for a group of options"),
        Component("SelectSeparator", "Visual divider between items or groups"),
        Component("SelectWithLabel", "Convenience wrapper with label, helper, and error text")
    ]
)


def create_select_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
