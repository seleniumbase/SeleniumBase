"""
This module contains methods for opening jquery-confirm boxes.
These helper methods SHOULD NOT be called directly from tests.
"""
from seleniumbase.fixtures import constants
from seleniumbase.fixtures import js_utils


form_code = (
    """'<form align="center" action="" class="jqc_form">' +
    '<div class="form-group">' +
    '<input style="font-size:20px; background-color: #f8fdfd; ' +
    ' width: 84%%; border: 1px solid blue; ' +
    ' box-shadow:inset 0 0 2px 2px #f4fafa;"' +
    ' type="text" class="jqc_input" />' +
    '</div>' +
    '</form>'"""
)


def jquery_confirm_button_dialog(driver, message, buttons, options=None):
    js_utils.activate_jquery_confirm(driver)
    # These defaults will be overwritten later if set
    theme = constants.JqueryConfirm.DEFAULT_THEME
    border_color = constants.JqueryConfirm.DEFAULT_COLOR
    width = constants.JqueryConfirm.DEFAULT_WIDTH
    if options:
        for option in options:
            if option[0].lower() == "theme":
                theme = option[1]
            elif option[0].lower() == "color":
                border_color = option[1]
            elif option[0].lower() == "width":
                width = option[1]
            else:
                raise Exception('Unknown option: "%s"' % option[0])
    if not message:
        message = ""
    key_row = ""
    if len(buttons) == 1:  # There's only one button as an option
        key_row = "keys: ['enter', 'y', '1'],"  # Shortcut: "Enter","Y","1"
    b_html = (
        """button_%s: {
            btnClass: 'btn-%s',
            text: '<b>%s</b>',
            %s
            action: function(){
                jqc_status = '%s';
                $jqc_status = jqc_status;
                jconfirm.lastButtonText = jqc_status;
            }
        },"""
    )
    all_buttons = ""
    btn_count = 0
    for button in buttons:
        btn_count += 1
        text = button[0]
        text = js_utils.escape_quotes_if_needed(text)
        if len(buttons) > 1 and text.lower() == "yes":
            key_row = "keys: ['y'],"
            if btn_count < 10:
                key_row = "keys: ['y', '%s']," % btn_count
        elif len(buttons) > 1 and text.lower() == "no":
            key_row = "keys: ['n'],"
            if btn_count < 10:
                key_row = "keys: ['n', '%s']," % btn_count
        elif len(buttons) > 1:
            if btn_count < 10:
                key_row = "keys: ['%s']," % btn_count
        color = button[1]
        if not color:
            color = "blue"
        new_button = b_html % (btn_count, color, text, key_row, text)
        all_buttons += new_button

    content = (
        '<div></div><font color="#0066ee">%s</font>'
        "" % (message)
    )
    content = js_utils.escape_quotes_if_needed(content)
    overlay_opacity = "0.32"
    if theme.lower() == "supervan":
        overlay_opacity = "0.56"
    if theme.lower() == "bootstrap":
        overlay_opacity = "0.64"
    if theme.lower() == "modern":
        overlay_opacity = "0.5"
    if theme.lower() == "material":
        overlay_opacity = "0.4"
    jqcd = (
        """jconfirm({
            boxWidth: '%s',
            useBootstrap: false,
            containerFluid: true,
            bgOpacity: %s,
            type: '%s',
            theme: '%s',
            animationBounce: 1,
            typeAnimated: true,
            animation: 'scale',
            draggable: true,
            dragWindowGap: 1,
            container: 'body',
            title: '%s',
            content: '<div></div>',
            buttons: {
                %s
            }
        });"""
        % (
            width,
            overlay_opacity,
            border_color,
            theme,
            content,
            all_buttons
        )
    )
    driver.execute_script(jqcd)


