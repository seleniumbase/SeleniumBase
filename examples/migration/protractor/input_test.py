from seleniumbase import BaseCase


class AngularMaterialInputTests(BaseCase):

    def test_invalid_input(self):
        # Test that there's an error for an invalid input
        self.open("https://material.angular.io/components/input/examples")
        self.assert_element(".mat-button-wrapper > .mat-icon")
        self.type("#mat-input-1", "invalid")
        self.assert_element("mat-error")
