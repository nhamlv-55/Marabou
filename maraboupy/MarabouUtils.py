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
from maraboupy.MarabouNetwork import ZERO



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
        print(self)
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

class ReLUGradEquation:
    """
    Given v_out = ReLU(v_in)
    The corresponding g_in can be computed knowing g_out and v_out

    This is the class to convenietly represent the disjuct computing 
    g_in
    """
    def __init__(self, v_in: int, v_out: int, g_in: int, g_out: int):
        """
        Construct the disjunct of 2 MarabouUtils.Equation
        """
        assert v_in < v_out
        assert g_in - v_in == g_out - v_out
        self.g_in = g_in #we need this to keep track of what ReLU to be abstracted
        self.g_out = g_out
        self.v_in = v_in
        self.v_out = v_out
        self.disjunct: List[List[Equation]] = []
        #example: v10 = relu(v7)
        #grad constraints:
        #if v7 > 0 then g7 = g10 ~ (g7=g10)or(v7<=0): pos_grad constraints
        #v7<=0 then g7 = 0 ~ (g7=0) or (v7 >= 0)
        #positive grad
        pos_condition = Equation(MarabouCore.Equation.LE)
        pos_condition.addAddend(1, v_in); 
        pos_condition.setScalar(-ZERO)

        pos_body = Equation(MarabouCore.Equation.EQ)
        pos_body.addAddend(1, g_in)
        pos_body.addAddend(-1, g_out)
        pos_body.setScalar(0)

        self.disjunct.append([pos_condition, pos_body])
        print("IF POSITIVE:", pos_condition, "OR", pos_body)

        
        #negative grad
        neg_condition = Equation(MarabouCore.Equation.GE)
        neg_condition.addAddend(1, v_in); 
        neg_condition.setScalar(0)

        neg_body = Equation(MarabouCore.Equation.EQ)
        neg_body.addAddend(1, g_in)
        neg_body.setScalar(0)

        self.disjunct.append([neg_condition, neg_body])
        print("IF NEGATIVE:", neg_condition, "OR", neg_body)

    def abstract(self, v_in_bounds: List[float],
                 v_out_bounds: List[float],
                 g_out_bounds: List[float])->List[Equation]:
        abstraction: List[Equation] = []
        return abstraction