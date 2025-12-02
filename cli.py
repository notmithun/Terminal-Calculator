import random
import statistics as stats

from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel

from utils import *

init(autoreset=True)
import sys
from os import system
from typing import Any, Final

ver: str = f"1.0"


def help_text() -> str:
    return f"""
{Fore.CYAN}=== Terminal Calculator Help ==={Style.RESET_ALL}

{Fore.YELLOW}General:{Style.RESET_ALL}
  {Fore.GREEN}exit / quit / close{Style.RESET_ALL}   - Close the calculator
  {Fore.GREEN}cls / clear{Style.RESET_ALL}          - Clear the screen
  {Fore.GREEN}help / ?{Style.RESET_ALL}             - Show this help

{Fore.YELLOW}Rounding:{Style.RESET_ALL}
  {Fore.GREEN}sf(x, y){Style.RESET_ALL}             - Round x to y significant figures
  {Fore.GREEN}dp(x, y){Style.RESET_ALL}             - Round x to y decimal places
  {Fore.GREEN}round(x, y){Style.RESET_ALL}          - Round to y-th place (ones, tens, etc.)

{Fore.YELLOW}Math:{Style.RESET_ALL}
  {Fore.GREEN}sqrt(x){Style.RESET_ALL}              - Square root
  {Fore.GREEN}cbrt(x){Style.RESET_ALL}              - Cube root
  {Fore.GREEN}root(x, n){Style.RESET_ALL}           - n-th root
  {Fore.GREEN}pow(x, y){Style.RESET_ALL}            - x to the power y
  {Fore.GREEN}exp(x){Style.RESET_ALL}               - e^x
  {Fore.GREEN}log(x, base=10){Style.RESET_ALL}      - Logarithm with base
  {Fore.GREEN}ln(x){Style.RESET_ALL}                - Natural log
  {Fore.GREEN}fact(n){Style.RESET_ALL}             - Factorial
  {Fore.GREEN}nCr(n, r){Style.RESET_ALL}           - Combinations
  {Fore.GREEN}nPr(n, r){Style.RESET_ALL}           - Permutations

{Fore.YELLOW}Trigonometry:{Style.RESET_ALL}
  {Fore.GREEN}sin(x), cos(x), tan(x){Style.RESET_ALL}        - Radians
  {Fore.GREEN}sind(x), cosd(x), tand(x){Style.RESET_ALL}     - Degrees
  {Fore.GREEN}asin(x), acos(x), atan(x){Style.RESET_ALL}     - Arc functions
  {Fore.GREEN}sinh, cosh, tanh{Style.RESET_ALL}             - Hyperbolic
  {Fore.GREEN}deg(x), rad(x){Style.RESET_ALL}               - Convert between deg/rad

{Fore.YELLOW}Statistics:{Style.RESET_ALL}
  {Fore.GREEN}mean(x), median(x), mode(x){Style.RESET_ALL}    - Central tendency
  {Fore.GREEN}std(x), var(x){Style.RESET_ALL}               - Standard deviation / variance
  {Fore.GREEN}gmean(x), hmean(x){Style.RESET_ALL}           - Geometric / harmonic mean
  {Fore.GREEN}percentile(x, p){Style.RESET_ALL}             - p-th percentile

{Fore.YELLOW}Random / Probability:{Style.RESET_ALL}
  {Fore.GREEN}rand(), randint(a,b){Style.RESET_ALL}          - Random float / int
  {Fore.GREEN}randrange(a,b), uniform(a,b){Style.RESET_ALL} - Random in range
  {Fore.GREEN}choose(list), choices(list,k){Style.RESET_ALL} - Pick elements
  {Fore.GREEN}shuffle(list){Style.RESET_ALL}                - Shuffle a list

{Fore.YELLOW}Number Theory:{Style.RESET_ALL}
  {Fore.GREEN}gcd(a,b), lcm(a,b){Style.RESET_ALL}          - Greatest / least common multiple
  {Fore.GREEN}hcfx(*nums), lcmx(*nums){Style.RESET_ALL}    - HCF / LCM for multiple numbers
  {Fore.GREEN}sign(x){Style.RESET_ALL}                     - Sign of x
  {Fore.GREEN}isprime(x){Style.RESET_ALL}                  - Check if prime
  {Fore.GREEN}pf(x){Style.RESET_ALL}                       - Prime factors

{Fore.YELLOW}Sequences & Fractions:{Style.RESET_ALL}
  {Fore.GREEN}fib(n){Style.RESET_ALL}                       - n-th Fibonacci number
  {Fore.GREEN}ratios(a,b,...){Style.RESET_ALL}             - Simplify a ratio
  {Fore.GREEN}ratio_simplify(a,b,...){Style.RESET_ALL}     - Alias for ratios()
  {Fore.GREEN}ratio2frac(a,b,...){Style.RESET_ALL}         - Convert ratio to fractions
  {Fore.GREEN}ratio2percent(a,b,...){Style.RESET_ALL}      - Convert ratio to percent

{Fore.YELLOW}Conversions:{Style.RESET_ALL}
  {Fore.GREEN}deg <-> rad, length, mass, area, volume, temperature{Style.RESET_ALL} - Unit conversions
"""


