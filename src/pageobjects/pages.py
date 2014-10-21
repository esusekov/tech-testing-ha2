import urlparse
from components import AuthForm, TopMenu, Slider, BaseSettings, BannerForm, BannerPreview, IncomeBlock, DateBlock, \
    CampaignActions, CampaignInfo, CreateCampaign


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def slider(self):
        return Slider(self.driver)

    @property
    def base_settings(self):
        return BaseSettings(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    @property
    def banner_preview(self):
        return BannerPreview(self.driver)

    @property
    def income_block(self):
        return IncomeBlock(self.driver)

    @property
    def date_block(self):
        return DateBlock(self.driver)

    @property
    def create_campaign(self):
        return CreateCampaign(self.driver)


class CampaignPage(Page):
    PATH = '/ads/campaigns/'

    @property
    def campaign_info(self):
        return CampaignInfo(self.driver)

    @property
    def campaign_actions(self):
        return CampaignActions(self.driver)


class EditPage(CreatePage):
    pass