from .vector import Vec
from typing import List, Self
from math import radians, cos, sin, pi

class Hitbox():
    """
    A polygonal shape that detects collisions with other polygonal shapes
    """
    # hmm this description is kinda bad

    def __init__(self, center: Vec, vertices: List[Vec]) -> None:
        # vertices in this case should be distance from 0 i think?
        self.center = center
        self.original_vertices = vertices
        self.vertices = vertices
        self.angle_rad = 0

    def set_size_rect(self, dx: float, dy: float) -> None:
        self.original_vertices = [
            Vec(-dx/2, -dy/2),
            Vec( dx/2, -dy/2),
            Vec( dx/2,  dy/2),
            Vec(-dx/2,  dy/2),
        ]
        self.vertices = self.original_vertices

    def set_size_rad(self, rad: float) -> None:
        points = []
        for i in range(6):
            points.append(Vec(rad * cos(2 * pi * i / 6), rad * sin(2 * pi * i / 6)))
        self.original_vertices = points
        self.vertices = points

    def set_rotation(self, angle: float, degrees = True) -> None:
        if degrees:
            self.angle_rad = -radians(angle)
        else:
            self.angle_rad = angle
        self.__update_rotation()

    def rotate(self, angle: float, degrees = True) -> None:
        if degrees:
            self.angle_rad -= radians(angle)
        else:
            self.angle_rad -= angle
        self.__update_rotation()

    def set_position(self, new_center: Vec) -> None:
        self.center = new_center

    def translate(self, translation: Vec) -> None:
        """ This does not move the center """
        translated = []
        for p in self.original_vertices:
            trans_x = p.x + translation.x
            trans_y = p.y + translation.y
            translated.append(Vec(trans_x, trans_y))
        self.original_vertices = translated


    def __update_rotation(self) -> None:
        cos_a = cos(self.angle_rad)
        sin_a = sin(self.angle_rad)
        rotated = []

        for p in self.original_vertices:
            rotated_x = p.x * cos_a - p.y * sin_a
            rotated_y = p.x * sin_a + p.y * cos_a
            rotated.append(Vec(rotated_x, rotated_y))
        self.vertices = rotated

    def get_hitbox(self) -> List[Vec]:
        real_hitbox = []
        for p in self.vertices:
            real_hitbox.append(p + self.center)
        return real_hitbox

    def project_to_axis(self, axis: Vec) -> Vec:
        # create a "shadow" using dot product
        dots = [point.dot(axis) for point in self.get_hitbox()]
        return Vec(min(dots), max(dots))

    def is_colliding(self, other: Self) -> bool:
        # apparently this method is called the Separating Axis Theorem
        axies = []

        # get all axies from hitboxes, and find their perpendicular axis
        for polygon in (self, other):
            poly = polygon.get_hitbox()
            for i in range(len(poly)):
                point1 = poly[i]
                point2 = poly[(i+1) % len(poly)]
                edge = point2 - point1
                normal = Vec(-edge.y, edge.x).normalize() # rotate 90 degrees and normalize
                axies.append(normal)

        for axis in axies:
            min1, max1 = self.project_to_axis(axis)
            min2, max2 = other.project_to_axis(axis)
            if max1 < min2 or max2 < min1:
                return False # a projection doesn't overlap

        return True # all projections overlap

__all__ = ["Hitbox"]
