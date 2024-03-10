from vector2 import Vector2

class BoundingBox:
    """
    A class that represents a bounding box.
    ______________________

    Attributes:
        `point_a (Vector2):`
            The top left point of the bounding box.
        `point_b (Vector2):`
            The bottom right point of the bounding box.
    ______________________

    Methods:
        `size() -> int:`
            Returns the size of the bounding box.
        `__eq__(other: 'BoundingBox') -> bool:`
            Returns True if the bounding boxes are equal, False otherwise.
        `__str__() -> str:`
            Returns a string representation of the bounding box.
        `__init__(a: Vector2, b: Vector2) -> None:`
            Initializes the bounding box with the given points.
    
    """
    def __init__(self, a: Vector2, b: Vector2) -> None:
        """
        Initializes the bounding box with the given points.
        ______________________

        Parameters[in]:
            `a (Vector2):`
                The top left point of the bounding box.
            `b (Vector2):`
                The bottom right point of the bounding box.
        ______________________

        Unit test:
            `tests/bounding_box_test.py`: `test_bounding_box__init__()`

        """
        self.point_a = a
        self.point_b = b
        self.correspondence = None

    def __eq__(self, other: 'BoundingBox') -> bool:
        """
        Returns:
            `bool:`
                True if the bounding boxes are equal, False otherwise.
        ______________________

        Unit test:
            `tests/bounding_box_test.py`: `test_bounding_box__eq__()`

        """
        return self.point_a == other.point_a and self.point_b == other.point_b

    def __str__(self) -> str:
        """
        Returns:
            `str:`
                A string representation of the bounding box.
        ______________________

        Unit test:
            `tests/bounding_box_test.py`: `test_bounding_box__str__()`

        """
        return f'{{"point_a": {str(self.point_a)}, "point_b": {str(self.point_b)}}}'

    def get_size(self) -> int:
        """
        Returns:
            `int:`
                The size of the bounding box.
        ______________________

        Unit test:
            `tests/bounding_box_test.py`: `test_bounding_box__get_size__()`


        """
        return (self.point_b.x - self.point_a.x + 1) * (self.point_b.y - self.point_a.y + 1)

    def get_center(self) -> Vector2:
        """
        Returns:
            `Vector2:`
                The center of the bounding box.
        ______________________

        Unit test:
            `tests/bounding_box_test.py`: `test_bounding_box__get_center__()`

        """
        return Vector2(
            (self.point_a.x + self.point_b.x) // 2,
            (self.point_a.y + self.point_b.y) // 2
        )
    
    def has_correspondence(self, box):
        self.correspondence = box
        box.correspondence = self

    def get_correspondence(self):
        return self.correspondence


