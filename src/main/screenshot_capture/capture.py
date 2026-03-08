"""Screenshot capture utilities using Selenium + Chrome."""

from __future__ import annotations

from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def capture_screenshot(url: str, output_path: str) -> str:
    """Capture a full-page screenshot of ``url`` and save it to ``output_path``."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        # Allow the page to finish rendering before measuring dimensions.
        sleep(2)

        full_width = driver.execute_script(
            "return Math.max(document.body.scrollWidth,"
            "document.documentElement.scrollWidth);"
        )
        full_height = driver.execute_script(
            "return Math.max(document.body.scrollHeight,"
            "document.documentElement.scrollHeight);"
        )
        driver.set_window_size(int(full_width), int(full_height))
        sleep(1)

        driver.save_screenshot(str(destination))
        return str(destination)
    finally:
        # Always close the browser and release resources.
        driver.quit()
