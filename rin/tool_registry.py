from .tools import get_current_datetime


class ToolRegistry:
    """
    Stores and manages tools available to Rin.
    """

    def __init__(self):
        self.tools = {}

        self._register_builtin_tools()

    def _register_builtin_tools(self):
        """
        Register Rin's built-in tools.
        """
        self.register(
            "get_current_datetime",
            get_current_datetime,
        )

    def register(self, name: str, function):
        """
        Register a tool using a unique name.
        """
        self.tools[name] = function

    def get(self, name: str):
        """
        Get a registered tool by name.
        """
        return self.tools.get(name)

    def list_tools(self):
        """
        Return the names of all registered tools.
        """
        return list(self.tools.keys())