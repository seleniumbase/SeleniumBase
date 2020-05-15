# -\*- coding: utf-8 -\*-

''' This is mainly for string obfuscation. '''

import base64
import codecs
import hashlib
from seleniumbase.config import settings


def str_xor(string, key):
    if len(key) < 1:
        raise Exception("2nd arg of str_xor() must be a string of length > 0!")
    if len(string) > len(key):
        difference = len(string) - len(key)
        key = key + (
            ((difference / len(key)) * key) + key)
    result = None
    try:
        result = "".join(
            [chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(string, key)])
    except Exception:
        string = string.decode('utf-8')
        result = "".join(
            [chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(string, key)])
    return result


def is_obfuscated(string):
    # Based on settings, determines if a string has already been obfuscated.
    # Obfuscated strings have a common predefined start token and end token.
    start_token = settings.OBFUSCATION_START_TOKEN
    end_token = settings.OBFUSCATION_END_TOKEN
    return (string.startswith(start_token) and string.endswith(end_token))


def shuffle_string(string):
    if len(string) < 2:
        return string
    return (string[1::2] + string[::2])


def reverse_shuffle_string(string):
    if len(string) < 2:
        return string
    new_string = ""
    odd = (len(string) % 2 == 1)
    part1 = string[:int(len(string) / 2):1]
    part2 = string[int(len(string) / 2)::1]
    for c in range(len(part1)):
        new_string += part2[c]
        new_string += part1[c]
    if odd:
        new_string += part2[-1]
    return new_string


def blend_strings(string1, string2):
    smallest_length = min(len(string1), len(string2))
    new_string = ""
    for c in range(smallest_length):
        new_string += string1[c]
        new_string += string2[c]
    if len(string1) > len(string2):
        new_string += string1[smallest_length:]
    elif len(string2) > len(string1):
        new_string += string2[smallest_length:]
    else:
        # Equal length strings
        pass
    return new_string


def rotate(string, n):
    return string[n:] + string[:n]


def ord_string_sum(string):
    count = 0
    try:
        for c in string:
            count += ord(c)
    except Exception:
        string = string.decode('utf-8')
        for c in string:
            count += ord(c)
    return count


def decrypt(string):
    # Password/String obfuscation/de-obfuscation
    # Used for both encryption and decryption
    # If you update the algorithm, you must re-encrypt all encrypted passwords!
    encryption_key = settings.ENCRYPTION_KEY
    start_token = settings.OBFUSCATION_START_TOKEN
    end_token = settings.OBFUSCATION_END_TOKEN
    already_encrypted = False
    if is_obfuscated(string):
        already_encrypted = True
        string = string[len(start_token):-len(end_token)]
        string = base64.b64decode(codecs.encode(string))
    # Obfuscate the key used for string obfuscation
    hd1 = hashlib.sha256(str(encryption_key).encode('utf-8')).hexdigest()
    hd2 = hashlib.sha256(str(encryption_key[::-1]).encode('utf-8')).hexdigest()
    b64_key = base64.b64encode(codecs.encode(encryption_key * 8))
    xor_key = "".join([chr(ord(str(c3)) - int(c1, 16) - int(c2, 16)) for (
        c1, c2, c3) in zip(hd1, hd2, b64_key.decode("utf-8"))])
    xor_key = blend_strings(xor_key, encryption_key)
    if len(xor_key) % 7 == 0:
        xor_key = xor_key + encryption_key[-1]
    xor_key = shuffle_string((xor_key * 8)[::7])
    # Use the str_xor method for the main string obfuscation / de-obfuscation
    if not already_encrypted:
        if len(string) > 0:
            rem1 = (ord_string_sum(string)) % 3
            rem2 = (ord_string_sum(string)) % 4
            rem3 = (ord_string_sum(string)) % 2
            rem4 = (len(string) + ord_string_sum(string)) % 2
        if len(string) % 2 != 0:
            if rem3 == 1:
                string = (chr(ord(string[-1]) - 5 - rem1) + string + ''
                          '' + chr(ord(string[-1]) - 13 - rem1))
            else:
                string = (chr(ord(string[-1]) - 11 - rem1) + string + ''
                          '' + chr(ord(string[-1]) - 23 - rem1))
        elif len(string) > 1:
            if rem4 == 1:
                string = (chr(ord(string[0]) - 19 + rem2) + string + ''
                          '' + chr(ord(string[0]) - 7 - rem2))
            else:
                string = (chr(ord(string[0]) - 26 + rem2) + string + ''
                          '' + chr(ord(string[0]) - 12 - rem2))
        rem5 = (len(string) + ord_string_sum(string)) % 23
        string = rotate(string, rem5)
        result = str_xor(shuffle_string(string)[::-1], xor_key)
        rem6 = (len(result) + ord_string_sum(result)) % 17
        result = rotate(result, rem6)
    else:
        rem6 = (len(string) + ord_string_sum(string)) % 17
        string = rotate(string, -rem6)
        result = reverse_shuffle_string(str_xor(string, xor_key)[::-1])
        if len(result) > 2:
            rem5 = (len(result) + ord_string_sum(result)) % 23
            result = rotate(result, -rem5)
            result = result[1:-1]
    # Finalize encryption of non-encrypted string
    if not already_encrypted:
        result = base64.b64encode(codecs.encode(result))
        result = start_token + result.decode("utf-8") + end_token
    return result
