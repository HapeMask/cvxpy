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

class Shape(object):
    """ The dimensions of an expression. """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        super(Shape, self).__init__()

    @property
    def size(self):
        return (self.rows, self.cols)

    # The expression's sizes must match unless one is a scalar,
    # in which case it is promoted to the size of the other.
    def __add__(self, other):
        shape = Shape.promoted_shape(self, other)
        if shape is not None:
            return shape
        elif self.size == other.size:
            return self
        else:
            raise Exception("Incompatible dimensions.")

    # Handles matrix and scalar multiplication.
    def __mul__(self, other):
        shape = Shape.promoted_shape(self, other)
        if shape is not None:
            return shape
        elif self.cols == other.rows:
            return Shape(self.rows, other.cols)
        else:
            raise Exception("Incompatible dimensions.")

    # Returns the shape of the expression if scalars were promoted.
    # Returns None if neither the lefthand nor righthand shapes can be
    # promoted.
    @staticmethod
    def promoted_shape(lh_shape, rh_shape):
        if lh_shape.size == (1,1):
            return rh_shape
        elif rh_shape.size == (1,1):
            return lh_shape
        else:
            return None