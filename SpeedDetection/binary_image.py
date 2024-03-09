import numpy as np

class BinaryImage:
    """
    A class that represents a binary image.
    ______________________

    Attributes:
        `width (int):`
            The width of the image.
        `height (int):`
            The height of the image.
        `matrix (np.ndarray):`
            The matrix of the image.
        `visited (np.ndarray):`
            The visited matrix of the image.
        `__bounding_boxes (list):`
            The bounding boxes of the image.
    ______________________

    Methods:
        `get_boxes() -> list:`
            Returns a list of the bounding boxes of the image.
        `__init__(matrix: np.ndarray, width: int, height: int) -> None:`
            Initializes the image with the given matrix, width and height.

    """

    def __init__(self, matrix : np.ndarray, width: int, height: int) -> None:
        """
        Initializes the image with the given matrix, width and height.
        ______________________

        Parameters[in]:
            `matrix (np.ndarray):`
                The matrix of the image.
            `width (int):`
                The width of the image.
            `height (int):`
                The height of the image.
        ______________________

        Unit tests:
            `tests/binary_image_test.py`: `test_binary_image__init__()`
            `tests/binary_image_test.py`: `test_binary_image__init__2()`

        """
        self.width = width
        self.height = height
        self.matrix = matrix
        self.visited = np.zeros((height, width), dtype=bool)
        self.__bounding_boxes = None

    def get_boxes(self) -> list:
        """
        On first call, computes the bounding boxes of the image and returns them.
        On subsequent calls, returns the previously computed bounding boxes.
        ______________________

        Returns:
            `list:`
                A list of the bounding boxes of the image.
        ______________________

        Unit tests:
            `tests/binary_image_test.py`: `test_binary_image__get_boxes__()`
            `tests/binary_image_test.py`: `test_binary_image__get_boxes__2()`
            `tests/binary_image_test.py`: `test_binary_image__get_boxes__3()`

        """
        from shape_object import ShapeObject
        if self.__bounding_boxes is not None:
            return self.__bounding_boxes

        self.__bounding_boxes = list()
        shape_objects = list()

        for y in range(self.height):
            for x in range(self.width):
                if not self.visited[y, x] and self.matrix[y, x] == 1:
                    new_object = ShapeObject(x, y, self, compute=True)
                    shape_objects.append(new_object)

                self.visited[y, x] = True

        self.__bounding_boxes = [shape_object.get_bounding_box() for shape_object in shape_objects]
        return self.__bounding_boxes

