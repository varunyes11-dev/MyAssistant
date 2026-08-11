from rin.tools import calculate


tests = [
    "25 * 18",
    "144 / 12",
    "15 / 100 * 800",
    "2 + 3 * 4",
]

for expression in tests:
    result = calculate(expression)
    print(f"{expression} = {result}")
