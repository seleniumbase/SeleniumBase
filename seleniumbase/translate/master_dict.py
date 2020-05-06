
# Master Dictionary

# Translations
# 0: English
# 1: Chinese
# 2: Dutch
# 3: French
# 4: Italian
# 5: Japanese
# 6: Korean
# 7: Portuguese
# 8: Russian
# 9: Spanish


class MD_F:
    # Master Dictionary Functions

    def get_languages_list():
        languages = []
        languages.append("English")
        languages.append("Chinese")
        languages.append("Dutch")
        languages.append("French")
        languages.append("Italian")
        languages.append("Japanese")
        languages.append("Korean")
        languages.append("Portuguese")
        languages.append("Russian")
        languages.append("Spanish")
        return languages

    def get_parent_classes_list():
        parent_classes = []
        parent_classes.append("BaseCase")
        parent_classes.append("硒测试用例")
        parent_classes.append("Testgeval")
        parent_classes.append("CasDeBase")
        parent_classes.append("CasoDiProva")
        parent_classes.append("セレニウムテストケース")
        parent_classes.append("셀레늄_테스트_케이스")
        parent_classes.append("CasoDeTeste")
        parent_classes.append("ТестНаСелен")
        parent_classes.append("CasoDePrueba")
        return parent_classes

    def get_parent_class_lang(parent_class):
        parent_class_lang = {}
        parent_class_lang["BaseCase"] = "English"
        parent_class_lang["硒测试用例"] = "Chinese"
        parent_class_lang["Testgeval"] = "Dutch"
        parent_class_lang["CasDeBase"] = "French"
        parent_class_lang["CasoDiProva"] = "Italian"
        parent_class_lang["セレニウムテストケース"] = "Japanese"
        parent_class_lang["셀레늄_테스트_케이스"] = "Korean"
        parent_class_lang["CasoDeTeste"] = "Portuguese"
        parent_class_lang["ТестНаСелен"] = "Russian"
        parent_class_lang["CasoDePrueba"] = "Spanish"
        if parent_class not in parent_class_lang.keys():
            raise Exception("Invalid parent_class {%s} not in {%s}!"
                            "" % (parent_class, parent_class_lang.keys()))
        return parent_class_lang[parent_class]

    def get_lang_parent_class(language):
        lang_parent_class = {}
        lang_parent_class["English"] = "BaseCase"
        lang_parent_class["Chinese"] = "硒测试用例"
        lang_parent_class["Dutch"] = "Testgeval"
        lang_parent_class["French"] = "CasDeBase"
        lang_parent_class["Italian"] = "CasoDiProva"
        lang_parent_class["Japanese"] = "セレニウムテストケース"
        lang_parent_class["Korean"] = "셀레늄_테스트_케이스"
        lang_parent_class["Portuguese"] = "CasoDeTeste"
        lang_parent_class["Russian"] = "ТестНаСелен"
        lang_parent_class["Spanish"] = "CasoDePrueba"
        if language not in lang_parent_class.keys():
            raise Exception("Invalid language {%s} not in {%s}!"
                            "" % (language, lang_parent_class.keys()))
        return lang_parent_class[language]

    def get_import_line(language):
        import_line = {}
        # - The Default Import Line:
        import_line["English"] = (
            "from seleniumbase import BaseCase")
        # - Translated Import Lines:
        import_line["Chinese"] = (
            "from seleniumbase.translate.chinese import 硒测试用例")
        import_line["Dutch"] = (
            "from seleniumbase.translate.dutch import Testgeval")
        import_line["French"] = (
            "from seleniumbase.translate.french import CasDeBase")
        import_line["Italian"] = (
            "from seleniumbase.translate.italian import CasoDiProva")
        import_line["Japanese"] = (
            "from seleniumbase.translate.japanese import セレニウムテストケース")
        import_line["Korean"] = (
            "from seleniumbase.translate.korean import 셀레늄_테스트_케이스")
        import_line["Portuguese"] = (
            "from seleniumbase.translate.portuguese import CasoDeTeste")
        import_line["Russian"] = (
            "from seleniumbase.translate.russian import ТестНаСелен")
        import_line["Spanish"] = (
            "from seleniumbase.translate.spanish import CasoDePrueba")
        if language not in import_line.keys():
            raise Exception("Invalid language {%s} not in {%s}!"
                            "" % (language, import_line.keys()))
        return import_line[language]


class MD_L_Codes:
    # Master Dictionary Language Codes
    lang = {}
    lang["English"] = 0
    lang["Chinese"] = 1
    lang["Dutch"] = 2
    lang["French"] = 3
    lang["Italian"] = 4
    lang["Japanese"] = 5
    lang["Korean"] = 6
    lang["Portuguese"] = 7
    lang["Russian"] = 8
    lang["Spanish"] = 9


class MD:
    # Master Dictionary
    md = {}
    num_langs = len(MD_L_Codes.lang)

    md["open"] = ["*"] * num_langs
    md["open"][0] = "open"
    md["open"][1] = "开启网址"
    md["open"][2] = "url_openen"
    md["open"][3] = "ouvrir_url"
    md["open"][4] = "apri_url"
    md["open"][5] = "URLを開く"
    md["open"][6] = "URL_열기"
    md["open"][7] = "abrir_url"
    md["open"][8] = "открыть"
    md["open"][9] = "abrir_url"

    md["click"] = ["*"] * num_langs
    md["click"][0] = "click"
    md["click"][1] = "单击"
    md["click"][2] = "klik"
    md["click"][3] = "cliquez_sur"
    md["click"][4] = "fare_clic"
    md["click"][5] = "クリックして"
    md["click"][6] = "클릭"
    md["click"][7] = "clique"
    md["click"][8] = "нажмите"
    md["click"][9] = "haga_clic"

    md["update_text"] = ["*"] * num_langs
    md["update_text"][0] = "update_text"
    md["update_text"][1] = "更新文本"
    md["update_text"][2] = "tekst_bijwerken"
    md["update_text"][3] = "modifier_le_texte"
    md["update_text"][4] = "aggiornare_il_testo"
    md["update_text"][5] = "テキストを更新"
    md["update_text"][6] = "텍스트를_업데이트"
    md["update_text"][7] = "atualizar_texto"
    md["update_text"][8] = "обновить_текст"
    md["update_text"][9] = "actualizar_texto"

    md["assert_text"] = ["*"] * num_langs
    md["assert_text"][0] = "assert_text"
    md["assert_text"][1] = "断言文本"
    md["assert_text"][2] = "controleren_tekst"
    md["assert_text"][3] = "vérifier_le_texte"
    md["assert_text"][4] = "verificare_il_testo"
    md["assert_text"][5] = "テキストを確認する"
    md["assert_text"][6] = "텍스트_확인"
    md["assert_text"][7] = "verificar_texto"
    md["assert_text"][8] = "подтвердить_текст"
    md["assert_text"][9] = "verificar_texto"
