# Mission 066 - Dynamic Plugin Loader
# Fixed solution
import importlib
import logging

logger = logging.getLogger(__name__)
REQUIRED_METHODS = ["execute", "name", "version"]

def load_plugin(module_name):
    try:
        module = importlib.import_module(module_name)
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
        except RuntimeError as e:
            logger.warning(f"Skipping plugin {name}: {e}")
    return plugins
