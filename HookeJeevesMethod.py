from typing import List
from typing import Tuple
from typing import Callable
import GoldenRatioMathod
import SvennMethod
import math

def FindMinimum(func: Callable[[List[float]], float], startPoint: List[float], delta: float, e: float, m: float = 0.5) -> List[Tuple[List[float], float]]:
    steps = len(startPoint)
    trace = [(startPoint.copy(), func(startPoint))]
    while True:
        (previousPoint, previousValue) = trace[-1]
        newPoint = previousPoint.copy()
        for step in range(steps):
            newPoint[step] += delta
            if func(newPoint) < previousValue:
                continue
            newPoint[step] -= delta * 2
            if func(newPoint) < previousValue:
                continue
            newPoint[step] += delta
        direction = GetDifference(newPoint, previousPoint)
        if all(abs(number) < e / 10 for number in direction):
            if delta <= e:
                return trace
            delta *= m
            continue
        singleVarFunc = GetSignleVariableFunc(func, previousPoint, direction)
        (a, b) = SvennMethod.FindUnimodalSegment(0, 0.01, singleVarFunc)
        (l, newValue) = GoldenRatioMathod.FindMinimum(a, b, e / 10, singleVarFunc)
        newPoint = GetSum(previousPoint, GetMultiply(direction, l))
        trace.append((newPoint, newValue))


def GetDifference(firstVector: List[float], secondVector: List[float]) -> List[float]:    
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors have different number of elements. First={}, second={}".format(len(firstVector), len(secondVector)))
    result = firstVector.copy()
    for i in range(len(firstVector)):
        result[i] = firstVector[i] - secondVector[i]
    return result


def GetSum(firstVector: List[float], secondVector: List[float]) -> List[float]:    
    if len(firstVector) != len(secondVector):
        raise Exception("Vectors have different number of elements. First={}, second={}".format(len(firstVector), len(secondVector)))
    result = firstVector.copy()
    for i in range(len(firstVector)):
        result[i] = firstVector[i] + secondVector[i]
    return result


def GetMultiply(vector: List[float], multiplier: float) -> List[float]:   
    result = vector.copy()
    for i in range(len(vector)):
        result[i] = vector[i] * multiplier
    return result


def GetSignleVariableFunc(func: Callable[[List[float]], float], previousPoint: List[float], direction: List[float]) -> Callable[[float], float]:
    def inner(l: float) -> float:
        newPoint = GetSum(previousPoint, GetMultiply(direction, l))
        return func(newPoint)
    return inner


def GetDistance(firstPoint: List[float], secondPoint: List[float]) -> float:
    if len(firstPoint) != len(secondPoint):
        raise Exception("Points have different dimensions. First={}, second={}".format(len(firstPoint), len(secondPoint)))
    i = 0
    distance = 0
    while i < len(firstPoint):
        distance += (firstPoint[i] - secondPoint[i]) ** 2
        i += 1
    return math.sqrt(distance)