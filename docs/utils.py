import inspect
import re
from dataclasses import dataclass
from functools import wraps
from textwrap import dedent
from typing import Any, Callable

# Explicit imports to preserve Python built-ins (any, all, match, etc.)
# since utils.py contains Python logic alongside HTML generation
from starhtml import (
    Div, H2, H3, P, Table, Thead, Tbody, Tr, Th, Td, Code, FT
)
from widgets.installation_section import InstallationSection
from widgets.code_block import CodeBlock


# ============================================================================
# MAIN API
# ============================================================================

def auto_generate_page(
    component_name: str,
    description: str,
    examples: list[Any],
    cli_command: str | None = None,
    manual_files: list[dict[str, str]] | None = None,
    dependencies: list[str] | None = None,
    usage_code: str | None = None,
    usage_description: str | None = None,
    api_reference: dict[str, Any] | None = None,
    hero_example: Any | None = None,
    hero_example_code: str | None = None,
    examples_data: list[dict[str, str]] | None = None,
    component_slug: str | None = None,
    **layout_attrs
) -> FT:
    from layouts.base import DocsLayout, LayoutConfig, SidebarConfig
    from app import DOCS_SIDEBAR_SECTIONS

    sections = [
        hero_example,
        _installation(cli_command, manual_files, dependencies),
        _examples(examples),
        _usage(usage_code, usage_description),
        _api_reference(api_reference)
    ]

    return DocsLayout(
        Div(*filter(None, sections)),
        layout=LayoutConfig(
            title=component_name,
            description=description,
            component_name=component_slug,
        ),
        sidebar=SidebarConfig(sections=DOCS_SIDEBAR_SECTIONS),
        **layout_attrs
    )


# ============================================================================
# SECTIONS
# ============================================================================

def _installation(cli_command, manual_files, dependencies):
    if not any([cli_command, manual_files, dependencies]):
        return None
    return InstallationSection(
        cli_command=cli_command,
        manual_files=manual_files,
        dependencies=dependencies,
        cls="my-8"
    )


def _examples(examples: list[Any]) -> FT | None:
    if not examples:
        return None
    return Div(
        H2("Examples", cls="text-2xl font-bold tracking-tight mb-6 mt-12"),
        Div(*examples)
    )


def _usage(code: str | None, description: str | None = None) -> FT | None:
    if not code:
        return None
    return Div(
        H2("Usage", cls="text-2xl font-bold tracking-tight mb-4 mt-12"),
        P(description, cls="text-muted-foreground mb-4") if description else "",
        CodeBlock(code, language="python"),
        cls="space-y-4"
    )


def _api_reference(api_ref: dict[str, Any] | None) -> FT | None:
    """
    API reference section with intentional table selection.

    Design philosophy:
    - Simple components (Button, Input): Show props table
    - Composite components (AlertDialog, Accordion): Show components table OR props table
    - Decision is made per-component based on what users need most
    """
    if not api_ref:
        return None

    props = api_ref.get("props", [])
    components = api_ref.get("api", api_ref.get("components", []))

    if not (props or components):
        return None

    tables = filter(None, [
        _props_table(props) if props else None,
        _api_items_table(components) if components else None
    ])

    return Div(
        H2("API Reference", cls="text-2xl font-bold tracking-tight mb-6 mt-12"),
        *tables,
        cls="space-y-6"
    )


# ============================================================================
# TABLES
# ============================================================================

def _props_table(props: list[dict]) -> FT | None:
    if not props:
        return None

    return Div(
        H3("Props", cls="text-lg font-semibold mb-4"),
        _table(
            ["Prop", "Type", "Default", "Description"],
            [[
                Code(p["name"], cls="text-sm font-mono font-medium"),
                Code(p["type"], cls="text-xs font-mono text-muted-foreground"),
                Code(p.get("default", "-"), cls="text-xs font-mono text-muted-foreground"),
                p.get("description", "")
            ] for p in props]
        ),
        cls="overflow-x-auto"
    )


