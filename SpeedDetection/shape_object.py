from bounding_box import BoundingBox
from vector2 import Vector2, DIRECTIONS
from binary_image import BinaryImage
from collections import deque

class ShapeObject:
    """
    A class that represents a shape object in an image.
    ______________________

    Attributes:
        `image (BinaryImage):`
            The image that the object belongs to.
        `source_node (Node):`
            The source node of the object.
        `__bounding_box (BoundingBox):`
            The bounding box of the object.
        `__coverage_ratio (float):`
            The coverage ratio of the object.
        `__computed (bool):`
            A flag that indicates if the bounding box and coverage ratio have been computed.
    ______________________

    Methods:
        `get_bounding_box() -> BoundingBox:`
            Returns the bounding box of the object.
        `__init__(x: int, y: int, image: BinaryImage) -> None:`
            Initializes the object with the given coordinates and image.
    """
    def __init__(self, x: int, y: int, image : BinaryImage, compute : bool =False) -> None:
        """
        Initializes the object with the given coordinates and image.
        ______________________

        Parameters[in]:
            `x (int):`
                The x coordinate of the object.
            `y (int):`
                The y coordinate of the object.
            `image (BinaryImage):`
                The image that the object belongs to.
            `compute (bool):`
                Optional parameter, defaults to False.
                If True, the compute method will be called at the end of the initialization.
        ______________________

        Unit test:
            `tests/shape_object_test.py`: `test_shape_object__init__()`

        """
        self.image = image
        self.source_node = Vector2(x, y)
        self.__bounding_box__ : BoundingBox | None = None
        self.__coverage_ratio__ : float | None = None
        self.__computed__ = False

        if compute:
            self.compute()


    def compute(self) -> None:
        """
        Computes the bounding box of the object and the coverage ratio( pixels occupied / area of the bounding box ).
        Storing them in the `__bounding_box__` and `__coverage_ratio__` attributes.

        Returns None.
        ______________________

        Parameters[out]:
            `__bounding_box__ (BoundingBox):`
                Is used to store the bounding box of the object.
            `__coverage_ratio__ (float):`
                Is used to store the coverage ratio of the object.
            `__computed__ (bool):`
                Is used to indicate if the bounding box and coverage ratio have been computed.
                On subsequent calls, the method will return immediately.
            `self.image.visited (np.ndarray):`
                Is used to mark the visited nodes.
        ______________________

        Global variables:
            `DIRECTIONS (list):` 
                A list of the directions in which the algorithm will search for neighbours.
                Will not be modified.
        ______________________

        Unit tests:
            `tests/shape_object_test.py`: `test_shape_object__compute__()`
            `tests/shape_object_test.py`: `test_shape_object__compute__2()`
            `tests/shape_object_test.py`: `test_shape_object__compute__3()`

        """

        if self.__computed__:
            return

        stack = deque([self.source_node])
        self.image.visited[self.source_node.y][self.source_node.x] = True

        nodes = deque()

        vector2_filter = lambda v: \
            0 <= v.x < self.image.width \
            and 0 <= v.y < self.image.height \
            and self.image.visited[v.y][v.x] == False \
            and self.image.matrix[v.y][v.x] == 1 

        while stack:
            node = stack.pop()

            neighbours = list(filter(vector2_filter, map(lambda direction: node + direction, DIRECTIONS)))

            for neighbour in neighbours:
                self.image.visited[neighbour.y, neighbour.x] = True

            stack.extend(neighbours)
            nodes.append(node)


        min_x, min_y = self.image.width, self.image.height
        max_x, max_y = -1, -1

        for node in nodes:
            if node.x < min_x:
                min_x = node.x

            if node.y < min_y:
                min_y = node.y

            if node.x > max_x:
                max_x = node.x

            if node.y > max_y:
                max_y = node.y

        self.__bounding_box__ = BoundingBox(Vector2(min_x, min_y), Vector2(max_x, max_y))
        self.__coverage_ratio__ = len(nodes) / self.__bounding_box__.get_size()
        self.__computed__ = True

    def get_bounding_box(self) -> BoundingBox:
        """
        A method that returns the bounding box of the object.
        At first, it calls the compute method, if it hasn't been called before.
        On subsequent calls, it returns the previously computed bounding box immediately.
        ______________________

        Returns:
            `__bounding_box__ (BoundingBox):`
                The bounding box of the object.
        ______________________

        Unit test:
            `tests/shape_object_test.py`: `test_shape_object__get_bounding_box__()`

        """
        if not self.__computed__:
            self.compute()

        if self.__bounding_box__ is None:
            raise Exception("Failed to compute bounding box.")

        return self.__bounding_box__


    def get_coverage_ratio(self) -> float:
        """
        A method that returns the coverage ratio of the object.
        At first, it calls the compute method, if it hasn't been called before.
        On subsequent calls, it returns the previously computed coverage ratio immediately.
        ______________________

        Returns:
            `__coverage_ratio__ (float):`
                The coverage ratio of the object.
        ______________________

        Unit test:
            `tests/shape_object_test.py`: `test_shape_object__get_coverage_ratio__()`

        """
        if not self.__computed__:
            self.compute()
        
        if self.__coverage_ratio__ is None:
            raise Exception("Failed to compute coverage ratio.")

        return self.__coverage_ratio__
