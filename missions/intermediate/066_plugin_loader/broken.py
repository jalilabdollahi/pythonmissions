# Mission 066 - Dynamic Plugin Loader
# Fix the 2 bugs in this script.
import importlib

REQUIRED_METHODS = ["execute", "name", "version"]

def load_plugin(module_name):
    try:
        module = importlib.__import__(module_name)  # BUG 1: should be importlib.import_module()
    except ImportError as e:
        raise RuntimeError(f"Cannot load plugin {module_name}: {e}")
    for method in REQUIRED_METHODS:
        if not hasattr(module, method):
            raise RuntimeError(f"Plugin missing required attribute: {method}")
    return module

def list_plugins(module_names):
    plugins = []
    for name in module_names:
        try:
            p = load_plugin(name)
            plugins.append(p)
        except RuntimeError:
            continue  # BUG 2: should at least log the error; but for this mission: pass is fine
    return plugins