def calculate(expression: str, custom_instructions: dict[str, Any]):
    expression = expression.replace("^", "**")
    try:
        result: Any = eval(expression, {"__builtins__": None}, custom_instructions)
        if isinstance(result, bool):
            return result
        elif isinstance(result, int):
            return f"{Fore.GREEN}{result:,}"
        elif isinstance(result, float):
            if result.is_integer():
                return f"{Fore.GREEN}{int(result):,}"
            integer_part, dot, decimal_part = f"{result}".partition(".")
            if len(integer_part) > 3:
                integer_part = f"{int(integer_part):,}"
            return f"{Fore.GREEN}{integer_part + (dot + decimal_part if decimal_part else "")}"
        elif isinstance(result, (list, tuple)):
            res_items = []
            for item in result:
                if isinstance(item, float) and item.is_integer():
                    res_items.append(f"{int(item):_}")
                elif isinstance(item, int):
                    res_items.append(f"{item:_}")
                else:
                    res_items.append(str(item))
            return f"{Fore.GREEN}{', '.join(res_items)}"
        else:
            return f"{Fore.GREEN}{str(result)}"
    except ZeroDivisionError:
        return f"{Fore.RED}Calculation Error:\nDivision of any number with zero is not possible."
    except TypeError as e:
        if str(e).startswith("'NoneType' object"):
            return f"{Fore.RED}Unknown function or command. Please check the spellings or the symbols used."
        return f"{Fore.RED} Calculation Error:\n{e}"
    except SyntaxError as e:
        if e.text:
            pointer_line = " " * (int(e.offset) - 1) + "^"  # type: ignore
            return f"{Fore.RED}Syntax Error:\nPlease check your spellings or the symbols you've used! The arrow pointed is where you've wrong\n{e.text.strip()}\n{pointer_line}"
        return f"{Fore.RED}Syntax Error:\n{e}"
    except ValueError as e:
        if str(e).startswith("expected a positive input, got -"):
            return f"{Fore.RED}Calculation Error:\nUsage of negative numbers is not possible for this function!"
        return f"Calculation Error:\n{e}"


