from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class AngularMaterialPaginatorTests(BaseCase):
    def test_pagination(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.click_if_visible("button.mat-mdc-button")
        self.scroll_to("div.mat-mdc-paginator-page-size")
        # Set pagination to 5 items per page
        self.click("mat-select > div")
        self.click("mat-option:nth-of-type(1)")
        # Verify navigation to the next page
        self.click('button[aria-label="Next page"]')
        self.assert_exact_text(
            "6 – 10 of 50", ".mat-mdc-paginator-range-label"
        )
        # Verify navigation to the previous page
        self.click('button[aria-label="Previous page"]')
        self.assert_exact_text(
            "1 – 5 of 50", ".mat-mdc-paginator-range-label"
        )
        # Set pagination to 10 items per page
        self.click("mat-select > div")
        self.click("mat-option:nth-of-type(2)")
        # Verify page with correct number of pages
        self.assert_exact_text(
            "1 – 10 of 50", ".mat-mdc-paginator-range-label"
        )
