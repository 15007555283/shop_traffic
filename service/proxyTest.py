import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from create_proxy_auth_extension import create_proxy_auth_extension
proxyHost = "proxy.smartproxycn.com"
proxyPort = "1000"
# 代理隧道验证信息（账号+密码）
proxyUser = "mallus_area-US"
proxyPass = "linemall888"
chrome_options = ChromeOptions()
chrome_options.add_extension(create_proxy_auth_extension(proxyHost, proxyPort, proxyUser, proxyPass))
prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
chrome_options.add_experimental_option('prefs', prefs)
driver = Chrome(options=chrome_options)
driver.get('https://www.menclothhrwe.com/index.php?route=product/category&path=59_64')
time.sleep(20)
print(driver.page_source)