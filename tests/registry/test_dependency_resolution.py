import pytest

from .conftest import make_component_entry, make_test_client

TEST_SOURCES = {
    "utils": "def cn(*classes): pass\ndef cva(): pass\n",
    "button": "from .utils import cn\n\ndef Button(**kwargs): pass\n",
    "theme_toggle": "from .button import Button\nfrom .utils import cn\n\ndef ThemeToggle(): pass\n",
    "alert": "from .utils import cn\n\ndef Alert(): pass\n",
}

TEST_INDEX = {
    "version": "0.3.0",
    "schema_version": 1,
    "components": {
        "utils": make_component_entry("utils", TEST_SOURCES["utils"]),
        "button": make_component_entry("button", TEST_SOURCES["button"], deps=["utils"]),
        "theme_toggle": make_component_entry("theme_toggle", TEST_SOURCES["theme_toggle"], deps=["utils", "button"]),
        "alert": make_component_entry("alert", TEST_SOURCES["alert"], deps=["utils"]),
    },
}


@pytest.fixture
def registry_client(tmp_path):
    return make_test_client(tmp_path, "test", TEST_INDEX, TEST_SOURCES)


class TestDependencyResolver:
    def test_resolve_simple_component(self, registry_client):
        assert registry_client.resolve_dependencies("button") == ["utils", "button"]

    def test_resolve_component_with_dependencies(self, registry_client):
        result = registry_client.resolve_dependencies("theme_toggle")
        assert "utils" in result
        assert "button" in result
        assert result[-1] == "theme_toggle"
        assert result.index("utils") < result.index("button")
        assert result.index("button") < result.index("theme_toggle")

    def test_nonexistent_component(self, registry_client):
        with pytest.raises(FileNotFoundError, match="Component 'nonexistent' not found"):
            registry_client.resolve_dependencies("nonexistent")


class TestComponentLoading:
    def test_load_single_component(self, registry_client):
        source = registry_client.get_component_source("button")
        assert "def Button" in source
        assert "from .utils import" in source

    def test_load_component_with_dependencies(self, registry_client):
        sources = registry_client.get_component_with_dependencies("theme_toggle")
        assert set(sources.keys()) == {"utils", "button", "theme_toggle"}
        assert "def Button" in sources["button"]
        assert "def ThemeToggle" in sources["theme_toggle"]

    def test_load_nonexistent_component(self, registry_client):
        with pytest.raises(FileNotFoundError):
            registry_client.get_component_source("nonexistent")


class TestRegistryClient:
    def test_list_components(self, registry_client):
        components = registry_client.list_components()
        assert "button" in components
        assert "theme_toggle" in components
        assert "alert" in components
        assert "utils" not in components

    def test_get_component_metadata(self, registry_client):
        meta = registry_client.get_component_metadata("theme_toggle")
        assert meta["name"] == "theme_toggle"
        assert meta["dependencies"] == ["utils", "button"]

        meta = registry_client.get_component_metadata("button")
        assert meta["dependencies"] == ["utils"]

    def test_get_component_source(self, registry_client):
        assert "def Button" in registry_client.get_component_source("button")
        utils_source = registry_client.get_component_source("utils")
        assert "def cn" in utils_source
        assert "def cva" in utils_source


class TestDependencyChain:
    def test_all_components_resolve_with_deps_before_dependents(self, registry_client):
        index = registry_client._get_index()
        for comp in index["components"]:
            result = registry_client.resolve_dependencies(comp)
            assert len(result) == len(set(result))
            assert result[-1] == comp
            for dep in index["components"][comp].get("dependencies", []):
                assert result.index(dep) < result.index(comp)

    def test_dependency_order_preserved(self, registry_client):
        order = list(registry_client.get_component_with_dependencies("theme_toggle").keys())
        assert order.index("button") < order.index("theme_toggle")


class TestCircularDependencies:
    @pytest.fixture
    def circular_client(self, tmp_path):
        sources = {"comp_a": "def A(): pass\n", "comp_b": "def B(): pass\n"}
        index = {
            "version": "0.3.0",
            "schema_version": 1,
            "components": {
                "comp_a": make_component_entry("comp_a", sources["comp_a"], deps=["comp_b"]),
                "comp_b": make_component_entry("comp_b", sources["comp_b"], deps=["comp_a"]),
            },
        }
        return make_test_client(tmp_path, "circ", index, sources)

    def test_circular_dependency_raises(self, circular_client):
        with pytest.raises(ValueError, match="Circular dependency"):
            circular_client.resolve_dependencies("comp_a")

    def test_self_referencing_raises(self, tmp_path):
        sources = {"self_dep": "pass\n"}
        index = {
            "version": "0.3.0",
            "schema_version": 1,
            "components": {
                "self_dep": make_component_entry("self_dep", sources["self_dep"], deps=["self_dep"]),
            },
        }
        client = make_test_client(tmp_path, "self", index, sources)
        with pytest.raises(ValueError, match="Circular dependency"):
            client.resolve_dependencies("self_dep")


class TestDiamondDependency:
    @pytest.fixture
    def diamond_client(self, tmp_path):
        sources = {n: f"def {n.title()}(): pass\n" for n in ["utils", "button", "badge", "dialog"]}
        index = {
            "version": "0.3.0",
            "schema_version": 1,
            "components": {
                "utils": make_component_entry("utils", sources["utils"]),
                "button": make_component_entry("button", sources["button"], deps=["utils"]),
                "badge": make_component_entry("badge", sources["badge"], deps=["utils"]),
                "dialog": make_component_entry("dialog", sources["dialog"], deps=["button", "badge"]),
            },
        }
        return make_test_client(tmp_path, "diamond", index, sources)

    def test_diamond_resolves_shared_dep_once(self, diamond_client):
        result = diamond_client.resolve_dependencies("dialog")
        assert result.count("utils") == 1
        assert result[-1] == "dialog"
        assert result.index("utils") < result.index("button")
        assert result.index("utils") < result.index("badge")

    def test_diamond_loads_all_sources(self, diamond_client):
        sources = diamond_client.get_component_with_dependencies("dialog")
        assert set(sources.keys()) == {"utils", "button", "badge", "dialog"}


class TestMissingTransitiveDependency:
    def test_missing_transitive_dep_raises(self, tmp_path):
        sources = {"comp_a": "pass\n", "comp_b": "pass\n"}
        index = {
            "version": "0.3.0",
            "schema_version": 1,
            "components": {
                "comp_a": make_component_entry("comp_a", sources["comp_a"], deps=["comp_b"]),
                "comp_b": make_component_entry("comp_b", sources["comp_b"], deps=["missing"]),
            },
        }
        client = make_test_client(tmp_path, "missing", index, sources)
        with pytest.raises(FileNotFoundError, match="'missing'"):
            client.resolve_dependencies("comp_a")
