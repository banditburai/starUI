"""Component loading and dependency resolution."""

from .client import RegistryClient
from .component_metadata import get_component_metadata


class ComponentLoader:
    """Loads components with dependency resolution."""

    def __init__(self, client: RegistryClient | None = None) -> None:
        self.client = client or RegistryClient()
        self.resolver = DependencyResolver(self.client)

    def load_component(self, component_name: str) -> str:
        if not self.client.component_exists(component_name):
            raise FileNotFoundError(f"Component '{component_name}' not found")
        return self.client.get_component_source(component_name)

    def load_component_with_dependencies(self, component_name: str) -> dict[str, str]:
        resolved = self.resolver.resolve_dependencies(component_name)

        sources = {}
        for name in resolved:
            if not self.client.component_exists(name):
                raise FileNotFoundError(f"Dependency '{name}' not found")
            sources[name] = self.client.get_component_source(name)

        return sources


class DependencyResolver:
    """Resolves dependencies with circular detection."""

    def __init__(self, client: RegistryClient) -> None:
        self.client = client

    def resolve_dependencies(self, component_name: str) -> list[str]:
        """Resolve dependencies in topological order."""
        resolved = []
        visiting = set()
        visited = set()

        def visit(name: str) -> None:
            if name in visiting:
                raise ValueError(f"Circular dependency: {name}")
            if name in visited:
                return

            metadata = get_component_metadata(name)
            if not metadata:
                raise FileNotFoundError(f"Component '{name}' not found")

            visiting.add(name)
            for dep in metadata.dependencies:
                visit(dep)
            visiting.remove(name)
            visited.add(name)

            if name not in resolved:
                resolved.append(name)

        visit(component_name)
        return resolved
