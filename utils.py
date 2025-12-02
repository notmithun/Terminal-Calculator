import math
from fractions import Fraction
from functools import reduce
from typing import Any, List, Tuple


def round_sf(x: float, sf: int) -> Any:
    """
    Round a number to a specified number of significant figures.

    Args:
        x (float): The number to round.
        sf (int): The number of significant figures.

    Returns:
        float: Rounded number to the specified significant figures.
               Returns 0 if the input is 0.
    """
    if x != 0:
        order = math.floor(math.log10(abs(x)))
        factor = 10 ** (sf - order - 1)
        return round(x * factor) / factor
    return x


def isprime(n: int) -> bool:
    """
    Check if a number is prime.

    Args:
        n (int): Number to check.

    Returns:
        bool: True if prime, False otherwise.
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def to_mixed(frac: Fraction) -> str:
    """
    Convert a Fraction to mixed number format.

    Args:
        frac (Fraction): Fraction to convert.

    Returns:
        str: Mixed number as a string (e.g., "1 1/2").
    """
    whole = frac.numerator // frac.denominator
    remainder = frac.numerator % frac.denominator
    if whole == 0:
        return f"{remainder}/{frac.denominator}"
    elif remainder == 0:
        return f"{whole}"
    else:
        return f"{whole} {remainder}/{frac.denominator}"


def pf(x: int) -> List[int]:
    """
    Compute the prime factors of a number.

    Args:
        x (int): Number to factorize.

    Returns:
        List[int]: List of prime factors.
    """
    res = []
    d = 2
    while d * d <= x:
        while x % d == 0:
            res.append(d)
            x //= d
        d += 1
    if x > 1:
        res.append(x)
    return res


def fib(n: int) -> int:
    """
    Compute the n-th Fibonacci number.

    Args:
        n (int): Index of Fibonacci number (0-based).

    Returns:
        int: n-th Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def integrate(f, a: float, b: float, n: int = 10000) -> float:
    """
    Approximate the integral of a function using the trapezoidal rule.

    Args:
        f (callable): Function to integrate.
        a (float): Lower limit.
        b (float): Upper limit.
        n (int, optional): Number of subintervals. Default is 10000.

    Returns:
        float: Approximate integral value.
    """
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h


def sec_to_hms(sec: int) -> Tuple[int, int, int]:
    """
    Convert seconds to hours, minutes, and seconds.

    Args:
        sec (int): Number of seconds.

    Returns:
        Tuple[int, int, int]: (hours, minutes, seconds)
    """
    h = sec // 3600
    sec %= 3600
    m = sec // 60
    s = sec % 60
    return h, m, s


def ratios(*vals: int) -> str:
    """
    Simplify a set of numbers as a ratio.

    Args:
        *vals (int): Numbers to simplify. Can also pass a list/tuple.

    Returns:
        str: Simplified ratio as a string (e.g., "2:3:5").
    """
    if len(vals) == 1 and isinstance(vals[0], (list, tuple)):
        vals = vals[0]
    nums = [int(v) for v in vals]
    g = reduce(math.gcd, nums)
    simplified = [n // g for n in nums]
    return ":".join(str(v) for v in simplified)


def round_place(x: int, place: int) -> int:
    """
    Round a number to its n-th place (1=ones, 2=tens, etc.)

    Args:
        x (int): Number to round.
        place (int): Place value to round to.

    Returns:
        int: Rounded number.
    """
    if x == 0:
        return 0
    sign = 1 if x > 0 else -1
    x = abs(x)
    digits = len(str(int(x)))
    factor = 10 ** (digits - place)
    return sign * round(x / factor) * factor


def percentile(data: list[float], p: float) -> Any:
    """
    Calculate the p-th percentile of a dataset.

    Args:
        data (list[float]): Data points.
        p (float): Percentile (0-100).

    Returns:
        float: Value at the p-th percentile.
    """
    if not data:
        return None
    data = sorted(data)
    k = (len(data) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return data[int(k)]
    return data[f] + (k - f) * (data[c] - data[f])


def ratio_simplify(*vals: int) -> str:
    """
    Alias for `ratios()`. Simplify numbers as a ratio.

    Args:
        *vals (int): Numbers to simplify. Can also pass a list/tuple.

    Returns:
        str: Simplified ratio as string.
    """
    return ratios(*vals)


def ratio_to_frac(*vals: int) -> List[Fraction]:
    """
    Convert a set of numbers into fractions of their sum.

    Args:
        *vals (int): Numbers to convert. Can also pass a list/tuple.

    Returns:
        List[Fraction]: Fractions of the total sum.
    """
    if len(vals) == 1 and isinstance(vals[0], (list, tuple)):
        vals = vals[0]
    nums = [Fraction(v) for v in vals]
    total = sum(nums)
    return [n / total for n in nums]


def ratio_to_percent(*vals: int) -> List[float]:
    """
    Convert a set of numbers into percentages of their sum.

    Args:
        *vals (int): Numbers to convert. Can also pass a list/tuple.

    Returns:
        List[float]: Percentages of the total sum.
    """
    if len(vals) == 1 and isinstance(vals[0], (list, tuple)):
        vals = vals[0]
    nums = [float(v) for v in vals]
    total = sum(nums)
    return [(n / total) * 100 for n in nums]
