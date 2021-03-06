"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from expression import Expression
from variables import Variable

class BinaryOperator(Expression):
    """
    Base class for expressions involving binary operators.
    """
    def __init__(self, lh_exp, rh_exp):
        self.lh_exp = lh_exp
        self.rh_exp = rh_exp
        # Set the sign and curvature.
        self._context = getattr(self.lh_exp._context,
                                self.OP_FUNC)(self.rh_exp._context)
        super(BinaryOperator, self).__init__()

    def name(self):
        return ' '.join([self.lh_exp.name(), 
                         self.OP_NAME, 
                         self.rh_exp.name()])

    # Return the symbolic affine expression equal to the given index
    # into the expression.
    def index_object(self, key):
        # Scalar promotion
        promoted = self.promoted_index_object(key)
        if promoted is not None:
            return promoted
        return getattr(self.lh_exp[key], self.OP_FUNC)(self.rh_exp[key])

    # The transpose of the binary operator.
    def transpose(self):
        return getattr(self.lh_exp.T, self.OP_FUNC)(self.rh_exp.T)

    # Handle promoted scalars.
    def promoted_index_object(self, key):
        if self.lh_exp.size == (1,1):
            return getattr(self.lh_exp, self.OP_FUNC)(self.rh_exp[key])
        elif self.rh_exp.size == (1,1):
            return getattr(self.lh_exp[key], self.OP_FUNC)(self.rh_exp)
        else:
            return None

    # Canonicalize both sides, concatenate the constraints,
    # and apply the appropriate arithmetic operator to
    # the two objectives.
    def canonicalize(self):
        lh_obj,lh_constraints = self.lh_exp.canonical_form()
        rh_obj,rh_constraints = self.rh_exp.canonical_form()
        obj = getattr(lh_obj, self.OP_FUNC)(rh_obj)
        return (obj,lh_constraints + rh_constraints)

class AddExpression(BinaryOperator):
    OP_NAME = "+"
    OP_FUNC = "__add__"

class SubExpression(BinaryOperator):
    OP_NAME = "-"
    OP_FUNC = "__sub__"

class MulExpression(BinaryOperator):
    OP_NAME = "*"
    OP_FUNC = "__mul__"

    # Return the symbolic affine expression equal to the given index
    # in the expression.
    def index_object(self, key):
        # Scalar multiplication.
        promoted = self.promoted_index_object(key)
        if promoted is not None:
            return promoted
        # Matrix multiplication.
        return self.lh_exp[key[0],:]*self.rh_exp[:,key[1]]

    # The transpose of the binary operator.
    def transpose(self):
        return self.rh_exp.T*self.lh_exp.T

    # If left-hand side is non-constant, replace lh*rh with x, x.T == rh.T*lh.T.
    def canonicalize(self):
        if not self.lh_exp.curvature.is_constant():
            x = Variable(*self.size)
            obj = x.canonical_form()[0]
            constraints = (x.T == self.rh_exp.T*self.lh_exp.T).canonical_form()[1]
            return (obj, constraints)
        else:
            return super(MulExpression, self).canonicalize()