# Russian Language Test
from seleniumbase.translate.russian import ТестНаСелен  # noqa


class МойТестовыйКласс(ТестНаСелен):

    def test_пример_1(self):
        self.открытый("https://ru.wikipedia.org/wiki/")
        self.проверить_элемент('[title="Русский язык"]')
        self.проверить_текст("Википедия", "h2.main-wikimedia-header")
        self.обновить_текст("#searchInput", "МГУ")
        self.нажмите("#searchButton")
        self.проверить_текст("университет", "#firstHeading")
        self.проверить_элемент('img[alt="МГУ, вид с воздуха.jpg"]')
        self.обновить_текст("#searchInput", "приключения Шурика")
        self.нажмите("#searchButton")
        self.проверить_текст("Операция «Ы» и другие приключения Шурика")
        self.проверить_элемент('img[alt="Постер фильма"]')
        self.назад()
        self.проверить_правду("университет" in self.получить_текущий_URL())
        self.вперед()
        self.проверить_правду("Шурика" in self.получить_текущий_URL())
