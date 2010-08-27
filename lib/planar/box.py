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
from planar.util import cached_property, assert_unorderable


class BoundingBox(object):
    """An axis-aligned immutable rectangular shape described
    by two points that define the minimum and maximum
    corners.

    :param points: Iterable containing one or more :class:`~planar.Vec2` 
        objects.
    """

    def __init__(self, points):
        self._init_min_max(points)
    
    def _init_min_max(self, points):
        points = iter(points)
        try:
            min_x, min_y = max_x, max_y = points.next()
        except StopIteration:
            raise ValueError, "BoundingBox() requires at least one point"
        for x, y in points:
            if x < min_x:
                min_x = x * 1.0
            elif x > max_x:
                max_x = x * 1.0
            if y < min_y:
                min_y = y * 1.0
            elif y > max_y:
                max_y = y * 1.0
        self._min = planar.Vec2(min_x, min_y)
        self._max = planar.Vec2(max_x, max_y)
    
    @property
    def bounding_box(self):
        """The bounding box for this shape. For a BoundingBox instance,
        this is always itself.
        """
        return self
    
    @property
    def min_point(self):
        """The minimum corner point for the shape. This is the corner
        with the smallest x and y value.
        """
        return self._min
    
    @property
    def max_point(self):
        """The maximum corner point for the shape. This is the corner
        with the largest x and y value.
        """
        return self._max

    @property
    def width(self):
        """The width of the box."""
        return self._max.x - self._min.x
    
    @property
    def height(self):
        """The height of the box."""
        return self._max.y - self._min.y
    
    @cached_property
    def center(self):
        """The center point of the box."""
        return (self._min + self._max) / 2.0
    
    @cached_property
    def is_empty(self):
        """True if the box has zero area."""
        width, height = self._max - self._min
        return not width or not height

    @classmethod
    def from_points(cls, points):
        """Create a bounding box that encloses all of the specified points.
        """
        box = object.__new__(cls)
        box._init_min_max(points)
        return box

    @classmethod
    def from_shapes(cls, shapes):
        """Creating a bounding box that completely encloses all of the
        shapes provided.
        """
        shapes = iter(shapes)
        try:
            shape = shapes.next()
        except StopIteration:
            raise ValueError, (
                "BoundingBox.from_shapes(): requires at least one shape")
        min_x, min_y = shape.bounding_box.min_point
        max_x, max_y = shape.bounding_box.max_point

        for shape in shapes:
            x, y = shape.bounding_box.min_point
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            x, y = shape.bounding_box.max_point
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        box = object.__new__(cls)
        box._min = planar.Vec2(min_x, min_y)
        box._max = planar.Vec2(max_x, max_y)
        return box
    
    @classmethod
    def from_center(cls, center, width, height):
        """Create a bounding box centered at a particular point

        :param center: Center point
        :type center: :class:`~planar.Vec2`
        :param width: Box width.
        :type width: float
        :param height: Box height.
        :type height: float
        """
        cx, cy = center
        half_w = width / 2.0
        half_h = height / 2.0
        return cls.from_points([
            (cx - half_w, cy - half_h),
            (cx + half_w, cy + half_h),
            ])
    
    def inflate(self, amount):
        """Return a new box resized from this one. The new
        box has its size changed by the specified amount,
        but remains centered on the same point.

        :param amount: The quantity to add to the width and
            height of the box. A scalar value changes
            both the width and height equally. A vector
            will change the width and height independently.
            Negative values reduce the size accordingly.
        :type amount: float or :class:`~planar.Vec2`
        """
        try:
            dx, dy = amount
        except TypeError:
            dx = dy = amount
        dv = planar.Vec2(dx, dy) / 2.0
        return self.from_points((self._min - dv, self._max + dv))
    
    def contains(self, other):
        """Return True if the box completely contains the specified object.

        :param other: A point vector, or a shape with a bounding box.
        :type other: :class:`~planar.Vec2` or :class:`~planar.Shape`
        """
        try:
            box = other.bounding_box
        except AttributeError:
            x, y = other
            return (self._min.x <= x <= self._max.x 
                and self._min.y <= y <= self._max.y)
        else:
            return (self._min.x <= box.min_point.x <= self._max.x 
                and self._min.x <= box.max_point.x <= self._max.x 
                and self._min.y <= box.min_point.y <= self._max.y
                and self._min.y <= box.max_point.y <= self._max.y)
    
    def fit(self, other):
        """Create a new shape by translating and scaling other so that
        it fits in this bounding box. Other is scaled evenly so that
        it retains the same aspect ratio.

        :param other: A transformable shape with a bounding box.
        """
        if isinstance(other, BoundingBox):
            scale = min(self.width / other.width, self.height / other.height)
            return other.from_center(
                self.center, other.width * scale, other.height * scale)
        else:
            try:
                other_bbox = other.bounding_box
            except AttributeError:
                raise ValueError('Cannot fit object with no bounding box')
            offset = planar.Affine.translation(self.center - other_bbox.center)
            scale = planar.Affine.scale(min(self.width / other_bbox.width,
                self.height / other_bbox.height))
            return other * (offset * scale)


# vim: ai ts=4 sts=4 et sw=4 tw=78

