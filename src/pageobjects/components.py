from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import os
root_path = os.path.dirname(os.path.abspath(__file__))


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )


class Slider(Component):
    SLIDER = '.price-slider__begunok'

    def move(self, offset):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SLIDER)
        )
        ac = ActionChains(self.driver)
        ac.click_and_hold(element).move_by_offset(offset, 0).perform()


class BaseSettings(Component):
    GAME_RADIOBOX = '#product-type-5208'
    MM_GAME_RADIOBOX = '#pad-mail_mir_abstract'
    CAMPAIGN_NAME_INPUT = '.base-setting__campaign-name__input'
    MM_LABEL = '.base-setting__pads-item__label'

    def choose_game(self):
        game_radiobox = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.GAME_RADIOBOX)
        )

        game_radiobox.click()

    def choose_mm(self):
        mm_radiobox = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.MM_GAME_RADIOBOX)
        )

        mm_radiobox.click()

    def set_campaign_name(self, name):
        campaign = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CAMPAIGN_NAME_INPUT)
        )
        campaign.clear()
        campaign.send_keys(name)

    def get_mm_label_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.MM_LABEL).text
        )

    def is_right_platforms_opened(self):
        OK_PROFILES_CHECKBOX = '#pad-odkl_profiles_abstract'
        OK_APPS_CHECKBOX = '#pad-odkl_games_abstract'
        wait = WebDriverWait(self.driver, 30, 0.1)
        mm_game = wait.until(
            lambda d: d.find_element_by_css_selector(self.MM_GAME_RADIOBOX)
        )
        ok_profiles = wait.until(
            lambda d: d.find_element_by_css_selector(OK_PROFILES_CHECKBOX)
        )
        ok_apps = wait.until(
            lambda d: d.find_element_by_css_selector(OK_APPS_CHECKBOX)
        )

        return mm_game.is_displayed() and ok_profiles.is_displayed() and ok_apps.is_displayed()


class BannerForm(Component):
    BANNER_INPUT = '.banner-form__input[data-name="%s"]'
    FILE_PATH = root_path + '/ya.png'
    SUBMIT_BANNER = '.banner-form__save-button'

    def set_image(self):
        SUBMIT_IMAGE = '.image-cropper__save'
        image = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector('.banner-form__img-file')
        )
        image.send_keys(self.FILE_PATH)

        #self.driver.execute_script("var xxx = document.querySelector('.jcrop-holder').children[0]; xxx.style.width = xxx.style.height = '100px';")
        submit_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(SUBMIT_IMAGE)
        )
        submit_button.click()

    def set_title(self, title_text):
        title = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BANNER_INPUT % 'title')
        )
        title.send_keys(title_text)

    def set_text(self, text_value):
        text = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BANNER_INPUT % 'text')
        )
        text.send_keys(text_value)

    def set_url(self, url_text):
        url = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.BANNER_INPUT % 'url')
        )
        url[1].send_keys(url_text)

    def submit(self):
        wait = WebDriverWait(self.driver, 30, 0.1)
        banner_preview = BannerPreview(self.driver)
        wait.until(
            banner_preview.wait_for_image
        )
        submit_btn = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.SUBMIT_BANNER)))
        ac = ActionChains(self.driver)
        ac.move_to_element(submit_btn).click(submit_btn).perform()


class BannerPreview(Component):
    PREVIEW_BLOCK = '.added-banner'
    PREVIEW_TITLE = '.banner-preview__title'
    PREVIEW_TEXT = '.banner-preview__text'
    PREVIEW_IMAGE = '.banner-preview__img'

    def set_preview_block(self):
        self.driver = WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.PREVIEW_BLOCK))
        )

    def get_title(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREVIEW_TITLE).text
        )

    def get_text(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREVIEW_TEXT).text
        )

    def get_image(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            self.wait_for_image
        )

    def wait_for_image(self, driver):
        images = driver.find_elements_by_css_selector(self.PREVIEW_IMAGE)
        for image in images:
            if image.is_displayed():
                return image

    def get_image_size(self):
        image = self.get_image()
        width = image.value_of_css_property("width")
        height = image.value_of_css_property("height")
        return width, height


