from rin.tool_registry import ToolRegistry


registry = ToolRegistry()

print("Registered tools:")
print(registry.list_tools())

tool = registry.get("get_current_datetime")

print("\nTool result:")
print(tool())