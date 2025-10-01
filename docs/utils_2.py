"""Documentation utilities for StarUI components."""

import inspect
import re
from functools import wraps
from textwrap import dedent
from typing import Any, Callable

from starhtml import *
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
    """Auto-generate a component documentation page."""
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
    """Installation section."""
    if not any([cli_command, manual_files, dependencies]):
        return None
    return InstallationSection(
        cli_command=cli_command,
        manual_files=manual_files,
        dependencies=dependencies,
        cls="my-8"
    )


def _examples(examples: list[Any]) -> FT | None:
    """Examples section."""
    if not examples:
        return None
    return Div(
        H2("Examples", cls="text-2xl font-bold tracking-tight mb-6 mt-12"),
        Div(*examples)
    )


def _usage(code: str | None, description: str | None = None) -> FT | None:
    """Usage section."""
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
    components = api_ref.get("components", [])
    
    if not (props or components):
        return None
    
    # Intentionally show either props OR components table, not both
    # The choice depends on what's most valuable for that specific component
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
    """Props table."""
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
    """API items/components table."""
    if not items:
        return None
    
    has_type = any("type" in item for item in items)
    headers = ["Name", "Type", "Description"] if has_type else ["Component", "Description"]
    
    rows = [[
        Code(item["name"], cls="text-sm font-mono font-medium"),
        Code(item.get("type", ""), cls="text-xs font-mono text-muted-foreground") if has_type else None,
        item.get("description", "")
    ] for item in items]
    
    # Filter out None values for tables without type column
    rows = [[cell for cell in row if cell is not None] for row in rows]
    
    return _table(headers, rows)


def _table(headers: list[str], rows: list[list]) -> FT:
    """Create a styled table."""
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
    """Generate markdown documentation."""
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
    """Format examples for markdown."""
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
    """Format props table for markdown."""
    if not api_ref or "props" not in api_ref:
        return None
    
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


# ============================================================================
# API REFERENCE BUILDERS
# ============================================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class Prop:
    """Represents a component prop for API documentation."""
    name: str
    type: str
    description: str
    default: Optional[str] = None

@dataclass 
class Component:
    """Represents a component for API documentation."""
    name: str
    description: str
    props: list[Prop] = None
    
    def __post_init__(self):
        if self.props is None:
            self.props = []

def build_api_reference(main_props: list[Prop] = None, components: list[Component] = None) -> dict:
    """
    Build API reference dict from typed objects.
    
    Design note: Intentionally choose either main_props OR components, not both.
    - main_props: For simple components where users need to understand parameters
    - components: For composite components where users need to understand structure
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
        result["components"] = []
        for comp in components:
            comp_dict = {
                "name": comp.name,
                "description": comp.description
            }
            # Note: We generally don't show component props in the table
            # since that creates too much detail. Component structure is the focus.
            if comp.props:
                comp_dict["props"] = [
                    {
                        "name": p.name,
                        "type": p.type,
                        "description": p.description,
                        **({"default": p.default} if p.default is not None else {})
                    }
                    for p in comp.props
                ]
            result["components"].append(comp_dict)
    
    return result


# ============================================================================
# CODE EXTRACTION
# ============================================================================

def extract_code(func: Callable) -> str:
    """Extract and normalize code from function body, handling both patterns."""
    try:
        source = dedent(inspect.getsource(func))
        lines = source.split('\n')
        
        # Find where the actual function body starts
        body_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and func.__name__ in line:
                body_start = i + 1
                break
        
        # Get everything after the function definition
        body_lines = lines[body_start:]
        
        # Remove empty lines at the start
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        
        if not body_lines:
            return "# Could not extract function body"
        
        # Find the base indentation level
        first_line = body_lines[0]
        base_indent = len(first_line) - len(first_line.lstrip())
        
        # Remove the base indentation from all lines
        normalized_lines = []
        for line in body_lines:
            if line.strip():
                if line.startswith(' ' * base_indent):
                    normalized_lines.append(line[base_indent:])
                else:
                    normalized_lines.append(line.lstrip())
            else:
                normalized_lines.append('')
        
        # Check if this is a simple return-only function (old pattern)
        # Old pattern: starts with 'return' and has no 'def' statements
        has_inner_def = any('def ' in line for line in normalized_lines[1:])  # Skip first line check
        first_code_line = next((line for line in normalized_lines if line.strip()), '')
        
        if first_code_line.strip().startswith('return ') and not has_inner_def:
            # Old pattern: just a return statement, extract what's being returned
            # Find where return starts
            return_index = 0
            for i, line in enumerate(normalized_lines):
                if line.strip().startswith('return '):
                    return_index = i
                    break
            
            # Get the return statement and everything after
            return_lines = normalized_lines[return_index:]
            # Remove 'return ' from the first line
            if return_lines:
                # Handle the indentation properly
                first_line = return_lines[0]
                indent = len(first_line) - len(first_line.lstrip())
                return_lines[0] = ' ' * indent + first_line.lstrip()[7:]  # Remove 'return ' but keep indent
            
            return '\n'.join(line.rstrip() for line in return_lines)
        else:
            # New pattern: has helper functions or assignments before return
            # Find all return statements and remove the 'return ' keyword
            result_lines = []
            for line in normalized_lines:
                if line.strip().startswith('return '):
                    # Replace 'return ' with proper indentation maintained
                    indent = len(line) - len(line.lstrip())
                    result_lines.append(' ' * indent + line.lstrip()[7:])  # Remove 'return '
                else:
                    result_lines.append(line)
            
            return '\n'.join(line.rstrip() for line in result_lines)
        
    except Exception as e:
        return f"# Error: {e}"


def with_code(func: Callable) -> Callable:
    """Add .code attribute with extracted source to a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    wrapper.code = extract_code(func)
    return wrapper