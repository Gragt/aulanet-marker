"""A script that inputs marks on AulaNet from an Excel file source."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class AulaNetSession:
    """The browser session and functions."""

    def __init__(self):
        """Open session by opening the web browser, identifying as Chrome."""
        options = Options()
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        )
        self.browser = webdriver.Firefox(options=options)
        self.browser.get("https://erp.aulanet.com.mx")

    def browser_close(self):
        """Close sessions."""
        self.browser.close()


def aulanet_marker():
    """Open session and awaits input to parse and copy marks."""
    print("Opening web browser …")
    session = AulaNetSession()
    print("Please manually log into AulaNet.")
    input("Press Enter when ready to continue.")
    session.browser_close()


# aulanet_marker()
