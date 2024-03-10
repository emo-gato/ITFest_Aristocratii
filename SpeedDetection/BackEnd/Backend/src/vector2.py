class Vector2:
    """
    A class that represents a 2D vector.
    ______________________

    Attributes:
        `x (int):`
            The x coordinate of the vector.
        `y (int):`
            The y coordinate of the vector.

    ______________________

    Methods:
        `__add__(other: Vector2) -> Vector2:`
            Returns the sum of the two vectors.
        `__eq__(other: Vector2) -> bool:`
            Returns True if the vectors are equal, False otherwise.
        `__str__() -> str:`
            Returns a string representation of the vector.
        `__init__(x: int, y: int) -> None:`
            Initializes the vector with the given coordinates.
        
    """
    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the vector with the given coordinates.
        ______________________

        Parameters[in]:
            `x (int):`
                The x coordinate of the vector.
            `y (int):`
                The y coordinate of the vector.
        ______________________

        Unit test:
            `tests/vector2_test.py`: `test_vector2__init__()`
            `tests/vector2_test.py`: `test_vector2__init__2()`

        """
        self.x = x
        self.y = y

    def __add__(self, other: "Vector2") -> "Vector2":
        """
        Returns:
            `Vector2:`
                The sum of the two vectors.
        ______________________

        Parameters[in]:
            `other (Vector2):`
                The other vector.
        ______________________

        Unit tests:
            `tests/vector2_test.py`: `test_vector2__add__()`
            `tests/vector2_test.py`: `test_vector2__add__2()`
        ______________________

        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Vector2") -> bool:
        """
        Returns:
            `bool:`
                True if the vectors are equal, False otherwise.
        ______________________

        Parameters[in]:
            `other (Vector2):`
                The other vector.
        ______________________

        Unit tests:
            `tests/vector2_test.py`: `test_vector2__eq__()`
            `tests/vector2_test.py`: `test_vector2__eq__2()`

        """
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """
        Returns:
            `str:`
                A string representation of the vector.
        ______________________

        Unit test:
            `tests/vector2_test.py`: `test_vector2__str__()`
        """
        return f'{{"x": {self.x}, "y": {self.y}}}'


DIRECTIONS = [
    Vector2(1, 0), # right
    Vector2(-1, 0), # left
    Vector2(0, 1), # down
    Vector2(0, -1), # up
    Vector2(1, 1), # down right
    Vector2(1, -1), # up right
    Vector2(-1, -1), # up left
    Vector2(-1, 1) # down left
]

