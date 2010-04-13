#############################################################################
# Copyright (c) 2010 by Casey Duncan
# Portions copyright (c) 2009 The Super Effective Team 
#                             (www.supereffective.org)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#############################################################################

from __future__ import division

import math
import planar
from planar.util import cached_property


class Vec2(tuple):
    """Two dimensional immutable vector.
    
    :param x:
    :type x: float
    :param y:
    :type y: float
    """

    def __new__(self, x, y):
		return tuple.__new__(Vec2, ((x * 1.0, y * 1.0)))

    @classmethod
    def polar(cls, angle, length=1.0):
        """Create a vector from polar coordinates

        :param angle: Vector angle in degrees from the positive x-axis.
        :type angle: float
        :param length: The length of the vector.
        :type length: float
        :return: ``Vec2`` instance.
        """
        radians = math.radians(angle)
        vec = tuple.__new__(cls, (math.cos(radians) * length, math.sin(radians) * length))
        vec.__dict__['length'] = length * 1.0
        return vec

    def __str__(self):
        """Concise string representation."""
        return "Vec2(%.2f, %.2f)" % self

    def __repr__(self):
        """Precise string representation."""
        return "Vec2(%r, %r)" % self

    @property
    def x(self):
        """The horizontal coordinate."""
        return self[0]

    @property
    def y(self):
        """The vertical coordinate."""
        return self[1]

    @cached_property
    def length(self):
        """The length or scalar magnitude of the vector."""
        return self.length2 ** 0.5

    @cached_property
    def length2(self):
        """The square of the length of the vector."""
        return self[0] ** 2 + self[1] ** 2

    @cached_property
    def is_null(self):
        """Flag indicating if the vector is effectively zero-length.
        
        :return: True if the vector length < EPSILON.
        """
        return self.length2 < planar.EPSILON2

    def almost_equals(self, other):
        """Compare vectors for approximate equality.

        :param other: Vector being compared.
        :type other: Vec2
        :return: True if distance between the vectors < ``EPSILON``.
        """
        return ((self[0] - other[0])**2 
            + (self[1] - other[1])**2) < planar.EPSILON2

    def normalized(self):
        """Return the vector scaled to unit length.
        
        Do not use this method if the vector may be null,
        instead use :meth:`safe_normalized`.
        """
        L = self.length
        v = tuple.__new__(Vec2, (self[0] / L, self[1] / L))
        v.__dict__['length'] = v.__dict__['length2'] = 1.0
        return v

    def safe_normalized(self):
        """Return the vector scaled to unit length. If the vector
        is null, the null vector is returned. This is safer, but
        slightly slower than :meth:`normalized`.
        """
        if not self.is_null:
            return self.normalized()
        else:
            return null

    @cached_property
    def angle(self):
        """The angle the vector makes to the positive x axis in the range
        ``(-180, 180]``.
        """
        return math.degrees(math.atan2(self[1], self[0]))

    def angle_to(self, other):
        """Compute the smallest angle from this vector to another.

        :param other: Vector to compute the angle to.
        :type other: Vec2
        :return: Angle in degrees in the range ``(-180, 180]``.
        """
        return other.angle - self.angle

    def __gt__(self, other):
        """Compare vector length, longer vectors are "greater than"
        shorter vectors.
        """
        return self.length2 > other.length2

    def __ge__(self, other):
        """Compare vector length, longer vectors are "greater than"
        shorter vectors.
        """
        return self.length2 >= other.length2

    def __lt__(self, other):
        """Compare vector length, shorter vectors are "less than"
        longer vectors.
        """
        return self.length2 < other.length2

    def __le__(self, other):
        """Compare vector length, shorter vectors are "less than"
        longer vectors.
        """
        return self.length2 <= other.length2

    def __add__(self, other):
        """Add the vectors componentwise.

        :param other: The vector to add.
        :type other: Vec2
        """
        return tuple.__new__(Vec2, (self[0] + other[0], self[1] + other[1]))

    __iadd__ = __add__

    def __sub__(self, other):
        """Subtract the vectors componentwise.

        :param other: The vector to substract.
        :type other: Vec2
        """
        return tuple.__new__(Vec2, (self[0] - other[0], self[1] - other[1]))

    __isub__ = __sub__

    def __mul__(self, other):
        """Either multiply the vector by a scalar or componentwise
        with another vector.

        :param other: The object to multiply by.
        :type other: Vec2 or float
        """
        try:
            other = float(other)
            return tuple.__new__(Vec2, (self[0] * other, self[1] * other))
        except TypeError:
            return tuple.__new__(Vec2, (self[0] * other[0], self[1] * other[1]))
    
    __rmul__ = __imul__ = __mul__

    def __div__(self, other):
        """Divide the vector by a scalar or componentwise
        by another vector.

        :param other: The value to divide by.
        :type other: Vec2 or float
        """
        try:
            other = float(other)
            return tuple.__new__(Vec2, (self[0] / other, self[1] / other))
        except TypeError:
            return tuple.__new__(Vec2, (self[0] / other[0], self[1] / other[1]))

    __truediv__ = __idiv__ = __div__

    def __floordiv__(self, other):
        """Divide the vector by a scalar or componentwise by
        another vector, rounding down.

        :param other: The value to divide by.
        :type other: Vec2 or float
        """
        try:
            other = float(other)
            return tuple.__new__(Vec2, (self[0] // other, self[1] // other))
        except TypeError:
            return tuple.__new__(Vec2, (self[0] // other[0], self[1] // other[1]))

    __ifloordiv__ = __floordiv__

    def __neg__(self):
        """Compute the unary negation of the vector."""
        return tuple.__new__(Vec2, (-self[0], -self[1]))


null = Vec2(0, 0)


# vim: ai ts=4 sts=4 et sw=4 tw=78
