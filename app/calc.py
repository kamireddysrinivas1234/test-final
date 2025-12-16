from typing import Callable, Dict

def add(a: float, b: float) -> float:
    return a + b

def sub(a: float, b: float) -> float:
    return a - b

def mul(a: float, b: float) -> float:
    return a * b

def div(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def mod(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Modulo by zero")
    return a % b

def pow_(a: float, b: float) -> float:
    return a ** b

OPS: Dict[str, Callable[[float, float], float]] = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "mod": mod,
    "pow": pow_,
}

def compute(op: str, a: float, b: float) -> float:
    if op not in OPS:
        raise ValueError("Unsupported operation")
    return float(OPS[op](a, b))
