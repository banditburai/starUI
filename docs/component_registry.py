from typing import Any, Callable


class ComponentRegistry:
    def __init__(self):
        self.components: dict[str, dict[str, Any]] = {}
        self.blocks: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        title: str,
        description: str,
        category: str = "ui",
        order: int = 100,
        status: str = "stable",
        examples: list[tuple[str, Any]] | None = None,
        create_docs: Callable | None = None,
    ) -> None:
        self.components[name] = {
            "title": title,
            "description": description,
            "category": category,
            "order": order,
            "status": status,
            "examples": examples or [],
            "create_docs": create_docs,
        }

    def register_block(
        self,
        name: str,
        title: str,
        description: str,
        create_docs: Callable | None = None,
        preview: Callable | None = None,
        order: int = 100,
        status: str = "stable",
    ) -> None:
        self.blocks[name] = {
            "title": title,
            "description": description,
            "create_docs": create_docs,
            "preview": preview,
            "order": order,
            "status": status,
        }

    def get(self, name: str) -> dict[str, Any] | None:
        return self.components.get(name)

    def get_block(self, name: str) -> dict[str, Any] | None:
        return self.blocks.get(name)
    
    def get_by_category(self, category: str) -> list[tuple[str, dict[str, Any]]]:
        return [
            (name, comp) 
            for name, comp in self.components.items() 
            if comp["category"] == category
        ]
    
    def get_categories(self) -> list[str]:
        return sorted(set(comp["category"] for comp in self.components.values()))


_registry = ComponentRegistry()


def get_registry() -> ComponentRegistry:
    return _registry