"""Small Dictionary for Demo Mode translations"""


class SD:
    def translate_in(language):
        words = {}
        words["English"] = "in"
        words["Chinese"] = "在"
        words["Dutch"] = "in"
        words["French"] = "dans"
        words["Italian"] = "nel"
        words["Japanese"] = "に"
        words["Korean"] = "에"
        words["Portuguese"] = "no"
        words["Russian"] = "в"
        words["Spanish"] = "en"
        return words[language]

    def translate_assert(language):
        words = {}
        words["English"] = "ASSERT"
        words["Chinese"] = "断言"
        words["Dutch"] = "CONTROLEREN"
        words["French"] = "VÉRIFIER"
        words["Italian"] = "VERIFICARE"
        words["Japanese"] = "検証"
        words["Korean"] = "확인"
        words["Portuguese"] = "VERIFICAR"
        words["Russian"] = "ПОДТВЕРДИТЬ"
        words["Spanish"] = "VERIFICAR"
        return words[language]

    def translate_assert_text(language):
        words = {}
        words["English"] = "ASSERT TEXT"
        words["Chinese"] = "断言文本"
        words["Dutch"] = "CONTROLEREN TEKST"
        words["French"] = "VÉRIFIER TEXTE"
        words["Italian"] = "VERIFICARE TESTO"
        words["Japanese"] = "テキストを確認する"
        words["Korean"] = "텍스트 확인하는"
        words["Portuguese"] = "VERIFICAR TEXTO"
        words["Russian"] = "ПОДТВЕРДИТЬ ТЕКСТ"
        words["Spanish"] = "VERIFICAR TEXTO"
        return words[language]

    def translate_assert_exact_text(language):
        words = {}
        words["English"] = "ASSERT EXACT TEXT"
        words["Chinese"] = "确切断言文本"
        words["Dutch"] = "CONTROLEREN EXACTE TEKST"
        words["French"] = "VÉRIFIER EXACTEMENT TEXTE"
        words["Italian"] = "VERIFICARE TESTO ESATTO"
        words["Japanese"] = "正確なテキストを確認する"
        words["Korean"] = "정확한 텍스트를 확인하는"
        words["Portuguese"] = "VERIFICAR TEXTO EXATO"
        words["Russian"] = "ПОДТВЕРДИТЬ ТЕКСТ ТОЧНО"
        words["Spanish"] = "VERIFICAR TEXTO EXACTO"
        return words[language]

    def translate_assert_link_text(language):
        words = {}
        words["English"] = "ASSERT LINK TEXT"
        words["Chinese"] = "断言链接文本"
        words["Dutch"] = "CONTROLEREN LINKTEKST"
        words["French"] = "VÉRIFIER TEXTE DU LIEN"
        words["Italian"] = "VERIFICARE TESTO DEL COLLEGAMENTO"
        words["Japanese"] = "リンクテキストを確認する"
        words["Korean"] = "링크 텍스트 확인"
        words["Portuguese"] = "VERIFICAR TEXTO DO LINK"
        words["Russian"] = "ПОДТВЕРДИТЬ ССЫЛКУ"
        words["Spanish"] = "VERIFICAR TEXTO DEL ENLACE"
        return words[language]

    def translate_assert_non_empty_text(language):
        words = {}
        words["English"] = "ASSERT NON-EMPTY TEXT"
        words["Chinese"] = "断言非空文本"
        words["Dutch"] = "CONTROLEREN NIET-LEGE TEKST"
        words["French"] = "VÉRIFIER TEXTE NON VIDE"
        words["Italian"] = "VERIFICARE TESTO NON VUOTO"
        words["Japanese"] = "空ではないテキストを確認する"
        words["Korean"] = "비어 있지 않은 텍스트 확인하는"
        words["Portuguese"] = "VERIFICAR TEXTO NÃO VAZIO"
        words["Russian"] = "ПОДТВЕРДИТЬ НЕПУСТОЙ ТЕКСТ"
        words["Spanish"] = "VERIFICAR TEXTO NO VACÍO"
        return words[language]

    def translate_assert_attribute(language):
        words = {}
        words["English"] = "ASSERT ATTRIBUTE"
        words["Chinese"] = "断言属性"
        words["Dutch"] = "CONTROLEREN ATTRIBUUT"
        words["French"] = "VÉRIFIER ATTRIBUT"
        words["Italian"] = "VERIFICARE ATTRIBUTO"
        words["Japanese"] = "属性を確認する"
        words["Korean"] = "특성 확인"
        words["Portuguese"] = "VERIFICAR ATRIBUTO"
        words["Russian"] = "ПОДТВЕРДИТЬ АТРИБУТ"
        words["Spanish"] = "VERIFICAR ATRIBUTO"
        return words[language]

    def translate_assert_title(language):
        words = {}
        words["English"] = "ASSERT TITLE"
        words["Chinese"] = "断言标题"
        words["Dutch"] = "CONTROLEREN TITEL"
        words["French"] = "VÉRIFIER TITRE"
        words["Italian"] = "VERIFICARE TITOLO"
        words["Japanese"] = "タイトルを確認"
        words["Korean"] = "제목 확인"
        words["Portuguese"] = "VERIFICAR TÍTULO"
        words["Russian"] = "ПОДТВЕРДИТЬ НАЗВАНИЕ"
        words["Spanish"] = "VERIFICAR TÍTULO"
        return words[language]

    def translate_assert_title_contains(language):
        words = {}
        words["English"] = "ASSERT TITLE CONTAINS"
        words["Chinese"] = "断言标题包含"
        words["Dutch"] = "CONTROLEREN TITEL BEVAT"
        words["French"] = "VÉRIFIER TITRE CONTIENT"
        words["Italian"] = "VERIFICARE TITOLO CONTIENE"
        words["Japanese"] = "タイトル部分文字列を確認する"
        words["Korean"] = "제목 부분 확인"
        words["Portuguese"] = "VERIFICAR TÍTULO CONTÉM"
        words["Russian"] = "ПОДТВЕРДИТЬ НАЗВАНИЕ СОДЕРЖИТ"
        words["Spanish"] = "VERIFICAR TÍTULO CONTIENE"
        return words[language]

    def translate_assert_url(language):
        words = {}
        words["English"] = "ASSERT URL"
        words["Chinese"] = "断言 URL"
        words["Dutch"] = "CONTROLEREN URL"
        words["French"] = "VÉRIFIER URL"
        words["Italian"] = "VERIFICARE URL"
        words["Japanese"] = "URL を確認する"
        words["Korean"] = "URL 확인"
        words["Portuguese"] = "VERIFICAR URL"
        words["Russian"] = "ПОДТВЕРДИТЬ URL"
        words["Spanish"] = "VERIFICAR URL"
        return words[language]

    def translate_assert_url_contains(language):
        words = {}
        words["English"] = "ASSERT URL CONTAINS"
        words["Chinese"] = "断言 URL 包含"
        words["Dutch"] = "CONTROLEREN URL BEVAT"
        words["French"] = "VÉRIFIER URL CONTIENT"
        words["Italian"] = "VERIFICARE URL CONTIENE"
        words["Japanese"] = "URL を確認する"
        words["Korean"] = "URL 확인"
        words["Portuguese"] = "VERIFICAR URL CONTÉM"
        words["Russian"] = "ПОДТВЕРДИТЬ URL СОДЕРЖИТ"
        words["Spanish"] = "VERIFICAR URL CONTIENE"
        return words[language]

    def translate_assert_no_404_errors(language):
        words = {}
        words["English"] = "ASSERT NO 404 ERRORS"
        words["Chinese"] = "检查断开的链接"
        words["Dutch"] = "CONTROLEREN OP 404 FOUTEN"
        words["French"] = "AFFIRMEZ PAS D'ERREURS 404"
        words["Italian"] = "CONTROLLA ERRORI 404"
        words["Japanese"] = "リンク切れを確認する"
        words["Korean"] = "끊어진 링크 확인"
        words["Portuguese"] = "VERIFICAR SE HÁ ERROS 404"
        words["Russian"] = "ПРОВЕРИТЬ ОШИБКИ 404"
        words["Spanish"] = "VERIFICAR SI HAY ERRORES 404"
        return words[language]

    def translate_assert_no_js_errors(language):
        words = {}
        words["English"] = "ASSERT NO JS ERRORS"
        words["Chinese"] = "检查JS错误"
        words["Dutch"] = "CONTROLEREN OP JS FOUTEN"
        words["French"] = "AFFIRMEZ PAS D'ERREURS JS"
        words["Italian"] = "CONTROLLA ERRORI JS"
        words["Japanese"] = "JSエラーを確認する"
        words["Korean"] = "JS 오류 확인"
        words["Portuguese"] = "VERIFICAR SE HÁ ERROS JS"
        words["Russian"] = "ПРОВЕРИТЬ ОШИБКИ JS"
        words["Spanish"] = "VERIFICAR SI HAY ERRORES JS"
        return words[language]
