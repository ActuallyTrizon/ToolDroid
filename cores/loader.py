import importlib
import pkgutil
import cogs

class CogLoader:
    @staticmethod
    def load_cogs(engine_instance):
        """Dynamically loads all modules inside the cogs/ directory and finds Cog classes."""
        loaded_cogs = []
        for _, module_name, _ in pkgutil.iter_modules(cogs.__path__):
            try:
                mod = importlib.import_module(f"cogs.{module_name}")
                for attribute_name in dir(mod):
                    if attribute_name.endswith("Cog"):
                        cog_class = getattr(mod, attribute_name)
                        loaded_cogs.append(cog_class(engine_instance))
            except Exception as e:
                print(f"Error loading cog {module_name}: {e}")
        return loaded_cogs