class IncomeBlock(Component):
    ABOVE_AVERAGE = '#income_group-9288'
    AVERAGE = '#income_group-9287'
    BELOW_AVERAGE = '#income_group-9286'
    INCOME_BLOCK = '.all-settings__item[data-name="income_group"]'
    UNCOLLAPSE_BTN = '.campaign-setting__value'
    INPUT = '.campaign-setting__input'

    def set_income_block(self):
        self.driver = WebDriverWait(self.driver, 30, 1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.INCOME_BLOCK))
        )

    def uncollapse_income_group(self):
        uncollapse = WebDriverWait(self.driver, 30, 1).until(
            lambda d: d.find_element_by_css_selector(self.UNCOLLAPSE_BTN)
        )
        uncollapse.click()

    def check_above_avg(self):
        above_avg = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.ABOVE_AVERAGE)
        )
        above_avg.click()

    def check_avg(self):
        avg = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.AVERAGE)
        )
        avg.click()

    def check_below_avg(self):
        below_avg = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BELOW_AVERAGE)
        )
        below_avg.click()

    def what_is_checked(self):
        items = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.INPUT)
        )

        data = {
            'above_avg': False,
            'avg': False,
            'below_avg': False
        }

        if items[0].is_selected():
            data['above_avg'] = True
        if items[1].is_selected():
            data['avg'] = True
        if items[2].is_selected():
            data['below_avg'] = True

        return data


class DateBlock(Component):
    DATE_BLOCK = '.all-settings__item[data-name="date"]'
    UNCOLLAPSE_BTN = '.campaign-setting__value'
    DATEPICKER = '.hasDatepicker[data-name="%s"]'

    def set_date_block(self):
        self.driver = WebDriverWait(self.driver, 30, 1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.DATE_BLOCK))
        )

    def uncollapse_datepickers(self):
        uncollapse = WebDriverWait(self.driver, 30, 1).until(
            lambda d: d.find_element_by_css_selector(self.UNCOLLAPSE_BTN)
        )
        uncollapse.click()

    def open_datepicker(self, type, driver):
        date_picker = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DATEPICKER % type)
        )
        date_picker.click()
        return DatePicker(driver)

    def get_datepicker_value(self, type):
        date_picker = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DATEPICKER % type)
        )
        return date_picker.get_attribute('value')

    def set_datepicker_value(self, type, date):
        date_picker = WebDriverWait(self.driver, 30, 1).until(
            lambda d: d.find_element_by_css_selector(self.DATEPICKER % type)
        )
        date_picker.send_keys(date)
        date_picker.send_keys(Keys.RETURN)


class DatePicker(Component):
    MONTH = '.ui-datepicker-month'
    YEAR = '.ui-datepicker-year'
    NEXT = '.ui-datepicker-next'
    PREV = '.ui-datepicker-prev'
    DAY = '[data-handler="selectDay"]'

    def set_month(self, month):
        select = self.driver.find_element_by_css_selector(self.MONTH)
        Select(select).select_by_visible_text(month)

    def set_year(self, year):
        select = self.driver.find_element_by_css_selector(self.YEAR)
        Select(select).select_by_visible_text(year)

    def pick_day(self, day):
        days = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.DAY)
        )
        days[day-1].click()

    def next_month(self):
        next_m = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.NEXT)
        )
        next_m.click()

    def prev_month(self):
        prev_m = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PREV)
        )
        prev_m.click()


class CampaignInfo(Component):
    CAMPAIGN = '.campaign-title__name'
    CAMPAIGN_ID = '.campaign-title__id'

    def get_campaign_name(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CAMPAIGN).text
        )

    def get_campaign_id(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CAMPAIGN_ID).text[:-1]
        )


class CampaignActions(Component):
    EDIT = '.control__link_edit'
    DELETE = '.control__preset_delete'

    def edit_campaign(self):
        edit_btn = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EDIT)
        )
        edit_btn.click()

    def delete_campaign(self):
        delete_btn = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DELETE)
        )
        delete_btn.click()


class CreateCampaign(Component):
    CREATE = '.main-button__label'

    def create(self):
        create_btn = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CREATE)
        )
        create_btn.click()