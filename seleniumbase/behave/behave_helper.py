"""Generating Gherkin-formatted code from the Recorder."""


def generate_gherkin(srt_actions):
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
                sb_actions.append('Open "%s"' % action[2])
            elif "'" not in action[2]:
                sb_actions.append("Open '%s'" % action[2])
            else:
                sb_actions.append('Open "%s"' % action[2].replace('"', '\\"'))
        elif action[0] == "f_url":
            if "%" in action[2]:
                try:
                    from urllib.parse import unquote

                    action[2] = unquote(action[2], errors="strict")
                except Exception:
                    pass
            if '"' not in action[2]:
                sb_actions.append('Open if not "%s"' % action[2])
            elif "'" not in action[2]:
                sb_actions.append("Open if not '%s'" % action[2])
            else:
                sb_actions.append(
                    'Open if not "%s"' % action[2].replace('"', '\\"')
                )
        elif action[0] == "click":
            if '"' not in action[1]:
                sb_actions.append('Click "%s"' % action[1])
            else:
                sb_actions.append("Click '%s'" % action[1])
        elif action[0] == "dbclk":
            if '"' not in action[1]:
                sb_actions.append('Double click "%s"' % action[1])
            else:
                sb_actions.append("Double click '%s'" % action[1])
        elif action[0] == "js_cl":
            if '"' not in action[1]:
                sb_actions.append('JS click "%s"' % action[1])
            else:
                sb_actions.append("JS click '%s'" % action[1])
        elif action[0] == "js_ca":
            if '"' not in action[1]:
                sb_actions.append('JS click all "%s"' % action[1])
            else:
                sb_actions.append("JS click all '%s'" % action[1])
        elif action[0] == "jq_cl":
            if '"' not in action[1]:
                sb_actions.append('jQuery click "%s"' % action[1])
            else:
                sb_actions.append("jQuery click '%s'" % action[1])
        elif action[0] == "jq_ca":
            if '"' not in action[1]:
                sb_actions.append('jQuery click all "%s"' % action[1])
            else:
                sb_actions.append("jQuery click all '%s'" % action[1])
        elif action[0] == "r_clk":
            if '"' not in action[1]:
                sb_actions.append('Context click "%s"' % action[1])
            else:
                sb_actions.append("Context click '%s'" % action[1])
        elif action[0] == "canva":
            selector = action[1][0]
            p_x = action[1][1]
            p_y = action[1][2]
            if '"' not in selector:
                sb_actions.append(
                    'Click "%s" at (%s, %s)' % (selector, p_x, p_y)
                )
            else:
                sb_actions.append(
                    "Click '%s' at (%s, %s)" % (selector, p_x, p_y)
                )
        elif action[0] == "input":
            text = action[2].replace("\n", "\\n")
            if '"' not in text and '"' not in action[1]:
                sb_actions.append('Type "%s" into "%s"' % (text, action[1]))
            elif '"' in text and '"' not in action[1]:
                sb_actions.append('Type \'%s\' into "%s"' % (text, action[1]))
            elif '"' not in text and '"' in action[1]:
                sb_actions.append('Type "%s" into \'%s\'' % (text, action[1]))
            elif '"' in text and '"' in action[1]:
                sb_actions.append("Type '%s' into '%s'" % (text, action[1]))
        elif action[0] == "js_ty":
            text = action[2].replace("\n", "\\n")
            if '"' not in text and '"' not in action[1]:
                sb_actions.append('JS type "%s" in "%s"' % (text, action[1]))
            elif '"' in text and '"' not in action[1]:
                sb_actions.append('JS type \'%s\' in "%s"' % (text, action[1]))
            elif '"' not in text and '"' in action[1]:
                sb_actions.append('JS type "%s" in \'%s\'' % (text, action[1]))
            elif '"' in text and '"' in action[1]:
                sb_actions.append("JS type '%s' in '%s'" % (text, action[1]))
        elif action[0] == "jq_ty":
            text = action[2].replace("\n", "\\n")
            if '"' not in text and '"' not in action[1]:
                sb_actions.append(
                    'jQuery type "%s" in "%s"' % (text, action[1])
                )
            elif '"' in text and '"' not in action[1]:
                sb_actions.append(
                    'jQuery type \'%s\' in "%s"' % (text, action[1])
                )
            elif '"' not in text and '"' in action[1]:
                sb_actions.append(
                    'jQuery type "%s" in \'%s\'' % (text, action[1])
                )
            elif '"' in text and '"' in action[1]:
                sb_actions.append(
                    "jQuery type '%s' in '%s'" % (text, action[1])
                )
        elif action[0] == "pkeys":
            text = action[2].replace("\n", "\\n")
            if '"' not in text and '"' not in action[1]:
                sb_actions.append(
                    'Press keys "%s" in "%s"' % (text, action[1])
                )
            elif '"' in text and '"' not in action[1]:
                sb_actions.append(
                    'Press keys \'%s\' in "%s"' % (text, action[1])
                )
            elif '"' not in text and '"' in action[1]:
                sb_actions.append(
                    'Press keys "%s" in \'%s\'' % (text, action[1])
                )
            elif '"' in text and '"' in action[1]:
                sb_actions.append(
                    "Press keys '%s' in '%s'" % (text, action[1])
                )
        elif action[0] == "hover":
            if '"' not in action[1]:
                sb_actions.append('Hover "%s"' % action[1])
            else:
                sb_actions.append("Hover '%s'" % action[1])
        elif action[0] == "e_mfa":
            text = action[2].replace("\n", "\\n")
            if '"' not in action[1] and '"' not in text:
                sb_actions.append('Into "%s" do MFA "%s"' % (action[1], text))
            elif '"' not in action[1] and '"' in text:
                sb_actions.append(
                    'Into "%s" do MFA \'%s\'' % (action[1], text)
                )
            elif '"' in action[1] and '"' not in text:
                sb_actions.append(
                    'Into \'%s\' do MFA "%s"' % (action[1], text)
                )
            elif '"' in action[1] and '"' in text:
                sb_actions.append("Into '%s' do MFA '%s'" % (action[1], text))
        elif action[0] == "h_clk":
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Hover "%s" and click "%s"' % (action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'Hover "%s" and click \'%s\'' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Hover \'%s\' and click "%s"' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "Hover '%s' and click '%s'" % (action[1], action[2])
                )
        elif action[0] == "ddrop":
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Drag "%s" into "%s"' % (action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'Drag "%s" into \'%s\'' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Drag \'%s\' into "%s"' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "Drag '%s' into '%s'" % (action[1], action[2])
                )
        elif action[0] == "s_opt":
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Find "%s" and select "%s"' % (action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'Find "%s" and select \'%s\'' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Find \'%s\' and select "%s"' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "Find '%s' and select '%s'" % (action[1], action[2])
                )
        elif action[0] == "set_v":
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Set value of "%s" to "%s"' % (action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'Set value of "%s" to \'%s\'' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Set value of \'%s\' to "%s"' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "Set value of '%s' to '%s'" % (action[1], action[2])
                )
        elif action[0] == "cho_f":
            action[2] = action[2].replace("\\", "\\\\")
            if '"' not in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Into "%s" choose file "%s"' % (action[1], action[2])
                )
            elif '"' not in action[1] and '"' in action[2]:
                sb_actions.append(
                    'Into "%s" choose file \'%s\'' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' not in action[2]:
                sb_actions.append(
                    'Into \'%s\' choose file "%s"' % (action[1], action[2])
                )
            elif '"' in action[1] and '"' in action[2]:
                sb_actions.append(
                    "Into '%s' choose file '%s'" % (action[1], action[2])
                )
        elif action[0] == "sw_fr":
            method = "Switch to frame"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "sw_dc":
            sb_actions.append("Switch to default content")
        elif action[0] == "sw_pf":
            sb_actions.append("Switch to parent frame")
        elif action[0] == "s_c_f":
            method = "Set content to frame"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "s_c_d":
            nested = action[1]
            if nested:
                sb_actions.append("Set content to parent")
            else:
                sb_actions.append("Set content to default")
        elif action[0] == "sleep":
            sb_actions.append("Sleep for %s seconds" % action[1])
        elif action[0] == "wf_el":
            method = "Wait for element"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "as_el":
            method = "Assert element"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "as_ep":
            method = "Assert element present"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "asenv":
            method = "Assert element not visible"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "s_at_" or action[0] == "s_ats":
            start = "Find"
            if action[0] == "s_ats":
                start = "Find all"
            if '"' not in action[1][0]:
                sb_actions.append(
                    '%s "%s" and set %s to "%s"'
                    % (start, action[1][0], action[1][1], action[1][2])
                )
            elif "'" not in action[1][0]:
                sb_actions.append(
                    "%s '%s' and set %s to \"%s\""
                    % (start, action[1][0], action[1][1], action[1][2])
                )
            else:
                sb_actions.append(
                    '%s "%s" and set %s to "%s")'
                    % (
                        start.replace('"', '\\"'),
                        action[1][0], action[1][1], action[1][2]
                    )
                )
        elif action[0] == "acc_a":
            sb_actions.append("Accept alert")
        elif action[0] == "dis_a":
            sb_actions.append("Dismiss alert")
        elif action[0] == "hi_li":
            method = "Highlight"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "as_lt":
            method = "Assert link text"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "as_ti":
            method = "Assert title"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "as_tc":
            method = "Assert title contains"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "a_url":
            method = "Assert URL"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "a_u_c":
            method = "Assert URL contains"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "as_df":
            method = "Assert downloaded file"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "do_fi":
            method = "Download file"
            file_url = action[1][0]
            dest = action[1][1]
            if not dest:
                sb_actions.append('%s "%s" to downloads' % (method, file_url))
            else:
                sb_actions.append('%s "%s" to "%s"' % (method, file_url, dest))
        elif action[0] == "as_at":
            if ('"' not in action[1][0]) and action[1][2]:
                sb_actions.append(
                    'In "%s" assert attribute/value "%s"/"%s"'
                    % (action[1][0], action[1][1], action[1][2])
                )
            elif ('"' not in action[1][0]) and not action[1][2]:
                sb_actions.append(
                    'In "%s" assert attribute "%s"'
                    % (action[1][0], action[1][1])
                )
            elif ('"' in action[1][0]) and action[1][2]:
                sb_actions.append(
                    'In \'%s\' assert attribute/value "%s"/"%s"'
                    % (action[1][0], action[1][1], action[1][2])
                )
            else:
                sb_actions.append(
                    'In \'%s\' assert attribute "%s"'
                    % (action[1][0], action[1][1])
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
            method = "Assert text"
            if action[0] == "as_et":
                method = "Assert exact text"
            elif action[0] == "astnv":
                method = "Assert text not visible"
            elif action[0] == "aetnv":
                method = "Assert exact text not visible"
            elif action[0] == "da_te":
                method = "Deferred assert text"
            elif action[0] == "da_et":
                method = "Deferred assert exact text"
            if action[1][1] != "html":
                if '"' not in action[1][0] and '"' not in action[1][1]:
                    sb_actions.append(
                        '%s "%s" in "%s"'
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' not in action[1][0] and '"' in action[1][1]:
                    sb_actions.append(
                        '%s "%s" in \'%s\''
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' in action[1] and '"' not in action[1][1]:
                    sb_actions.append(
                        '%s \'%s\' in "%s"'
                        % (method, action[1][0], action[1][1])
                    )
                elif '"' in action[1] and '"' in action[1][1]:
                    sb_actions.append(
                        "%s '%s' in '%s'"
                        % (method, action[1][0], action[1][1])
                    )
            else:
                if '"' not in action[1][0]:
                    sb_actions.append('%s "%s"' % (method, action[1][0]))
                else:
                    sb_actions.append("%s '%s'" % (method, action[1][0]))
        elif action[0] == "asnet":
            method = "Assert non-empty text in"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "da_el":
            method = "Deferred assert element"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "da_ep":
            method = "Deferred assert element present"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "danet":
            method = "Deferred assert non-empty text in"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            elif "'" not in action[1]:
                sb_actions.append("%s '%s'" % (method, action[1]))
            else:
                sb_actions.append(
                    "%s '%s'" % (method, action[1].replace("'", "\\'"))
                )
        elif action[0] == "s_scr":
            method = "Save screenshot as"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
        elif action[0] == "ss_tf":
            if '"' not in action[2] and '"' not in action[1]:
                sb_actions.append(
                    'Save screenshot to "%s" as "%s"'
                    % (action[2], action[1])
                )
            elif '"' not in action[2] and '"' in action[1]:
                sb_actions.append(
                    'Save screenshot to "%s" as \'%s\''
                    % (action[2], action[1])
                )
            elif '"' in action[2] and '"' not in action[1]:
                sb_actions.append(
                    'Save screenshot to \'%s\' as "%s"'
                    % (action[2], action[1])
                )
            elif '"' in action[2] and '"' in action[1]:
                sb_actions.append(
                    "Save screenshot to '%s' as '%s'"
                    % (action[2], action[1])
                )
        elif action[0] == "ss_tl":
            sb_actions.append("Save screenshot to logs")
        elif action[0] == "sh_fc":
            sb_actions.append("Show file choosers")
        elif action[0] == "pr_da":
            sb_actions.append("Process deferred asserts")
        elif action[0] == "a_d_m":
            sb_actions.append("Activate Demo Mode")
        elif action[0] == "d_d_m":
            sb_actions.append("Deactivate Demo Mode")
        elif action[0] == "c_l_s":
            sb_actions.append("Clear Local Storage")
        elif action[0] == "c_s_s":
            sb_actions.append("Clear Session Storage")
        elif action[0] == "d_a_c":
            sb_actions.append("Delete all cookies")
        elif action[0] == "go_bk":
            sb_actions.append("Go back")
        elif action[0] == "go_fw":
            sb_actions.append("Go forward")
        elif action[0] == "c_box":
            method = "Check if unchecked"
            if action[2] == "no":
                method = "Uncheck if checked"
            if '"' not in action[1]:
                sb_actions.append('%s "%s"' % (method, action[1]))
            else:
                sb_actions.append("%s '%s'" % (method, action[1]))
    return sb_actions