def jquery_confirm_text_dialog(driver, message, button=None, options=None):
    js_utils.activate_jquery_confirm(driver)
    # These defaults will be overwritten later if set
    theme = constants.JqueryConfirm.DEFAULT_THEME
    border_color = constants.JqueryConfirm.DEFAULT_COLOR
    width = constants.JqueryConfirm.DEFAULT_WIDTH

    if not message:
        message = ""
    if button:
        if not type(button) is list and not type(button) is tuple:
            raise Exception('"button" should be a (text, color) tuple!')
        if len(button) != 2:
            raise Exception('"button" should be a (text, color) tuple!')
    else:
        button = ("Submit", "blue")
    if options:
        for option in options:
            if option[0].lower() == "theme":
                theme = option[1]
            elif option[0].lower() == "color":
                border_color = option[1]
            elif option[0].lower() == "width":
                width = option[1]
            else:
                raise Exception('Unknown option: "%s"' % option[0])
    btn_text = button[0]
    btn_color = button[1]
    if not btn_color:
        btn_color = "blue"
    content = (
        '<div></div><font color="#0066ee">%s</font>'
        "" % (message)
    )
    content = js_utils.escape_quotes_if_needed(content)
    overlay_opacity = "0.32"
    if theme.lower() == "supervan":
        overlay_opacity = "0.56"
    if theme.lower() == "bootstrap":
        overlay_opacity = "0.64"
    if theme.lower() == "modern":
        overlay_opacity = "0.5"
    if theme.lower() == "material":
        overlay_opacity = "0.4"
    jqcd = (
        """jconfirm({
            boxWidth: '%s',
            useBootstrap: false,
            containerFluid: true,
            bgOpacity: %s,
            type: '%s',
            theme: '%s',
            animationBounce: 1,
            typeAnimated: true,
            animation: 'scale',
            draggable: true,
            dragWindowGap: 1,
            container: 'body',
            title: '%s',
            content: '<div></div>' +
            %s,
            buttons: {
                formSubmit: {
                btnClass: 'btn-%s',
                text: '%s',
                action: function () {
                    jqc_input = this.$content.find('.jqc_input').val();
                    $jqc_input = this.$content.find('.jqc_input').val();
                    jconfirm.lastInputText = jqc_input;
                    $jqc_status = '%s';  // There is only one button
                },
            },
            },
            onContentReady: function () {
            var jc = this;
            this.$content.find('form.jqc_form').on('submit', function (e) {
                // User submits the form by pressing "Enter" in the field
                e.preventDefault();
                jc.$$formSubmit.trigger('click');  // Click the button
            });
            }
        });"""
        % (
            width,
            overlay_opacity,
            border_color,
            theme,
            content,
            form_code,
            btn_color,
            btn_text,
            btn_text
        )
    )
    driver.execute_script(jqcd)


def jquery_confirm_full_dialog(driver, message, buttons, options=None):
    js_utils.activate_jquery_confirm(driver)
    # These defaults will be overwritten later if set
    theme = constants.JqueryConfirm.DEFAULT_THEME
    border_color = constants.JqueryConfirm.DEFAULT_COLOR
    width = constants.JqueryConfirm.DEFAULT_WIDTH

    if not message:
        message = ""
    btn_count = 0
    b_html = (
        """button_%s: {
            btnClass: 'btn-%s',
            text: '%s',
            action: function(){
            jqc_input = this.$content.find('.jqc_input').val();
            $jqc_input = this.$content.find('.jqc_input').val();
            jconfirm.lastInputText = jqc_input;
            $jqc_status = '%s';
            }
        },"""
    )
    b1_html = (
            """formSubmit: {
                btnClass: 'btn-%s',
                text: '%s',
                action: function(){
                jqc_input = this.$content.find('.jqc_input').val();
                $jqc_input = this.$content.find('.jqc_input').val();
                jconfirm.lastInputText = jqc_input;
                jqc_status = '%s';
                $jqc_status = jqc_status;
                jconfirm.lastButtonText = jqc_status;
                }
            },"""
        )
    one_button_trigger = ""
    if len(buttons) == 1:
        # If there's only one button, allow form submit with "Enter/Return"
        one_button_trigger = "jc.$$formSubmit.trigger('click');"
    all_buttons = ""
    for button in buttons:
        text = button[0]
        text = js_utils.escape_quotes_if_needed(text)
        color = button[1]
        if not color:
            color = "blue"
        btn_count += 1
        if len(buttons) == 1:
            new_button = b1_html % (color, text, text)
        else:
            new_button = b_html % (btn_count, color, text, text)
        all_buttons += new_button
    if options:
        for option in options:
            if option[0].lower() == "theme":
                theme = option[1]
            elif option[0].lower() == "color":
                border_color = option[1]
            elif option[0].lower() == "width":
                width = option[1]
            else:
                raise Exception('Unknown option: "%s"' % option[0])

    content = (
        '<div></div><font color="#0066ee">%s</font>'
        "" % (message)
    )
    content = js_utils.escape_quotes_if_needed(content)
    overlay_opacity = "0.32"
    if theme.lower() == "supervan":
        overlay_opacity = "0.56"
    if theme.lower() == "bootstrap":
        overlay_opacity = "0.64"
    if theme.lower() == "modern":
        overlay_opacity = "0.5"
    if theme.lower() == "material":
        overlay_opacity = "0.4"
    jqcd = (
        """jconfirm({
            boxWidth: '%s',
            useBootstrap: false,
            containerFluid: true,
            bgOpacity: %s,
            type: '%s',
            theme: '%s',
            animationBounce: 1,
            typeAnimated: true,
            animation: 'scale',
            draggable: true,
            dragWindowGap: 1,
            container: 'body',
            title: '%s',
            content: '<div></div>' +
            %s,
            buttons: {
                %s
            },
            onContentReady: function () {
            var jc = this;
            this.$content.find('form.jqc_form').on('submit', function (e) {
                // User submits the form by pressing "Enter" in the field
                e.preventDefault();
                %s
            });
            }
        });"""
        % (
            width,
            overlay_opacity,
            border_color,
            theme,
            content,
            form_code,
            all_buttons,
            one_button_trigger
        )
    )
    driver.execute_script(jqcd)
