# -*- coding: utf-8 -*-
from seleniumbase import BaseCase


class AngularMaterialPaginatorTests(BaseCase):
    def test_pagination(self):
        self.open("https://material.angular.io/components/paginator/examples")
        self.assert_element(".mat-button-wrapper > .mat-icon")
        # Verify navigation to the next page
        self.click('button[aria-label="Next page"]')
        self.assert_exact_text("Page 2 of 10", ".mat-paginator-range-label")
        # Verify navigation to the previous page
        self.click('button[aria-label="Previous page"]')
        self.assert_exact_text("Page 1 of 10", ".mat-paginator-range-label")
        # Verify changed list length to 5 items per page
        self.click("mat-select > div")
        self.click("mat-option > .mat-option-text")
        self.assert_exact_text("Page 1 of 20", ".mat-paginator-range-label")
