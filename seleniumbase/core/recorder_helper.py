"""Generating SeleniumBase Python code from the Recorder"""


def generate_sbase_code(srt_actions):
    sb_actions = []
    for action in srt_actions:
        if action[0] == "begin" or action[0] == "_url_":
            if "%" in action[2]:
                try:
                    from urllib.parse import unquote

                    action[2] = unquote(action[2], errors="strict")
                except Exception:
                    pass
            if '"' not in action[2]:
                sb_actions.append('self.open("%s")' % action[2])
            elif "'" not in action[2]:
                sb_actions.append("self.open('%s')" % action[2])
            else:
                sb_actions.append(
                    'self.open("%s")' % action[2].replace('"', '\\"')
                )
        elif action[0] == "f_url":
            if "%" in action[2]:
                try:
                    from urllib.parse import unquote

                    action[2] = unquote(action[2], errors="strict")
                except Exception:
                    pass
            if '"' not in action[2]:
                sb_actions.append('self.open_if_not_url("%s")' % action[2])
            elif "'" not in action[2]:
                sb_actions.append("self.open_if_not_url('%s')" % action[2])
            else:
                sb_actions.append(
                    'self.open_if_not_url("%s")'
                    % action[2].replace('"', '\\"')
                )
        elif action[0] == "click":
            method = "click"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "dbclk":
            method = "double_click"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "js_cl":
            method = "js_click"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "js_ca":
            method = "js_click_all"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "jq_cl":
            method = "jquery_click"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "jq_ca":
            method = "jquery_click_all"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "r_clk":
            method = "context_click"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "canva":
            method = "click_with_offset"
            selector = action[1][0]
            p_x = action[1][1]
            p_y = action[1][2]
            if '"' not in selector:
                sb_actions.append(
                    'self.%s("%s", %s, %s)' % (method, selector, p_x, p_y)
                )
            else:
                sb_actions.append(
                    "self.%s('%s', %s, %s)" % (method, selector, p_x, p_y)
                )
        elif (
            action[0] == "input"
            or action[0] == "js_ty"
            or action[0] == "jq_ty"
            or action[0] == "pkeys"
        ):
            method = "type"
            if action[0] == "js_ty":
                method = "js_type"
            elif action[0] == "jq_ty":
                method = "jquery_type"
            elif action[0] == "pkeys":
                method = "press_keys"
            text = action[2].replace("\n", "\\n")
            if '"' not in action[1] and '"' not in text:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], text)
                )
            elif '"' not in action[1] and '"' in text:
                sb_actions.append(
                    'self.%s("%s", \'%s\')' % (method, action[1], text)
                )
            elif '"' in action[1] and '"' not in text:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")' % (method, action[1], text)
                )
            elif '"' in action[1] and '"' in text:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], text)
                )
        elif action[0] == "hover":
            method = "hover"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "e_mfa":
            method = "enter_mfa_code"
            text = action[2].replace("\n", "\\n")
            if '"' not in action[1] and '"' not in text:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], text)
                )
            elif '"' not in action[1] and '"' in text:
                sb_actions.append(
                    'self.%s("%s", \'%s\')' % (method, action[1], text)
                )
            elif '"' in action[1] and '"' not in text:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")' % (method, action[1], text)
                )
            elif '"' in action[1] and '"' in text:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], text)
                )
        elif action[0] == "h_clk":
            method = "hover_and_click"
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "ddrop":
            method = "drag_and_drop"
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "s_opt":
            method = "select_option_by_text"
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "set_v":
            method = "set_value"
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "cho_f":
            method = "choose_file"
            action[2] = action[2].replace("\\", "\\\\")
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "sw_fr":
            method = "switch_to_frame"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "sw_dc":
            sb_actions.append("self.switch_to_default_content()")
        elif action[0] == "sw_pf":
            sb_actions.append("self.switch_to_parent_frame()")
        elif action[0] == "s_c_f":
            method = "set_content_to_frame"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "s_c_d":
            method = "set_content_to_default"
            nested = action[1]
            if nested:
                method = "set_content_to_parent"
                sb_actions.append("self.%s()" % method)
            else:
                sb_actions.append("self.%s()" % method)
        elif action[0] == "sleep":
            method = "sleep"
            sb_actions.append("self.%s(%s)" % (method, action[1]))
        elif action[0] == "wf_el":
            method = "wait_for_element"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "as_el":
            method = "assert_element"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "as_ep":
            method = "assert_element_present"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "asenv":
            method = "assert_element_not_visible"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "s_at_" or action[0] == "s_ats":
            method = "set_attribute"
            if action[0] == "s_ats":
                method = "set_attributes"
            if '"' not in action[1][0]:
                sb_actions.append(
                    'self.%s("%s", "%s", "%s")'
                    % (method, action[1][0], action[1][1], action[1][2])
                )
            elif "'" not in action[1][0]:
                sb_actions.append(
                    "self.%s('%s', \"%s\", \"%s\")"
                    % (method, action[1][0], action[1][1], action[1][2])
                )
            else:
                sb_actions.append(
                    'self.%s("""%s""", "%s", "%s")'
                    % (method, action[1][0], action[1][1], action[1][2])
                )
        elif action[0] == "acc_a":
            sb_actions.append("self.accept_alert()")
        elif action[0] == "dis_a":
            sb_actions.append("self.dismiss_alert()")
        elif action[0] == "hi_li":
            method = "highlight"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "as_lt":
            method = "assert_link_text"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "as_ti":
            method = "assert_title"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "as_tc":
            method = "assert_title_contains"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "a_url":
            method = "assert_url"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "a_u_c":
            method = "assert_url_contains"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "as_df":
            method = "assert_downloaded_file"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "do_fi":
            method = "download_file"
            file_url = action[1][0]
            dest = action[1][1]
            if not dest:
                sb_actions.append('self.%s("%s")' % (method, file_url))
            else:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, file_url, dest)
                )
        elif action[0] == "as_at":
            method = "assert_attribute"
            if ('"' not in action[1][0]) and action[1][2]:
                sb_actions.append(
                    'self.%s("%s", "%s", "%s")'
                    % (method, action[1][0], action[1][1], action[1][2])
                )
            elif ('"' not in action[1][0]) and not action[1][2]:
                sb_actions.append(
                    'self.%s("%s", "%s")'
                    % (method, action[1][0], action[1][1])
                )
            elif ('"' in action[1][0]) and action[1][2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s", "%s")'
                    % (method, action[1][0], action[1][1], action[1][2])
                )
            else:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1][0], action[1][1])
                )
        elif (
            action[0] == "as_te"
            or action[0] == "as_et"
            or action[0] == "astnv"
            or action[0] == "aetnv"
            or action[0] == "da_te"
            or action[0] == "da_et"
        ):
            import unicodedata

            action[1][0] = unicodedata.normalize("NFKC", action[1][0])
            action[1][0] = action[1][0].replace("\n", "\\n")
            action[1][0] = action[1][0].replace("\u00B6", "")
            method = "assert_text"
            if action[0] == "as_et":
                method = "assert_exact_text"
            elif action[0] == "astnv":
                method = "assert_text_not_visible"
            elif action[0] == "aetnv":
                method = "assert_exact_text_not_visible"
            elif action[0] == "da_te":
                method = "deferred_assert_text"
            elif action[0] == "da_et":
                method = "deferred_assert_exact_text"
            if action[1][1] != "html":
                if '"' not in action[1][0] and '"' not in action[1][1]:
                    sb_actions.append(
                        'self.%s("%s", "%s")'
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' not in action[1][0] and '"' in action[1][1]:
                    sb_actions.append(
                        'self.%s("%s", \'%s\')'
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' in action[1] and '"' not in action[1][1]:
                    sb_actions.append(
                        'self.%s(\'%s\', "%s")'
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' in action[1] and '"' in action[1][1]:
                    sb_actions.append(
                        "self.%s('%s', '%s')"
                        % (method, action[1][0], action[1][1])
                    )
            else:
                if '"' not in action[1][0]:
                    sb_actions.append(
                        'self.%s("%s")' % (method, action[1][0])
                    )
                else:
                    sb_actions.append(
                        "self.%s('%s')" % (method, action[1][0])
                    )
        elif action[0] == "asnet":
            method = "assert_non_empty_text"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "da_el":
            method = "deferred_assert_element"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "da_ep":
            method = "deferred_assert_element_present"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "danet":
            method = "deferred_assert_non_empty_text"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
            else:
                sb_actions.append(
                    'self.%s("""%s""")' % (method, action[1])
                )
        elif action[0] == "s_scr":
            method = "save_screenshot"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
        elif action[0] == "ss_tf":
            method = "save_screenshot"
            action[2] = action[1][1]
            action[1] = action[1][0]
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s("%s", "%s")' % (method, action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'self.%s("%s", \'%s\')'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'self.%s(\'%s\', "%s")'
                    % (method, action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "self.%s('%s', '%s')" % (method, action[1], action[2])
                )
        elif action[0] == "ss_tl":
            method = "save_screenshot_to_logs"
            sb_actions.append("self.%s()" % method)
        elif action[0] == "sh_fc":
            method = "show_file_choosers"
            sb_actions.append("self.%s()" % method)
        elif action[0] == "pr_da":
            sb_actions.append("self.process_deferred_asserts()")
        elif action[0] == "a_d_m":
            sb_actions.append("self.activate_demo_mode()")
        elif action[0] == "d_d_m":
            sb_actions.append("self.deactivate_demo_mode()")
        elif action[0] == "c_l_s":
            sb_actions.append("self.clear_local_storage()")
        elif action[0] == "c_s_s":
            sb_actions.append("self.clear_session_storage()")
        elif action[0] == "d_a_c":
            sb_actions.append("self.delete_all_cookies()")
        elif action[0] == "go_bk":
            sb_actions.append("self.go_back()")
        elif action[0] == "go_fw":
            sb_actions.append("self.go_forward()")
        elif action[0] == "c_box":
            method = "check_if_unchecked"
            if action[2] == "no":
                method = "uncheck_if_checked"
            if '"' not in action[1]:
                sb_actions.append('self.%s("%s")' % (method, action[1]))
            else:
                sb_actions.append("self.%s('%s')" % (method, action[1]))
    return sb_actions
