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

from elementwise import Elementwise
from ..quad_over_lin import quad_over_lin
from ... import utilities as u
from ... import interface as intf
from ...expressions import types
from ...expressions.variables import Variable
from ...constraints.affine import AffEqConstraint, AffLeqConstraint

class inv_pos(Elementwise):
    """ Elementwise 1/x, x >= 0 """
    def __init__(self, x):
        super(inv_pos, self).__init__(x)
        # Args are all indexes into x.
        self.x = self.args[0]
        self.args = [xi for xi in self.x]
        
    # The shape is the same as the argument's shape.
    def set_shape(self):
        self._shape = u.Shape(*self.args[0].size)

    # Always positive.
    def sign_from_args(self):
        return u.Sign.POSITIVE

    # Default curvature.
    def base_curvature(self):
        return u.Curvature.CONVEX

    def monotonicity(self):
        return [u.Monotonicity.DECREASING]
    
    @staticmethod
    def graph_implementation(var_args, size):
        t = Variable(*size)
        constraints = []
        one = types.constant()(1).canonical_form()[0]
        for ti,xi in zip(t,var_args):
            obj,constr = quad_over_lin.graph_implementation([one,xi],(1,1))
            constraints += constr + [AffEqConstraint(obj, ti), 
                                     AffLeqConstraint(0, xi)]
        return (t, constraints)