from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from create_proxy_auth_extension import create_proxy_auth_extension
proxyHost = "us.smartproxy.com"
proxyPort = "10000"
# 代理隧道验证信息（账号+密码）
proxyUser = "user-mall"
proxyPass = "mail.2022"
chrome_options = ChromeOptions()
chrome_options.add_extension(create_proxy_auth_extension(proxyHost, proxyPort, proxyUser, proxyPass))
driver = Chrome(options=chrome_options)
driver.get('https://shop.snyder.cc')
print(driver.page_source)