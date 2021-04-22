from seleniumbase import BaseCase


class AngularMaterialPaginatorTests(BaseCase):

    def test_pagination(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.assert_element(".mat-button-wrapper > .mat-icon")
        # Verify navigation to the next page
        self.click('button[aria-label="Next page"]')
        self.assert_exact_text("11 – 20 of 100", ".mat-paginator-range-label")
        # Verify navigation to the previous page
        self.click('button[aria-label="Previous page"]')
        self.assert_exact_text("1 – 10 of 100", ".mat-paginator-range-label")
        # Verify changed list length to 5 items per page
        self.click("mat-select > div")
        self.click("mat-option > .mat-option-text")
        self.assert_exact_text("1 – 5 of 100", ".mat-paginator-range-label")
