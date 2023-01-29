# Russian Language Test
from seleniumbase.translate.russian import ТестНаСелен
ТестНаСелен.main(__name__, __file__)


class МойТестовыйКласс(ТестНаСелен):
    def test_пример_1(self):
        self.открыть("https://ru.wikipedia.org/wiki/")
        self.подтвердить_элемент('[title="Русский язык"]')
        self.подтвердить_текст("Википедия", "h2.main-wikimedia-header")
        self.введите("#searchInput", "МГУ")
        self.нажмите("#searchButton")
        self.подтвердить_текст("университет", "#firstHeading")
        self.подтвердить_элемент('img[alt*="Главное здание МГУ"]')
        self.введите("#searchInput", "приключения Шурика")
        self.нажмите("#searchButton")
        self.подтвердить_текст("Операция «Ы» и другие приключения Шурика")
        self.подтвердить_элемент('img[alt="Постер фильма"]')
        self.назад()
        self.подтвердить_URL_содержит("университет")
        self.вперед()
        self.подтвердить_URL_содержит("Шурика")
