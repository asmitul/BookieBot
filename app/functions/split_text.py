import re


def split_text(text):
    result = re.split(r'[,\s，]+', text)

    return result