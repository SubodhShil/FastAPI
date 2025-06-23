import pkgutil
import importlib

def discover_and_include_routers(app, package_name):
    """
    Dynamically discovers and includes routers from a given package.
    """
    package = importlib.import_module(package_name)
    for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(name)
            if hasattr(module, 'router'):
                app.include_router(module.router)
        except Exception as e:
            print(f"Could not import router from {name}: {e}") 