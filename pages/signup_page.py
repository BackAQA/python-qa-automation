
from playwright.sync_api import Page

from pages.base_page import BasePage


class SignupPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Main signup form
        self.signup_form = self.page.locator(
            "form[action='/signup']"
        )

        # Account information
        self.title_mr = self.signup_form.locator("#id_gender1")
        self.title_mrs = self.signup_form.locator("#id_gender2")

        self.name_input = self.signup_form.locator("#name")
        self.email_input = self.signup_form.locator("#email")
        self.password_input = self.signup_form.locator("#password")

        # Date of birth
        self.day_select = self.signup_form.locator("#days")
        self.month_select = self.signup_form.locator("#months")
        self.year_select = self.signup_form.locator("#years")

        # Preferences
        self.newsletter_checkbox = self.signup_form.locator(
            "#newsletter"
        )

        self.special_offers_checkbox = self.signup_form.locator(
            "#optin"
        )

        # Address information
        self.first_name_input = self.signup_form.locator(
            "#first_name"
        )

        self.last_name_input = self.signup_form.locator(
            "#last_name"
        )

        self.company_input = self.signup_form.locator(
            "#company"
        )

        self.address1_input = self.signup_form.locator(
            "#address1"
        )

        self.address2_input = self.signup_form.locator(
            "#address2"
        )

        self.country_select = self.signup_form.locator(
            "#country"
        )

        self.state_input = self.signup_form.locator(
            "#state"
        )

        self.city_input = self.signup_form.locator(
            "#city"
        )

        self.zipcode_input = self.signup_form.locator(
            "#zipcode"
        )

        self.mobile_number_input = self.signup_form.locator(
            "#mobile_number"
        )

        # Create account
        self.create_account_button = self.signup_form.get_by_role(
            "button",
            name="Create Account",
            exact=True
        )

    def select_title(self, title: str = "Mr") -> None:
        if title == "Mr":
            self.title_mr.check()
        elif title == "Mrs":
            self.title_mrs.check()
        else:
            raise ValueError(
                "Title must be either 'Mr' or 'Mrs'"
            )

    def fill_account_information(
        self,
        password: str,
        day: str,
        month: str,
        year: str,
        title: str = "Mr"
    ) -> None:
        self.select_title(title)

        self.password_input.fill(password)

        self.day_select.select_option(label=day)
        self.month_select.select_option(label=month)
        self.year_select.select_option(label=year)

    def set_preferences(
        self,
        newsletter: bool = False,
        special_offers: bool = False
    ) -> None:
        if newsletter:
            self.newsletter_checkbox.check()
        else:
            self.newsletter_checkbox.uncheck()

        if special_offers:
            self.special_offers_checkbox.check()
        else:
            self.special_offers_checkbox.uncheck()

    def fill_address_information(
        self,
        first_name: str,
        last_name: str,
        address1: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile_number: str,
        company: str = "",
        address2: str = ""
    ) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)

        self.company_input.fill(company)

        self.address1_input.fill(address1)
        self.address2_input.fill(address2)

        self.country_select.select_option(label=country)

        self.state_input.fill(state)
        self.city_input.fill(city)
        self.zipcode_input.fill(zipcode)
        self.mobile_number_input.fill(mobile_number)

    def create_account(self) -> None:
        self.create_account_button.click()
