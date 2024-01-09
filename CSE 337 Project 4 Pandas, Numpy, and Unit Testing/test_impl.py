import unittest
import impl

class MyUnitTestingForPhysicalInfo(unittest.TestCase):

    def setUp(self):
        self.physical_info = impl.PhysicalInfo()

    # Tests for set_name
    def test_valid_name_with_normal_length(self):
        try:
            self.physical_info.set_name("John Doe")
        except ValueError:
            self.fail("set_name raised ValueError unexpectedly!")

    def test_valid_name_with_minimum_length(self):
        try:
            self.physical_info.set_name("Jo")
        except ValueError:
            self.fail("set_name raised ValueError unexpectedly!")

    def test_invalid_name_with_special_characters(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_name("John#Doe")

    def test_invalid_name_with_no_alphabet_characters(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_name("123456789")
            
    # Tests for set_name with invalid types
    def test_invalid_name_with_numeric_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_name(123)

    def test_invalid_name_with_none_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_name(None)

    # Tests for set_gender
    def test_valid_gender_male(self):
        try:
            self.physical_info.set_gender("M")
        except ValueError:
            self.fail("set_gender raised ValueError unexpectedly!")

    def test_valid_gender_female(self):
        try:
            self.physical_info.set_gender("F")
        except ValueError:
            self.fail("set_gender raised ValueError unexpectedly!")

    def test_invalid_gender(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_gender("No Gender")
    
    # Tests for set_gender with invalid types
    def test_invalid_gender_with_numeric_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_gender(1)

    def test_invalid_gender_with_none_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_gender(None)

    # Tests for set_height
    def test_valid_normal_height(self):
        try:
            self.physical_info.set_height(50)
        except ValueError:
            self.fail("set_height raised ValueError unexpectedly!")

    def test_valid_minimum_height(self):
        try:
            self.physical_info.set_height(17)
        except ValueError:
            self.fail("set_height raised ValueError unexpectedly!")

    def test_valid_maximum_height(self):
        try:
            self.physical_info.set_height(84)
        except ValueError:
            self.fail("set_height raised ValueError unexpectedly!")

    def test_invalid_height_below_minimum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_height(16)

    def test_invalid_height_above_maximum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_height(85)

    # Tests for set_height with invalid types
    def test_invalid_height_with_string_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_height("average height")

    def test_invalid_height_with_float_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_height(70.5)

    # Tests for set_temperature
    def test_valid_normal_temperature(self):
        try:
            self.physical_info.set_temperature(100.0)
        except ValueError:
            self.fail("set_temperature raised ValueError unexpectedly!")
    
    def test_valid_minimum_temperature(self):
        try:
            self.physical_info.set_temperature(95.0)
        except ValueError:
            self.fail("set_temperature raised ValueError unexpectedly!")

    def test_valid_maximum_temperature(self):
        try:
            self.physical_info.set_temperature(104.0)
        except ValueError:
            self.fail("set_temperature raised ValueError unexpectedly!")

    def test_invalid_temperature_below_minimum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_temperature(94.9)

    def test_invalid_temperature_above_maximum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_temperature(104.1)

    # Tests for set_temperature with invalid types
    def test_invalid_temperature_with_string_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_temperature("normal")

    def test_invalid_temperature_with_integer_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_temperature(98)

    # Tests for set_date
    def test_valid_date_minimum_year(self):
        try:
            self.physical_info.set_date("01-01-1900")
        except ValueError:
            self.fail("set_date raised ValueError unexpectedly!")

    def test_valid_date_maximum_year(self):
        try:
            self.physical_info.set_date("12-31-2100")
        except ValueError:
            self.fail("set_date raised ValueError unexpectedly!")

    def test_invalid_date_year_below_minimum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_date("01-01-1899")

    def test_invalid_date_year_above_maximum(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_date("01-01-2101")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_date("99-12-2020")

    # Tests for set_date with invalid types
    def test_invalid_date_with_numeric_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_date(20201231)

    def test_invalid_date_with_none_input(self):
        with self.assertRaises(ValueError):
            self.physical_info.set_date(None)

if __name__ == '__main__':
    unittest.main()
