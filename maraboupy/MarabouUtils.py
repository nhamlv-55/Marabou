'''
Top contributors (to current version):
    - Christopher Lazarus
    - Shantanu Thakoor
    - Kyle Julian
    
This file is part of the Marabou project.
Copyright (c) 2017-2019 by the authors listed in the file AUTHORS
in the top-level source directory) and their institutional affiliations.
All rights reserved. See the file COPYING in the top-level source
directory for licensing information.

MarabouUtils contains supporting Maraboupy code that doesn't fit in other files
'''

from maraboupy import MarabouCore
from typing import List, Tuple
class Equation:
    """Python class to conveniently represent :class:`~maraboupy.MarabouCore.Equation`

    Attributes:
        addendList (list of tuples): Each addend tuple contains a coefficient and variable number
        scalar (float): Scalar term for equation
        EquationType (:class:`~maraboupy.MarabouCore.EquationType`): Equation type (EQ, LE, GE)
    """
    def __init__(self, EquationType=MarabouCore.Equation.EQ):
        """Construct empty equation
        """
        self.addendList:List[Tuple[float, int]] = []
        self.scalar:float = float('-inf')
        self.EquationType = EquationType

    def setScalar(self, x):
        """Set scalar of equation

        Args:
            x (float): scalar RHS of equation
        """
        self.scalar = x

    def addAddend(self, c, x):
        """Add an addend to the equation

        Args:
            c (float): coefficient of addend
            x (int): variable number of variable in addend
        """
        self.addendList += [(c, x)]
    def toCoreEquation(self)->MarabouCore.Equation:
        eq = MarabouCore.Equation(self.EquationType)
        for (c, v) in self.addendList:
            eq.addAddend(c, v)
        eq.setScalar(self.scalar)
        return eq
    def __str__(self) -> str:
        #build sign
        sign: str
        if self.EquationType == MarabouCore.Equation.LE:
            sign = "<="
        elif self.EquationType == MarabouCore.Equation.GE:
            sign = ">="
        elif self.EquationType == MarabouCore.Equation.EQ:
            sign = "=="
        else:
            sign = "?"
        #build rhs
        rhs:str = str(self.scalar)
        #build lhs
        terms: List[str] = []
        lhs:str = ""
        addend: Tuple[int, int]
        for addend in self.addendList:
            terms.append("{}*var_{} ".format(addend[0], addend[1]))
        lhs = " + ".join(terms)
        return "{} {} {}".format(lhs, sign, rhs)