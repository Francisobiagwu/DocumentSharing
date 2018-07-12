"""
@author: Francis Obiagwu
@software: SecureDocumentSharing
@file: DSPrintStyle.py
@time: 7/11/18 5:59 PM
"""


class Color:
    """
    This class is used to color string
    """

    def __init__(self):
        self.CRED = '\033[91m'
        self.CEND = '\033[0m'
        self.CEND = '\33[0m'

        self.CBLACK = '\33[30m'
        self.CRED = '\33[31m'
        self.CGREEN = '\33[32m'
        self.CYELLOW = '\33[33m'
        self.CBLUE = '\33[34m'
        self.CVIOLET = '\33[35m'
        self.CBEIGE = '\33[36m'
        self.CWHITE = '\33[37m'

        self.CBLACKBG = '\33[40m'
        self.CREDBG = '\33[41m'
        self.CGREENBG = '\33[42m'
        self.CYELLOWBG = '\33[43m'
        self.CBLUEBG = '\33[44m'
        self.CVIOLETBG = '\33[45m'
        self.CBEIGEBG = '\33[46m'
        self.CWHITEBG = '\33[47m'

        self.CGREY = '\33[90m'
        self.CRED2 = '\33[91m'
        self.CGREEN2 = '\33[92m'
        self.CYELLOW2 = '\33[93m'
        self.CBLUE2 = '\33[94m'
        self.CVIOLET2 = '\33[95m'
        self.CBEIGE2 = '\33[96m'
        self.CWHITE2 = '\33[97m'

        self.CGREYBG = '\33[100m'
        self.CREDBG2 = '\33[101m'
        self.CGREENBG2 = '\33[102m'
        self.CYELLOWBG2 = '\33[103m'
        self.CBLUEBG2 = '\33[104m'
        self.CVIOLETBG2 = '\33[105m'
        self.CBEIGEBG2 = '\33[106m'
        self.CWHITEBG2 = '\33[107m'

    def red(self, text):
        """
        Used to return a red string
        :param text: String
        :return: red String
        """
        return self.CRED + text + self.CEND

    def green(self, text):
        """
        Used to return a green string
        :param text: String
        :return: green string
        """
        return self.CGREEN + text + self.CEND

    def white(self, text):
        """
        Used to return a white string
        :param text: String
        :return: white string
        """
        return self.CWHITE + text + self.CEND

    def yellow(self, text):
        """
        Used to return a yellow String
        :param text: String
        :return: yellow string
        """
        return self.CYELLOW + text + self.CEND

    def black(self, text):
        """
        Used to return a black string
        :param text: String
        :return: black String
        """
        return self.CBLACK + text + self.CEND

    def blue(self, text):
        """
        Used to return a blue string
        :param text: String
        :return: blue string
        """
        return self.CBLUE + text + self.CEND

    def biege(self, text):
        """
        Used to return a biege string
        :param text: String
        :return: biege string
        """
        return self.CBEIGE + text + self.CEND


class Style:
    """
    This class is used for styling string
    """

    def __init__(self):
        self.CBOLD = '\33[1m'
        self.CITALIC = '\33[3m'
        self.CURL = '\33[4m'
        self.CBLINK = '\33[5m'
        self.CBLINK2 = '\33[6m'
        self.CSELECTED = '\33[7m'
        self.CEND = '\33[0m'

    def selected(self, text):
        """
        Used to return a str as selected
        :param text: String
        :return: Selected string
        """
        return self.CSELECTED + text + self.CEND

    def blink(self, text):
        """
        Used to return blinking string
        :param text: String
        :return: blinking string
        """
        return self.CBLINK + text + self.CEND

    def bold(self, text):
        """
        Used to return bold string
        :param text: String
        :return: bold tring
        """
        return self.CBOLD + text + self.CEND

    def italic(self, text):
        """
        Used to return italics
        :param text: String
        :return: Italised string
        """
        return self.CITALIC + text + self.CEND


