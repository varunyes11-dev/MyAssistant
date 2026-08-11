from .tools import get_current_datetime


class ToolRegistry:
    """
    Stores, describes, and executes tools available to Rin.
    """

    def __init__(self):
        self.tools = {}

        self._register_builtin_tools()

    def _register_builtin_tools(self):
        """
        Register Rin's built-in tools.
        """
        self.register(
            name="get_current_datetime",
            function=get_current_datetime,
            description="Get the current local date and time.",
        )

    def register(
        self,
        name: str,
        function,
        description: str,
    ):
        """
        Register a tool.
        """
        self.tools[name] = {
            "function": function,
            "description": description,
        }

    def get(self, name: str):
        """
        Get a registered tool.
        """
        return self.tools.get(name)

    def list_tools(self) -> list[str]:
        """
        Return the names of all registered tools.
        """
        return list(self.tools.keys())

    def get_descriptions(self) -> dict[str, str]:
        """
        Return descriptions of all registered tools.
        """
        return {
            name: tool["description"]
            for name, tool in self.tools.items()
        }

    def execute(self, name: str, arguments: dict | None = None) -> str:
        """
        Execute a registered tool.

        Tools that don't require arguments simply ignore
        the arguments dictionary.
        """
        tool = self.get(name)

        if tool is None:
            raise ValueError(
                f"Unknown tool requested: {name}"
            )

        function = tool["function"]

        if arguments:
            return str(function(**arguments))

        return str(function())