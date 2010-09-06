"""Polygon class unit tests"""

from __future__ import division
import sys
import math
import unittest
from nose.tools import assert_equal, assert_almost_equal, raises


class PolygonBaseTestCase(object):

    @raises(TypeError)
    def test_too_few_args(self):
        self.Polygon()

    @raises(ValueError)
    def test_no_verts(self):
        self.Polygon([])

    @raises(ValueError)
    def test_too_few_verts(self):
        self.Polygon([(0,0), (1,1)])

    def test_init_triangle(self):
        poly = self.Polygon([(-1,0), (1,1), (0,0)])
        assert_equal(len(poly), 3)
        assert_equal(tuple(poly), 
            (self.Vec2(-1,0), self.Vec2(1,1), self.Vec2(0,0)))

    def test_is_Seq2_subclass(self):
        import planar
        assert issubclass(self.Polygon, planar.Seq2)
        poly = self.Polygon([(-1,0), (-1,1), (0,0), (0, -1)])
        assert isinstance(poly, planar.Seq2)

    def test_triangle_is_known_convex(self):
        poly = self.Polygon([(-1,0), (1,1), (0,0)])
        assert poly.is_convex_known
        assert poly.is_convex

    def test_triangle_is_known_simple(self):
        poly = self.Polygon([(-1,0), (1,1), (0,0)])
        assert poly.is_simple_known
        assert poly.is_simple

    def test_convex_not_known(self):
        poly = self.Polygon([(-1,0), (-1,1), (0,0), (0, -1)])
        assert_equal(len(poly), 4)
        assert not poly.is_convex_known

    def test_specify_convex(self):
        poly = self.Polygon([(-1,0), (-1,1), (0,0), (0, -1)], 
            is_convex=True)
        assert_equal(len(poly), 4)
        assert poly.is_convex_known
        assert poly.is_convex
        assert poly.is_simple_known
        assert poly.is_simple

    def test_triangle_is_always_convex(self):
        poly = self.Polygon([(-1,0), (1,1), (0,0)], is_convex=False)
        assert poly.is_convex_known
        assert poly.is_convex
        assert poly.is_simple_known
        assert poly.is_simple

    def test_specify_simple(self):
        poly = self.Polygon([(-1,0), (-0.5, 0.5), (-1,1), (0,0), (0, -1)], 
            is_simple=True)
        assert poly.is_simple_known
        assert poly.is_simple
        assert not poly.is_convex_known

    def test_is_convex(self):
        poly = self.Polygon([(-1,0), (-1,1), (0,0), (0, -1)])
        assert not poly.is_convex_known
        assert poly.is_convex
        assert poly.is_convex_known
        assert poly.is_convex # test cached value

    def test_not_is_convex(self):
        poly = self.Polygon([(0,0), (-1,1), (0,0.5), (-1, -1)])
        assert not poly.is_convex_known
        assert not poly.is_convex
        assert poly.is_convex_known
        assert not poly.is_convex # test cached value

    def test_convex_is_simple(self):
        poly = self.Polygon([(-1,-1), (1,-1), (0.5,0), (0, 0)])
        assert not poly.is_simple_known
        assert poly.is_convex
        assert poly.is_simple_known
        assert poly.is_simple
        assert poly.is_simple # test cached value

    def test_non_convex_simple_unknown(self):
        poly = self.Polygon([(-1,-1), (1,-1), (1,0), (0, -0.9)])
        assert not poly.is_simple_known
        assert not poly.is_convex
        assert not poly.is_simple_known

    def test_is_simple(self):
        poly = self.Polygon([(0,0), (-1,-1), (-2, 0), (-1, 1)])
        assert not poly.is_simple_known
        assert poly.is_simple
        assert poly.is_simple_known
        assert poly.is_simple # test cached value

    def test_not_is_simple(self):
        poly = self.Polygon([(0,0), (-1,1), (1,1), (-1,0)])
        assert not poly.is_simple_known
        assert not poly.is_simple
        assert poly.is_simple_known
        assert not poly.is_simple # test cached value
    
    def test_mutation_invalidates_cached_properties(self):
        poly = self.Polygon([(0.5,0.5), (0.5,-0.5), (-0.5,-0.5), (-0.5,0.5)])
        assert poly.is_convex
        assert poly.is_simple
        assert poly.is_convex_known
        assert poly.is_simple_known
        poly[0] = (0, 0.6)
        assert not poly.is_convex_known
        assert not poly.is_simple_known
        assert poly.is_convex
        assert poly.is_simple
        assert poly.is_convex_known
        assert poly.is_simple_known
        poly[-1] = (0, 0)
        assert not poly.is_convex_known
        assert not poly.is_simple_known
        assert not poly.is_convex
        assert poly.is_simple
        assert poly.is_convex_known
        assert poly.is_simple_known
        poly[-1] = (1, 0)
        assert not poly.is_convex_known
        assert not poly.is_simple_known
        assert not poly.is_convex
        assert not poly.is_simple
        assert poly.is_convex_known
        assert poly.is_simple_known
        poly[0] = (0.5, 0.5)
        poly[1] = (0.5, -0.5)
        poly[2] = (-0.5, -0.5)
        poly[3] = (-0.5, 0.5)
        assert not poly.is_convex_known
        assert not poly.is_simple_known
        assert poly.is_convex
        assert poly.is_simple
        assert poly.is_convex_known
        assert poly.is_simple_known

    def test_regular(self):
        import planar
        poly = self.Polygon.regular(5, 1.5)
        assert_equal(len(poly), 5)
        assert poly.is_convex_known
        assert poly.is_simple_known
        assert poly.is_centroid_known
        assert poly.is_convex
        assert poly.is_simple
        assert isinstance(poly.centroid, planar.Vec2)
        assert_equal(poly.centroid, (0, 0))
        angle = 0
        for i in range(5):
            assert_equal(self.Vec2.polar(angle, 1.5), poly[i])
            angle += 72

    def test_regular_with_center_and_angle(self):
        import planar
        angle = -60
        poly = self.Polygon.regular(vertex_count=3, radius=2, 
            center=(-3, 1), angle=angle)
        assert_equal(len(poly), 3)
        assert poly.is_convex_known
        assert poly.is_simple_known
        assert poly.is_centroid_known
        assert poly.is_convex
        assert poly.is_simple
        assert isinstance(poly.centroid, planar.Vec2)
        assert_equal(poly.centroid, (-3, 1))
        for i in range(3):
            assert_equal(self.Vec2.polar(angle, 2) + (-3, 1), poly[i])
            angle += 120

    @raises(ValueError)
    def test_regular_too_few_sides(self):
        self.Polygon.regular(2, 1)

    def test_star(self):
        import planar
        poly = self.Polygon.star(5, 3, 5)
        assert_equal(len(poly), 10)
        assert poly.is_convex_known
        assert poly.is_simple_known
        assert poly.is_centroid_known
        assert not poly.is_convex
        assert poly.is_simple
        assert isinstance(poly.centroid, planar.Vec2)
        assert_equal(poly.centroid, (0, 0))
        angle = 0
        for i in range(5):
            assert_equal(self.Vec2.polar(angle, 3), poly[i * 2])
            angle += 36
            assert_equal(self.Vec2.polar(angle, 5), poly[i * 2 + 1])
            angle += 36

    def test_star_is_convex_with_same_radii(self):
        import planar
        poly = self.Polygon.star(9, 2, 2)
        assert_equal(len(poly), 18)
        assert poly.is_convex_known
        assert poly.is_simple_known
        assert poly.is_centroid_known
        assert poly.is_convex
        assert poly.is_simple
        assert isinstance(poly.centroid, planar.Vec2)
        assert_equal(poly.centroid, (0, 0))

    def test_star_with_center_and_angle(self):
        import planar
        poly = self.Polygon.star(peak_count=2, radius1=1.5, radius2=3, 
            center=(-11, 3), angle=15)
        assert_equal(len(poly), 4)
        assert poly.is_convex_known
        assert poly.is_simple_known
        assert poly.is_centroid_known
        assert not poly.is_convex
        assert poly.is_simple
        assert isinstance(poly.centroid, planar.Vec2)
        assert_equal(poly.centroid, (-11, 3))
        assert_equal(poly[0], self.Vec2.polar(15, 1.5) + (-11, 3))
        assert_equal(poly[1], self.Vec2.polar(105, 3) + (-11, 3))
        assert_equal(poly[2], self.Vec2.polar(195, 1.5) + (-11, 3))
        assert_equal(poly[3], self.Vec2.polar(285, 3) + (-11, 3))

    def test_star_with_one_negative_radius(self):
        import planar
        poly = self.Polygon.star(3, -1, 2)
        assert_equal(len(poly), 6)
        assert poly.is_convex_known
        assert not poly.is_simple_known
        assert not poly.is_centroid_known
        assert not poly.is_convex
        assert not poly.is_simple
        assert_equal(poly.centroid, None)

    @raises(ValueError)
    def test_star_too_few_peaks(self):
        self.Polygon.star(1, 1, 2)

    def test_centroid_convex(self):
        import planar
        poly = self.Polygon([(-1, -2), (2, -1), (1, 1), (-2, 1), (-3, -1)])
        assert poly.is_convex
        expected = self.Vec2(0, 0)
        for v in poly:
            expected += v
        expected /= len(poly)
        assert not poly.is_centroid_known
        assert_equal(poly.centroid, expected)
        assert isinstance(poly.centroid, planar.Vec2)
        assert poly.is_centroid_known
        assert_equal(poly.centroid, expected) # check cached value


class PyPolygonTestCase(PolygonBaseTestCase, unittest.TestCase):
    from planar.vector import Vec2, Seq2
    from planar.box import BoundingBox
    from planar.polygon import Polygon


if __name__ == '__main__':
    unittest.main()


# vim: ai ts=4 sts=4 et sw=4 tw=78