def _api_items_table(items: list[dict]) -> FT | None:
    if not items:
        return None

    # Only show Type column if items actually have non-empty type information
    # (not for component lists that just have name + description)
    has_type = any(item.get("type") for item in items)
    headers = ["Name", "Type", "Description"] if has_type else ["Component", "Description"]

    rows = [[
        Code(item["name"], cls="text-sm font-mono font-medium"),
        Code(item.get("type", ""), cls="text-xs font-mono text-muted-foreground") if has_type else None,
        item.get("description", "")
    ] for item in items]

    # Filter out None cells (when has_type is False)
    rows = [[cell for cell in row if cell is not None] for row in rows]

    return _table(headers, rows)


def _table(headers: list[str], rows: list[list]) -> FT:
    header_cls = "px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider"
    cell_cls = "px-6 py-4"

    return Div(
        Table(
            Thead(
                Tr(*[Th(h, cls=header_cls) for h in headers], cls="bg-muted/50")
            ),
            Tbody(
                *[Tr(
                    *[Td(cell, cls=f"{cell_cls} {getattr(cell, 'attrs', {}).get('cls', '')}")
                      for cell in row],
                    cls="border-t border-border"
                ) for row in rows],
                cls="divide-y divide-border"
            ),
            cls="w-full"
        ),
        cls="overflow-hidden rounded-lg border border-border"
    )


# ============================================================================
# MARKDOWN
# ============================================================================

def generate_component_markdown(
    component_name: str,
    description: str,
    examples_data: list[dict[str, str]],
    cli_command: str | None = None,
    usage_code: str | None = None,
    api_reference: dict[str, Any] | None = None,
    hero_example_code: str | None = None,
) -> str:
    sections = filter(None, [
        f"# {component_name}\n\n{description}",
        f"## Preview\n\n```python\n{hero_example_code}\n```" if hero_example_code else None,
        f"## Installation\n\n```bash\n{cli_command}\n```" if cli_command else None,
        _markdown_examples(examples_data),
        f"## Usage\n\n```python\n{usage_code}\n```" if usage_code else None,
        _markdown_props(api_reference)
    ])

    return "\n\n".join(sections)


def _markdown_examples(examples: list[dict[str, str]] | None) -> str | None:
    if not examples:
        return None

    parts = ["## Examples"]
    for ex in examples:
        if title := ex.get("title"):
            parts.append(f"### {title}")
        if desc := ex.get("description"):
            parts.append(desc)
        if code := ex.get("code"):
            parts.append(f"```python\n{code}\n```")

    return "\n\n".join(parts)


def _markdown_props(api_ref: dict[str, Any] | None) -> str | None:
    if not api_ref:
        return None

    # Handle components table
    if "components" in api_ref:
        lines = [
            "## API Reference",
            "",
            "| Component | Description |",
            "|-----------|-------------|"
        ]

        for comp in api_ref["components"]:
            lines.append(
                f"| `{comp.get('name', '')}` | "
                f"{comp.get('description', '')} |"
            )

        return "\n".join(lines)

    # Handle props table
    if "props" in api_ref:
        lines = [
            "## API Reference",
            "",
            "| Prop | Type | Default | Description |",
            "|------|------|---------|-------------|"
        ]

        for p in api_ref["props"]:
            lines.append(
                f"| `{p.get('name', '')}` | "
                f"`{p.get('type', '')}` | "
                f"`{p.get('default', '')}` | "
                f"{p.get('description', '')} |"
            )

        return "\n".join(lines)

    return None


# ============================================================================
# CODE EXTRACTION
# ============================================================================

