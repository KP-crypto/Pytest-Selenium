import pytest
import os
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from decouple import config
from pathlib import Path


@pytest.fixture(scope='class')
def setup(browser):
    global driver
    if browser=="chrome" and config("Headless")=='False':
        driver = webdriver.Chrome(ChromeDriverManager().install())

    else:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


    driver.get(config('URL'))
    driver.maximize_window()

    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser")

@pytest.fixture(scope='class')
def browser(request):
    return request.config.getoption('--browser')

@pytest.fixture(scope='class')
def createDirectories():
    ROOT_DIR = Path(__file__).parent.parent
    results_dir = os.path.join(ROOT_DIR,"results")
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)



@pytest.fixture(scope='class')
def clear_results():
    ROOT_DIR = Path(__file__).parent.parent
    Results = os.path.join(ROOT_DIR, 'results').replace('\\', '/')

    if os.path.isdir(Results):
        file_list = os.listdir(Results)
        if len(file_list) != "":
            for filename in file_list:
                item = Results + "/" + filename
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)


def _capture_screenshot(name):
    driver.save_screenshot(name)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra