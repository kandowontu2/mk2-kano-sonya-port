"""Synthetic in-memory cursor fixtures; no game art or files modified."""
import unittest
from PIL import Image
from qualify_selection_ui import masks,GREEN

class CursorPixelTests(unittest.TestCase):
    def fixture(self,center,color=(0,255,0),thickness=3,number_y=33,count=63):
        image=Image.new('RGB',(400,254))
        for y in range(20,98):
            for x in range(center-31,center+32):
                if x<center-31+thickness or x>=center+32-thickness or y<20+thickness or y>=98-thickness:
                    image.putpixel((x,y),color)
        for i in range(count):image.putpixel((center-3+i%7,number_y+i//7),color)
        return image

    def test_dim_and_bright_translated_native_geometry_match(self):
        reference=masks(self.fixture(110),110)
        self.assertEqual(masks(self.fixture(50,(0,123,0)),50),reference)
        self.assertEqual(masks(self.fixture(350),350),reference)
        self.assertEqual(len(reference[0]),63)

    def test_one_pixel_shift_is_detected(self):
        reference=masks(self.fixture(110),110)
        self.assertNotEqual(masks(self.fixture(51),50),reference)

    def test_thin_border_does_not_match_native_control(self):
        reference=masks(self.fixture(110),110)
        thin=masks(self.fixture(50,thickness=1),50)
        self.assertEqual(thin[0],reference[0])
        self.assertNotEqual(thin[1],reference[1])

    def test_p2_number_position_and_color_are_distinct(self):
        red={(123,0,0),(255,0,0)}
        image=self.fixture(50,(255,0,0),number_y=64,count=61)
        self.assertEqual(len(masks(image,50,red,64)[0]),61)
        self.assertFalse(masks(image,50,GREEN)[0])
        self.assertFalse(masks(image,50,red,33)[0])