if __name__ == "__main__":
    CUSTOM_INSTRUCTIONS: Final[dict[str, Any]] = {
        # Rounding
        "sf": round_sf,
        "dp": round,
        "round": round_place,
        "floor": math.floor,
        "celi": math.ceil,
        "trunc": math.trunc,
        "clamp": lambda x, low, high: max(low, min(x, high)),

        # Constants
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,

        # Exponents, logs
        "sqrt": math.sqrt,
        "cbrt": lambda x: x ** (1 / 3),
        "root": lambda x, n: x ** (1 / n),
        "exp": math.exp,
        "log": lambda x, base=10: math.log(x, base),
        "ln": math.log,
        "pow": pow,
        "gamma": math.gamma,

        # Trig
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sind": lambda x: math.sin(math.radians(x)),
        "cosd": lambda x: math.cos(math.radians(x)),
        "tand": lambda x: math.tan(math.radians(x)),
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "asinh": math.asinh,
        "acosh": math.acosh,
        "atanh": math.atanh,
        "deg": math.degrees,
        "rad": math.radians,
        "hypot": math.hypot,

        # Stats
        "mean": lambda x: stats.mean(x if isinstance(x, list) else [x]),
        "median": lambda x: stats.median(x if isinstance(x, list) else [x]),
        "mode": lambda x: stats.mode(x if isinstance(x, list) else [x]),
        "std": lambda x: stats.stdev(x if isinstance(x, list) else [x]),
        "var": stats.variance,
        "gmean": stats.geometric_mean,
        "hmean": stats.harmonic_mean,
        "percentile": percentile,

        # Random
        "rand": random.random,
        "randint": random.randint,
        "randrange": random.randrange,
        "uniform": random.uniform,
        "choose": random.choice,
        "choices": random.choices,
        "shuffle": lambda lst: random.sample(lst, len(lst)),

        # Number theory
        "fact": math.factorial,
        "nCr": math.comb,
        "nPr": math.perm,
        "gcd": math.gcd,
        "lcm": math.lcm,
        "hcfx": lambda *nums: reduce(math.gcd, nums),
        "lcmx": lambda *nums: reduce(lambda x, y: x * y // math.gcd(x, y), nums),
        "sign": lambda x: (x > 0) - (x < 0),
        "isprime": isprime,
        "pf": pf,

        # Fractions
        "frac": Fraction,
        "to_frac": Fraction,
        "simplify_frac": lambda f: f.limit_denominator(),
        "mixed": to_mixed,
        "mod": lambda x, y: x % y,

        # Sequences
        "seq": lambda a, b, c=1: list(range(a, b, c)),
        "percent": lambda x: x / 100,
        "fib": fib,

        # Calculus
        "deriv": lambda f, x, h=1e-16: (f(x + h) - f(x - h)) / (2 * h),
        "integrate": integrate,

        # Time
        "secstohms": sec_to_hms,
        "hmstosecs": lambda h, m, s: h * 3600 + m * 60 + s,

        # Bases
        "bin2dec": lambda b: int(str(b), 2),
        "dec2bin": lambda x: bin(x)[2:],
        "hex2dec": lambda h: int(str(h), 16),
        "dec2hex": lambda n: hex(n)[2:],
        "oct2dec": lambda o: int(str(o), 8),
        "dec2oct": lambda i: oct(i)[2:],

        # Units
        "km2m": lambda km: km * 1000,
        "m2km": lambda m: m / 1000,
        "cm2m": lambda cm: cm / 100,
        "m2cm": lambda m: m * 100,
        "km2mi": lambda km: km * 0.621371,
        "mi2km": lambda mi: mi / 0.621371,
        "c2f": lambda c: c * 9 / 5 + 32,
        "f2c": lambda f: (f - 32) * 5 / 9,
        "c2k": lambda c: c + 273.15,
        "k2c": lambda k: k - 273.15,
        "f2k": lambda f: (f - 32) * 5 / 9 + 273.15,
        "k2f": lambda k: (k - 273.15) * 9 / 5 + 32,
        "kg2g": lambda kg: kg * 1000,
        "g2kg": lambda g: g / 1000,
        "g2mg": lambda g: g * 1000,
        "mg2g": lambda mg: mg / 1000,
        "kg2lb": lambda kg: kg * 0.20462,
        "lb2kg": lambda lb: lb / 0.20462,
        "sqm2sqft": lambda sqm: sqm * 10.7639,
        "sqft2sqm": lambda sqft: sqft / 10.7639,
        "ltoml": lambda l: l * 1000,
        "ml2l": lambda ml: ml / 1000,

        # Physics
        "pressure": lambda f, a: f / a,
        "density": lambda m, v: m / v,
        "will_it_sink": lambda obj_density, fluid_density: obj_density >= fluid_density,
        "force": lambda m, a: m * a,

        # Misc
        "len": len,
        "ratio": ratios,
        "ratio2frac": ratio_to_frac,
        "ratio2percent": ratio_to_percent,
        "ratio_simplify": ratios,  # can reuse ratios function
        "ver": lambda: ver
    }
    try:
        console = Console()

        console.print(
            Panel("💻 Terminal Calculator", style="bold cyan", expand=False, padding=(1, 4), subtitle_align="center",
                  title=f"Version: {ver}"))
        print(f"Running on {sys.version}")
        while True:
            expr = input(f"{Fore.MAGENTA}>>> ")
            if expr.lower() in ["exit", "quit", "close"]:
                break
            elif expr.lower() in ["cls", "clear"]:
                system("cls")
                continue
            elif expr.lower() in ["help", "?"]:
                print(help_text())
                continue
            print(calculate(expr, CUSTOM_INSTRUCTIONS))
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Force halt!")
        sys.exit(1)
    except EOFError as e:
        print(f"\n{Fore.RED}Either Force halt or something else: {e}")

sys.exit(0)
