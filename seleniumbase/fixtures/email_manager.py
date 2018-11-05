"""
EmailManager - a helper class to login, search for, and delete emails.
"""

import email
import htmlentitydefs
import imaplib
import quopri
import re
import time
import types
from seleniumbase.config import settings


class EmailManager:
    """ A helper class to interface with an Email account. These imap methods
    can search for and fetch messages without needing a browser.

    Example:

    em = EmailManager()
    result = em.check_for_recipient(
        "[GMAIL.USER]+[SOME CODE OR TIMESTAMP KEY]@gmail.com")
    """

    HTML = "text/html"
    PLAIN = "text/plain"
    TIMEOUT = 1800

    def __init__(self, uname=settings.EMAIL_USERNAME,
                 pwd=settings.EMAIL_PASSWORD,
                 imap_string=settings.EMAIL_IMAP_STRING,
                 port=settings.EMAIL_IMAP_PORT):
        self.uname = uname
        self.pwd = pwd
        self.imap_string = imap_string
        self.port = port

    def imap_connect(self):
        """
        Connect to the IMAP mailbox.
        """
        self.mailbox = imaplib.IMAP4_SSL(self.imap_string, self.port)
        self.mailbox.login(self.uname, self.pwd)
        self.mailbox.select()

    def imap_disconnect(self):
        """
        Disconnect from the IMAP mailbox.
        """
        self.mailbox.close()
        self.mailbox.logout()

    def __imap_search(self, ** criteria_dict):
        """ Searches for query in the given IMAP criteria and returns
        the message numbers that match as a list of strings.

        Criteria without values (eg DELETED) should be keyword args
        with KEY=True, or else not passed. Criteria with values should
        be keyword args of the form KEY="VALUE" where KEY is a valid
        IMAP key.

        IMAP default is to AND all criteria together. We don't support
        other logic quite yet.

        All valid keys: ALL, ANSWERED, BCC <string>, BEFORE <string>,
        BODY <string>, CC <string>, DELETED, DRAFT, FLAGGED, FROM
        <string>, HEADER <field-name> <string> (UNTESTED), KEYWORD
        <flag>, LARGER <n>, NEW, NOT <search-key>, OLD, ON <date>,
        OR <search-key1> <search-key2> (UNTESTED), RECENT, SEEN,
        SENTBEFORE <date>, SENTON <date>, SENTSINCE <date>, SINCE <date>,
        SMALLER <n>, SUBJECT <string>, TEXT <string>, TO <string>,
        UID <sequence set>, UNANSWERED, UNDELETED, UNDRAFT, UNFLAGGED,
        UNKEYWORD <flag>, UNSEEN.

        For details on keys and their values, see
        http://tools.ietf.org/html/rfc3501#section-6.4.4

        :param criteria_dict: dictionary of search criteria keywords
        :raises: EmailException if something in IMAP breaks
        :returns: List of message numbers as strings matched by given criteria
        """
        self.imap_connect()

        criteria = []
        for key in criteria_dict:
            if criteria_dict[key] is True:
                criteria.append('(%s)' % key)
            else:
                criteria.append('(%s "%s")' % (key, criteria_dict[key]))

        # If any of these criteria are not valid IMAP keys, IMAP will tell us.
        status, msg_nums = self.mailbox.search('UTF-8', * criteria)
        self.imap_disconnect()

        if 0 == len(msg_nums):
            msg_nums = []

        if 'OK' in status:
            return self.__parse_imap_search_result(msg_nums)
        else:
            raise EmailException("IMAP status is " + str(status))

    def remove_formatting(self, html):
        """
        Clean out any whitespace
        @Params
        html - String of html to remove whitespace from
        @Returns
        Cleaned string
        """
        return ' '.join(html.split())

    def __parse_imap_search_result(self, result):
        """
        This takes the result of imap_search and returns SANE results
        @Params
        result - result from an imap_search call
        @Returns
        List of IMAP search results
        """
        if isinstance(result, types.ListType):
            # Above is same as "type(result) == types.ListType"
            if len(result) == 1:
                return self.__parse_imap_search_result(result[0])
            else:
                return result
        elif isinstance(result, types.StringType):
            # Above is same as "type(result) == types.StringType"
            return result.split()
        else:
            # Fail silently assuming tests will fail if emails are not found
            return []

    def fetch_html(self, msg_nums):
        """
        Given a message number that we found with imap_search,
        get the text/html content.
        @Params
        msg_nums - message number to get html message for
        @Returns
        HTML content of message matched by message number
        """
        if not msg_nums:
            raise Exception("Invalid Message Number!")

        return self.__imap_fetch_content_type(msg_nums, self.HTML)

    def fetch_plaintext(self, msg_nums):
        """
        Given a message number that we found with imap_search,
        get the text/plain content.
        @Params
        msg_nums - message number to get message for
        @Returns
        Plaintext content of message matched by message number
        """
        if not msg_nums:
            raise Exception("Invalid Message Number!")

        return self.__imap_fetch_content_type(msg_nums, self.PLAIN)

    def __imap_fetch_content_type(self, msg_nums, content_type):
        """
        Given a message number that we found with imap_search, fetch the
        whole source, dump that into an email object, and pick out the part
        that matches the content type specified. Return that, if we got
        multiple emails, return dict of all the parts.
        @Params
        msg_nums - message number to search for
        content_type - content type of email message to return
        @Returns
        Specified content type string or dict of all content types of matched
        email.
        """

        if not msg_nums:
            raise Exception("Invalid Message Number!")
        if not content_type:
            raise Exception("Need a content type!")

        contents = {}
        self.imap_connect()
        for num in msg_nums:
            status, data = self.mailbox.fetch(num, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    for part in msg.walk():
                        if str(part.get_content_type()) == content_type:
                            content = str(part.get_payload(decode=True))
                            contents[int(num)] = content
        self.imap_disconnect()
        return contents

    def fetch_html_by_subject(self, email_name):
        """
        Get the html of an email, searching by subject.
        @Params
        email_name - the subject to search for
        @Returns
        HTML content of the matched email
        """
        if not email_name:
            raise EmailException("Subject cannot be null")

        results = self.__imap_search(SUBJECT=email_name)
        sources = self.fetch_html(results)

        return sources

    def fetch_plaintext_by_subject(self, email_name):
        """
        Get the plain text of an email, searching by subject.
        @Params
        email_name - the subject to search for
        @Returns
        Plaintext content of the matched email
        """
        if not email_name:
            raise EmailException("Subject cannot be null")

        results = self.__imap_search(SUBJECT=email_name)
        sources = self.fetch_plaintext(results)

        return sources

    def search_for_recipient(self, email, timeout=None, content_type=None):
        """
        Get content of emails, sent to a specific email address.
        @Params
        email - the recipient email address to search for
        timeout - seconds to try beore timing out
        content_type - type of email string to return
        @Returns
        Content of the matched email in the given content type
        """
        return self.search(timeout=timeout,
                           content_type=content_type, TO=email)

    def search_for_subject(self, subject, timeout=None, content_type=None):
        """
        Get content of emails, sent to a specific email address.
        @Params
        email - the recipient email address to search for
        timeout - seconds to try beore timing out
        content_type - type of email string to return
        @Returns
        Content of the matched email in the given content type
        """
        return self.search(timeout=timeout,
                           content_type=content_type, SUBJECT=subject)

    def search_for_count(self, ** args):
        """
        A search that keeps searching up until timeout for a
        specific number of matches to a search. If timeout is not
        specified we use the default.  If count= is not specified we
        will fail. Return values are the same as search(), except for count=0,
        where we will return an empty list. Use this if you need to wait for a
        number of emails other than 1.

        @Params
        args - dict of arguments to use in search:
               count - number of emails to search for
               timeout - seconds to try search before timing out
        @Returns
        List of message numbers matched by search
        """
        if "timeout" not in args.keys():
            timeout = self.TIMEOUT
        elif args["timeout"]:
            timeout = args["timeout"]
        args["timeout"] = timeout / 15

        if "count" not in args.keys():
            raise EmailException("Count param not defined!")
        else:
            count = int(args["count"])
            del args["count"]

        results = None
        timer = timeout
        count = 0
        while count < timer:
            try:
                results = self.search(** args)
            except EmailException:
                if count == 0:
                    return []

            if results and len(results) == count:
                return results
            else:
                time.sleep(15)
                count += 15
        if count >= timer:
            raise EmailException("Failed to match criteria %s in %s minutes" %
                                 (args, timeout / 60))

    def __check_msg_for_headers(self, msg, ** email_headers):
        """
        Checks an Email.Message object for the headers in email_headers.

        Following are acceptable header names: ['Delivered-To',
            'Received', 'Return-Path', 'Received-SPF',
            'Authentication-Results', 'DKIM-Signature',
            'DomainKey-Signature', 'From', 'To', 'Message-ID',
            'Subject', 'MIME-Version', 'Content-Type', 'Date',
            'X-Sendgrid-EID', 'Sender'].

        @Params
        msg - the Email.message object to check
        email_headers - list of headers to check against
        @Returns
        Boolean whether all the headers were found
        """
        all_headers_found = False
        email_headers['Delivered-To'] = email_headers['To']
        email_headers.pop('To')
        all_headers_found = all(k in msg.keys() for k in email_headers)

        return all_headers_found

    def fetch_message(self, msgnum):
        """
        Given a message number, return the Email.Message object.
        @Params
        msgnum - message number to find
        @Returns
        Email.Message object for the given message number
        """
        self.imap_connect()
        status, data = self.mailbox.fetch(msgnum, "(RFC822)")
        self.imap_disconnect()

        for response_part in data:
            if isinstance(response_part, tuple):
                return email.message_from_string(response_part[1])

    def get_content_type(self, msg, content_type="HTML"):
        """
        Given an Email.Message object, gets the content-type payload
        as specified by @content_type. This is the actual body of the
        email.
        @Params
        msg - Email.Message object to get message content for
        content_type - Type of content to get from the email
        @Return
        String content of the email in the given type
        """
        if "HTML" in content_type.upper():
            content_type = self.HTML
        elif "PLAIN" in content_type.upper():
            content_type = self.PLAIN

        for part in msg.walk():
            if str(part.get_content_type()) == content_type:
                return str(part.get_payload(decode=True))

    def search(self, ** args):
        """
        Checks email inbox every 15 seconds that match the criteria
        up until timeout.

        Search criteria should be keyword args eg
        TO="selenium@gmail.com".  See __imap_search docstring for list
        of valid criteria. If content_type is not defined, will return
        a list of msg numbers.

        Options:
        - fetch: will return a dict of Message objects, keyed on msgnum,
          which can be used to look at headers and other parts of the complete
          message.  (http://docs.python.org/library/email.message.html)
        - timeout: will replace the default module timeout with the
          value in SECONDS.
        - content_type: should be either "PLAIN" or
          "HTML". If defined returns the source of the matched messages
          as a dict of msgnum:content. If not defined we return a list
          of msg nums.
        """

        if "content_type" not in args.keys():
            content_type = None
        elif "HTML" in args["content_type"]:
            content_type = self.HTML
            del args["content_type"]
        elif "PLAIN" in args["content_type"]:
            content_type = self.PLAIN
            del args["content_type"]
        elif args["content_type"]:
            content_type = args['content_type']
            del args["content_type"]

        if "timeout" not in args.keys():
            timeout = self.TIMEOUT
        elif "timeout" in args:
            timeout = args["timeout"]
            del args["timeout"]

        fetch = False
        if "fetch" in args.keys():
            fetch = True
            del args["fetch"]

        results = None
        timer = timeout
        count = 0
        while count < timer:
            results = self.__imap_search(** args)
            if len(results) > 0:
                if fetch:
                    msgs = {}
                    for msgnum in results:
                        msgs[msgnum] = self.fetch_message(msgnum)
                    return msgs
                elif not content_type:
                    return results
                else:
                    return self.__imap_fetch_content_type(results,
                                                          content_type)
            else:
                time.sleep(15)
                count += 15
        if count >= timer:
            raise EmailException(
                "Failed to find message for criteria %s in %s minutes" %
                (args, timeout / 60))

    def remove_whitespace(self, html):
        """
        Clean whitespace from html
        @Params
        html - html source to remove whitespace from
        @Returns
        String html without whitespace
        """
        # Does python have a better way to do exactly this?
        clean_html = html
        for char in ("\r", "\n", "\t"):
            clean_html = clean_html.replace(char, "")
        return clean_html

    def remove_control_chars(self, html):
        """
        Clean control characters from html
        @Params
        html - html source to remove control characters from
        @Returns
        String html without control characters
        """
        return self.remove_whitespace(html)

    def replace_entities(self, html):
        """
        Replace htmlentities with unicode characters
        @Params
        html - html source to replace entities in
        @Returns
        String html with entities replaced
        """
        def fixup(text):
            """replace the htmlentities in some text"""
            text = text.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text  # leave as is
        return re.sub(r"&#?\w+;", fixup, html)

    def decode_quoted_printable(self, html):
        """
        Decoding from Quoted-printable, or QP encoding, that uses ASCII 7bit
        chars to encode 8 bit chars, resulting in =3D to represent '='. Python
        supports UTF-8 so we decode. Also removes line breaks with '= at the
        end.'
        @Params
        html - html source to decode
        @Returns
        String decoded HTML source
        """
        return self.replace_entities(quopri.decodestring(html))

    def html_bleach(self, html):
        """
        Cleanup and get rid of all extraneous stuff for better comparison
        later. Turns formatted into into a single line string.
        @Params
        html - HTML source to clean up
        @Returns
        String cleaned up HTML source
        """
        return self.decode_quoted_printable(html)


class EmailException(Exception):
    """Raised when we have an Email-related problem."""
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
