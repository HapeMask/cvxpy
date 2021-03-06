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

import abc
import types
import expression
from .. import utilities as u
from affine import AffObjective
from collections import deque

class Leaf(expression.Expression, u.Affine):
    """
    A leaf node, i.e. a Variable, Constant, or Parameter.
    """
    __metaclass__ = abc.ABCMeta
    # Objective associated with the leaf.
    def _objective(self):
        return AffObjective(self.variables(), [deque([self])], self.shape)

    # Constraints associated with the leaf.
    def _constraints(self):
        return []

    # Root for the construction of affine expressions.
    def canonicalize(self):
        return (self._objective(), self._constraints())

    # Returns the coefficients dictionary for the leaf.
    @abc.abstractmethod
    def coefficients(self, interface):
        return NotImplemented
        
    # Returns the tranpose of the non-scalar leaf.
    @abc.abstractmethod
    def transpose(self):
        return NotImplemented