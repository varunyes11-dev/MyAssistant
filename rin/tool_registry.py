from .tools import (
    calculate,
    get_battery_status,
    get_current_datetime,
    get_system_info,
    open_application,
    open_website,
)


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
            parameters={
                "type": "object",
                "properties": {},
            },
        )

        self.register(
            name="calculate",
            function=calculate,
            description="Calculate a basic arithmetic expression.",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A basic arithmetic expression such as "
                            "25 * 18 or 144 / 12."
                        ),
                    }
                },
                "required": ["expression"],
            },
        )

        self.register(
            name="get_battery_status",
            function=get_battery_status,
            description=(
                "Get the current Mac battery percentage "
                "and charging status."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
        )

        self.register(
            name="get_system_info",
            function=get_system_info,
            description=(
                "Get useful non-sensitive information about this Mac."
            ),
            parameters={
                "type": "object",
                "properties": {},
            },
        )

        self.register(
            name="open_application",
            function=open_application,
            description="Open a macOS application by name.",
            parameters={
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": (
                            "The exact name of the macOS "
                            "application to open."
                        ),
                    }
                },
                "required": ["app_name"],
            },
        )

        self.register(
            name="open_website",
            function=open_website,
            description="Open a website in the default browser.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The website URL to open."
                        ),
                    }
                },
                "required": ["url"],
            },
        )

    def register(
        self,
        name: str,
        function,
        description: str,
        parameters: dict | None = None,
    ):
        """
        Register a tool with its function, description,
        and Ollama parameter schema.
        """

        self.tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters or {
                "type": "object",
                "properties": {},
            },
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

    def execute(
        self,
        name: str,
        arguments: dict | None = None,
    ) -> str:
        """
        Execute a registered tool.
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