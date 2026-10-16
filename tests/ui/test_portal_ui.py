"""Browser tests with Playwright (REQ-01, REQ-05, REQ-08)."""
import re

import pytest
from playwright.sync_api import Page, expect

from tests.conftest import create_request


def fill_form(page: Page, **overrides):
    values = {
        "full_name": "Ram Bahadur Thapa",
        "citizenship_no": "05-03-68-04321",
        "district": "Sunsari",
        "phone": "9801234567",
        "service_type": "Passport Recommendation",
    }
    values.update(overrides)
    page.fill("#full_name", values["full_name"])
    page.fill("#citizenship_no", values["citizenship_no"])
    page.select_option("#district", values["district"])
    page.fill("#phone", values["phone"])
    page.select_option("#service_type", values["service_type"])


def test_tc16_citizen_can_submit_and_gets_tracking_id(page: Page):
    page.goto("/")
    fill_form(page)
    page.click("button[type=submit]")
    expect(page.locator("#result")).to_be_visible()
    expect(page.locator("#tracking-id")).to_have_text(re.compile(r"SR-\d{4}-\d{5}"))


def test_tc17_empty_form_shows_an_error_for_every_field(page: Page):
    page.goto("/")
    page.click("button[type=submit]")
    for field in ["full_name", "citizenship_no", "district", "phone", "service_type"]:
        expect(page.locator(f'[data-error-for="{field}"]')).not_to_be_empty()
    expect(page.locator("#result")).to_be_hidden()


def test_tc18_bad_phone_shows_phone_error_only(page: Page):
    page.goto("/")
    fill_form(page, phone="12345")
    page.click("button[type=submit]")
    expect(page.locator('[data-error-for="phone"]')).to_contain_text("10-digit")
    expect(page.locator('[data-error-for="full_name"]')).to_be_empty()


def test_tc19_track_link_shows_current_status(page: Page):
    page.goto("/")
    fill_form(page)
    page.click("button[type=submit]")
    page.click("#track-link")
    expect(page.locator('[data-field="status"]')).to_have_text("Submitted")


@pytest.mark.xfail(strict=True, reason="BUG-003: track page shows full citizenship number")
def test_tc20_track_page_masks_citizenship_number(page: Page, api):
    tid = create_request(api, citizenship_no="27-02-70-05678")["tracking_id"]
    page.goto(f"/track?id={tid}")
    expect(page.locator('[data-field="citizenship_no"]')).to_have_text("XX-XX-XX-X5678")


def test_tc21_unknown_tracking_id_shows_not_found(page: Page):
    page.goto("/track?id=SR-1999-99999")
    expect(page.locator("#not-found")).to_be_visible()
