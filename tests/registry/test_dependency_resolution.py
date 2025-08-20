"""Tests for component dependency resolution."""

import pytest

from starui.registry.client import RegistryClient
from starui.registry.loader import ComponentLoader, DependencyResolver


class TestDependencyResolver:
    """Test dependency resolution logic."""

    def test_resolve_simple_component(self):
        """Test resolving component with no dependencies."""
        client = RegistryClient()
        resolver = DependencyResolver(client)

        result = resolver.resolve_dependencies("button")
        assert result == ["button"]

    def test_resolve_component_with_dependencies(self):
        """Test resolving component with dependencies."""
        client = RegistryClient()
        resolver = DependencyResolver(client)

        result = resolver.resolve_dependencies("theme_toggle")
        assert result == ["button", "theme_toggle"]
        assert result[0] == "button"  # Dependency comes first
        assert result[-1] == "theme_toggle"  # Requested component comes last

    def test_nonexistent_component(self):
        """Test error handling for nonexistent components."""
        client = RegistryClient()
        resolver = DependencyResolver(client)

        with pytest.raises(
            FileNotFoundError, match="Component 'nonexistent' not found"
        ):
            resolver.resolve_dependencies("nonexistent")


class TestComponentLoader:
    """Test component loading with dependencies."""

    def test_load_single_component(self):
        """Test loading a single component without dependencies."""
        loader = ComponentLoader()

        source = loader.load_component("button")
        assert "def Button" in source
        assert "from .utils import" in source

    def test_load_component_with_dependencies(self):
        """Test loading component with all dependencies."""
        loader = ComponentLoader()

        sources = loader.load_component_with_dependencies("theme_toggle")

        assert len(sources) == 2
        assert "button" in sources
        assert "theme_toggle" in sources

        # Check button is valid
        assert "def Button" in sources["button"]

        # Check theme_toggle is valid
        assert "def ThemeToggle" in sources["theme_toggle"]
        assert "from .button import Button" in sources["theme_toggle"]

    def test_load_nonexistent_component(self):
        """Test error handling for nonexistent components."""
        loader = ComponentLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_component("nonexistent")


class TestRegistryClient:
    """Test registry client functionality."""

    def test_list_components(self):
        """Test listing all available components."""
        client = RegistryClient()

        components = client.list_components()
        assert "button" in components
        assert "theme_toggle" in components
        assert "alert" in components
        assert "badge" in components
        assert "card" in components
        assert "input" in components
        assert "label" in components

        # Utils should not be in the list
        assert "utils" not in components
        assert "__init__" not in components

    def test_component_exists(self):
        """Test checking if components exist."""
        client = RegistryClient()

        assert client.component_exists("button")
        assert client.component_exists("theme_toggle")
        assert client.component_exists("utils")  # Utils should be accessible
        assert not client.component_exists("nonexistent")

    def test_get_component_metadata(self):
        """Test extracting component metadata."""
        client = RegistryClient()

        # Test component with dependencies
        meta = client.get_component_metadata("theme_toggle")
        assert meta["name"] == "theme_toggle"
        assert meta["dependencies"] == ["button"]
        assert isinstance(meta["description"], str)
        assert len(meta["description"]) > 0  # Should have a description

        # Test component without dependencies
        meta = client.get_component_metadata("button")
        assert meta["name"] == "button"
        assert meta["dependencies"] == []
        assert isinstance(meta["description"], str)  # Should return empty string if no docstring

    def test_get_component_source(self):
        """Test getting component source code."""
        client = RegistryClient()

        source = client.get_component_source("button")
        assert "def Button" in source
        assert "from starhtml" in source

        # Test utils is accessible
        utils_source = client.get_component_source("utils")
        assert "def cn" in utils_source
        assert "def cva" in utils_source


class TestDependencyChain:
    """Test complex dependency scenarios."""

    def test_no_circular_dependencies(self):
        """Verify no circular dependencies exist in registry."""
        client = RegistryClient()
        resolver = DependencyResolver(client)

        # Test all components for circular dependencies
        components = client.list_components()
        for comp in components:
            try:
                result = resolver.resolve_dependencies(comp)
                assert comp in result
            except ValueError as e:
                if "Circular dependency" in str(e):
                    pytest.fail(f"Circular dependency detected in {comp}: {e}")

    def test_dependency_order_preserved(self):
        """Test that dependency order is topologically correct."""
        client = RegistryClient()
        loader = ComponentLoader(client)

        # Get theme_toggle with dependencies
        sources = loader.load_component_with_dependencies("theme_toggle")
        order = list(sources.keys())

        # Button should come before theme_toggle
        button_idx = order.index("button")
        toggle_idx = order.index("theme_toggle")
        assert button_idx < toggle_idx
