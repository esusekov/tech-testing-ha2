# -*- coding: utf-8 -*-

from selenium.webdriver import DesiredCapabilities, Remote
import unittest
from src.pageobjects.pages import AuthPage, CreatePage, CampaignPage, EditPage
import os
import urlparse
import datetime


def get_current_date():
    date = datetime.datetime.now()
    return unicode(date.strftime('%d.%m.%Y'))


class MainTestCase(unittest.TestCase):

    def setUp(self):

        self.LOGIN = 'tech-testing-ha2-30@bk.ru'
        self.PASSWORD = os.environ.get('TTHA2PASSWORD')
        self.DOMAIN = '@bk.ru'

        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_domain(self.DOMAIN)
        auth_form.set_login(self.LOGIN)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

    def tearDown(self):
        self.driver.quit()

    def test_domain(self):
        url = urlparse.urlparse(self.driver.current_url)
        self.assertEqual(url.netloc, "target.mail.ru")

    def test_create_page(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        email = create_page.top_menu.get_email()
        self.assertEqual(self.LOGIN, email)

    def test_is_game_has_right_platforms(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        base_settings = create_page.base_settings
        base_settings.choose_game()

        self.assertTrue(base_settings.is_right_platforms_opened())

    def test_banner_preview(self):
        create_page = CreatePage(self.driver)
        create_page.open()
        base_settings = create_page.base_settings
        base_settings.choose_game()
        base_settings.choose_mm()
        banner_form = create_page.banner_form

        test_title = 'New banner'
        test_text = 'Super awesome ad'
        test_url = 'http://my.mail.ru/apps/666'
        test_width = '90px'
        test_height = '75px'

        banner_form.set_title(test_title)
        banner_form.set_text(test_text)
        banner_form.set_url(test_url)
        banner_form.set_image()
        banner_form.submit()
        banner_preview = create_page.banner_preview
        banner_preview.set_preview_block()

        self.assertEqual(banner_preview.get_title(), test_title)
        self.assertEqual(banner_preview.get_text(), test_text)

        res_width, res_height = banner_preview.get_image_size()
        self.assertEqual(res_width, test_width)
        self.assertEqual(res_height, test_height)

    def test_income_block(self):
        create_page = CreatePage(self.driver)
        create_page.open()

        income_block = create_page.income_block
        income_block.set_income_block()
        income_block.uncollapse_income_group()
        income_block.check_above_avg()
        income_block.check_avg()

        inputs = income_block.what_is_checked()
        self.assertTrue(inputs['above_avg'])
        self.assertTrue(inputs['avg'])
        self.assertFalse(inputs['below_avg'])

    def test_date_picker_with_wrong_date(self):
        test_date = '32.01.2014'
        create_page = CreatePage(self.driver)
        create_page.open()

        date_block = create_page.date_block
        date_block.set_date_block()
        date_block.uncollapse_datepickers()
        date_block.set_datepicker_value('from', test_date)

        res_date = date_block.get_datepicker_value('from')
        self.assertEqual(get_current_date(), res_date)

    def test_date_picker_from_time_is_later_then_to_time(self):
        from_date = {
            'year': '2016',
            'month': 'Янв',
            'day': 10
        }
        from_date_str = u'10.01.2016'
        to_date = {
            'year': '2014',
            'month': 'Ноя',
            'day': 10
        }
        to_date_str = u'10.11.2014'

        create_page = CreatePage(self.driver)
        create_page.open()
        date_block = create_page.date_block
        date_block.set_date_block()
        date_block.uncollapse_datepickers()

        from_datepicker = date_block.open_datepicker('from', self.driver)
        from_datepicker.set_year(from_date['year'])
        from_datepicker.set_month(from_date['month'])
        from_datepicker.pick_day(from_date['day'])

        to_datepicker = date_block.open_datepicker('to', self.driver)
        to_datepicker.set_year(to_date['year'])
        to_datepicker.set_month(to_date['month'])
        to_datepicker.pick_day(to_date['day'])

        res_from_str = date_block.get_datepicker_value('from')
        res_to_str = date_block.get_datepicker_value('to')
        self.assertEqual(res_from_str, to_date_str)
        self.assertEqual(res_to_str, from_date_str)

    def test_all_platforms_saved_after_campaign_creating(self):
        test_campaign_name = 'Super awesome campaign'
        test_title = 'New banner'
        test_text = 'Super awesome ad'
        test_url = 'http://my.mail.ru/apps/666'

        create_page = CreatePage(self.driver)
        create_page.open()

        base_settings = create_page.base_settings
        base_settings.set_campaign_name(test_campaign_name)
        base_settings.choose_game()
        base_settings.choose_mm()

        banner_form = create_page.banner_form
        banner_form.set_title(test_title)
        banner_form.set_text(test_text)
        banner_form.set_url(test_url)
        banner_form.set_image()
        banner_form.submit()

        create_page.create_campaign.create()

        campaign_page = CampaignPage(self.driver)

        self.assertEqual(campaign_page.campaign_info.get_campaign_name(), test_campaign_name)

        campaign_page.campaign_actions.edit_campaign()

        edit_page = EditPage(self.driver)

        self.assertEqual(edit_page.base_settings.get_mm_label_text(), u'Мой Мир: профили, приложения и другие страницы')

        campaign_page.open()
        campaign_page.campaign_actions.delete_campaign()

    def test_incomes_saved_after_campaign_creating(self):
        test_campaign_name = 'Super awesome campaign'
        test_title = 'New banner'
        test_text = 'Super awesome ad'
        test_url = 'http://my.mail.ru/apps/666'

        create_page = CreatePage(self.driver)
        create_page.open()

        base_settings = create_page.base_settings
        base_settings.set_campaign_name(test_campaign_name)
        base_settings.choose_game()
        base_settings.choose_mm()

        banner_form = create_page.banner_form
        banner_form.set_title(test_title)
        banner_form.set_text(test_text)
        banner_form.set_url(test_url)
        banner_form.set_image()
        banner_form.submit()

        income_block = create_page.income_block
        income_block.set_income_block()
        income_block.uncollapse_income_group()
        income_block.check_above_avg()
        income_block.check_avg()

        create_page.create_campaign.create()

        campaign_page = CampaignPage(self.driver)
        campaign_page.campaign_actions.edit_campaign()

        edit_page = EditPage(self.driver)

        income_block = edit_page.income_block
        income_block.set_income_block()
        income_block.uncollapse_income_group()
        inputs = income_block.what_is_checked()

        self.assertTrue(inputs['above_avg'])
        self.assertTrue(inputs['avg'])
        self.assertFalse(inputs['below_avg'])

        campaign_page.open()
        campaign_page.campaign_actions.delete_campaign()

    def test_dates_saved_after_campaign_creating(self):
        test_campaign_name = 'Super awesome campaign'
        test_title = 'New banner'
        test_text = 'Super awesome ad'
        test_url = 'http://my.mail.ru/apps/666'

        from_date = {
            'year': '2014',
            'month': 'Ноя',
            'day': 10
        }
        from_date_str = u'10.11.2014'
        to_date = {
            'year': '2016',
            'month': 'Ноя',
            'day': 10
        }
        to_date_str = u'10.11.2016'

        create_page = CreatePage(self.driver)
        create_page.open()

        base_settings = create_page.base_settings
        base_settings.set_campaign_name(test_campaign_name)
        base_settings.choose_game()
        base_settings.choose_mm()

        banner_form = create_page.banner_form
        banner_form.set_title(test_title)
        banner_form.set_text(test_text)
        banner_form.set_url(test_url)
        banner_form.set_image()
        banner_form.submit()

        date_block = create_page.date_block
        date_block.set_date_block()
        date_block.uncollapse_datepickers()

        from_datepicker = date_block.open_datepicker('from', self.driver)
        from_datepicker.set_year(from_date['year'])
        from_datepicker.set_month(from_date['month'])
        from_datepicker.pick_day(from_date['day'])

        to_datepicker = date_block.open_datepicker('to', self.driver)
        to_datepicker.set_year(to_date['year'])
        to_datepicker.set_month(to_date['month'])
        to_datepicker.pick_day(to_date['day'])

        create_page.create_campaign.create()

        campaign_page = CampaignPage(self.driver)
        campaign_page.campaign_actions.edit_campaign()

        edit_page = EditPage(self.driver)

        date_block = edit_page.date_block
        date_block.set_date_block()
        date_block.uncollapse_datepickers()

        res_from_str = date_block.get_datepicker_value('from')
        res_to_str = date_block.get_datepicker_value('to')
        self.assertEqual(res_from_str, from_date_str)
        self.assertEqual(res_to_str, to_date_str)

        campaign_page.open()
        campaign_page.campaign_actions.delete_campaign()