def extract_code(func: Callable) -> str:
    """
    Extract code from function body.

    Supports directives:
    - #: hide - Exclude line from output
    - #: include function_name() - Inline function body
    """
    try:
        source = dedent(inspect.getsource(func))
        lines = source.split('\n')

        body_start = next(
            (i + 1 for i, line in enumerate(lines)
             if line.strip().startswith('def ') and func.__name__ in line),
            0
        )

        body_lines = lines[body_start:]

        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)

        if not body_lines:
            return "# Could not extract function body"

        base_indent = len(body_lines[0]) - len(body_lines[0].lstrip())
        normalized = [
            line[base_indent:] if line.strip() and line.startswith(' ' * base_indent)
            else line.lstrip() if line.strip()
            else ''
            for line in body_lines
        ]

        processed = []
        for line in normalized:
            if line.rstrip().endswith('#: hide'):
                continue

            if match := re.search(r'#: include (\w+)\(\)', line):
                func_name = match.group(1)
                frame = inspect.currentframe()
                if frame and frame.f_back and frame.f_back.f_back:
                    caller_globals = frame.f_back.f_back.f_globals
                    if func_name in caller_globals:
                        included_code = _extract_function_body(caller_globals[func_name])
                        if included_code:
                            indent = len(line) - len(line.lstrip())
                            for inc_line in included_code.split('\n'):
                                if inc_line.strip():
                                    processed.append(' ' * indent + inc_line)
                                else:
                                    processed.append('')
                            continue

            processed.append(line)

        has_inner_def = any('def ' in line for line in processed[1:])
        first_code = next((line for line in processed if line.strip()), '')

        if first_code.strip().startswith('return ') and not has_inner_def:
            return_idx = next(
                (i for i, line in enumerate(processed)
                 if line.strip().startswith('return ')),
                -1
            )
            if return_idx >= 0:
                result = processed[return_idx:]
                if result:
                    first = result[0]
                    indent = len(first) - len(first.lstrip())
                    result[0] = ' ' * indent + first.lstrip()[7:]
                return '\n'.join(line.rstrip() for line in result)
        else:
            # Only strip 'return' from base-level returns (indent 0), not nested ones
            result = [
                ' ' * (len(line) - len(line.lstrip())) + line.lstrip()[7:]
                if line.strip().startswith('return ') and (len(line) - len(line.lstrip())) == 0
                else line
                for line in processed
            ]
            return '\n'.join(line.rstrip() for line in result)

    except Exception as e:
        return f"# Error: {e}"


def _extract_function_body(func: Callable) -> str:
    try:
        source = dedent(inspect.getsource(func))
        lines = source.split('\n')

        body_start = next(
            (i + 1 for i, line in enumerate(lines)
             if 'def ' in line and func.__name__ in line and ':' in line),
            0
        )

        body_lines = lines[body_start:]

        clean_lines = []
        in_docstring = False
        for line in body_lines:
            stripped = line.strip()
            if stripped.startswith(('"""', "'''")):
                quotes = '"""' if '"""' in stripped else "'''"
                if in_docstring or stripped.count(quotes) >= 2:
                    in_docstring = not in_docstring
                    continue
                in_docstring = True
            elif not in_docstring:
                clean_lines.append(line)

        body_lines = clean_lines

        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)

        if not body_lines:
            return ""

        base_indent = len(body_lines[0]) - len(body_lines[0].lstrip())
        normalized = [
            line[base_indent:] if line.strip() and len(line) >= base_indent and line[:base_indent].isspace()
            else line.lstrip() if line.strip()
            else ''
            for line in body_lines
        ]

        return '\n'.join(line.rstrip() for line in normalized)

    except Exception:
        return ""


def with_code(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.code = extract_code(func)
    return wrapper


# ============================================================================
# API REFERENCE BUILDERS
# ============================================================================

@dataclass
class Prop:
    name: str
    type: str
    description: str
    default: str | None = None

@dataclass
class Component:
    name: str
    description: str
    props: list[Prop] = None

    def __post_init__(self):
        if self.props is None:
            self.props = []

def build_api_reference(main_props: list[Prop] = None, components: list[Component] = None) -> dict:
    """
    Build API reference from typed objects.

    Design: Choose either main_props OR components based on what's most useful:
    - main_props: For simple components (Button, Input)
    - components: For composite components (AlertDialog, Accordion)
    """
    result = {}

    if main_props:
        result["props"] = [
            {
                "name": p.name,
                "type": p.type,
                "description": p.description,
                **({"default": p.default} if p.default is not None else {})
            }
            for p in main_props
        ]

    if components:
        result["components"] = [
            {
                "name": comp.name,
                "description": comp.description,
                **({"props": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "description": p.description,
                        **({"default": p.default} if p.default is not None else {})
                    }
                    for p in comp.props
                ]} if comp.props else {})
            }
            for comp in components
        ]

    return result
