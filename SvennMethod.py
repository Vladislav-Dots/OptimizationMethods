from typing import Callable 

# находим отрезок унимодальности, на вход подаём:
# x0 - начальная точка
# t - длина шага
# func - целевая функция одной переменной
def FindUnimodalSegment(x0: float, t: float, func: Callable[[float], float]) -> (float, float):
    print("Called FindUnimodalSegment by SvennMethod with params x0={}, t={}".format(x0, t))
    if t <= 0:
        raise Exception("Parameter 't' must be positive but was: {}".format(t))
    fx0 = func(x0)
    fxminus = func(x0 - t)
    fxplus = func(x0 + t)
    if fxminus >= fx0 and fx0 <= fxplus:
        return (x0 - t, x0 + t)
    if fxminus <= fx0 and fx0 >= fxplus:
        return None        
    if fxminus >= fx0 >= fxplus:
        delta = t
    elif fxminus <= fx0 <= fxplus:
        delta = -t
    xk = x0
    fxk = fx0
    xkminus = x0 - t
    while True:
        xkplus = xk + delta
        fxkplus = func(xkplus)
        if (fxkplus > fxk):
            if delta > 0:
                return (xkminus, xkplus)
            else: 
                return (xkplus, xkminus)
        xkminus = xk
        xk = xkplus
        fxk = fxkplus
        delta *= 2