from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import base64
import re

"""
    账号储存在txt文件中
    账号--密码
"""

file = "./formated_accounts.txt"
admin_account = ""
admin_password = ""
url_xyhelper = ""

def get_webdriver():
    """
    自动下载并返回适合当前环境的 Chrome 浏览器驱动。
    """
    # 使用 Service 对象来创建 webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def input_text(driver, by, identifier, text):
    """
    在指定的输入框中输入文本。

    :param driver: WebDriver 实例
    :param by: 定位元素的方法 (例如 By.ID, By.NAME 等)
    :param identifier: 元素的定位标识符 (例如元素的id或name)
    :param text: 要输入的文本
    """
    element = driver.find_element(by, identifier)
    element.send_keys(text)


def input_text_by_placeholder(driver, placeholder, text):
    """
    在具有指定占位符的输入框中输入文本。

    :param driver: WebDriver 实例
    :param placeholder: 输入框的占位符文本
    :param text: 要输入的文本
    """
    xpath = f"//input[@placeholder='{placeholder}']"
    element = driver.find_element(By.XPATH, xpath)
    element.send_keys(text)

def get_src_of_element(driver, class_name):
    """
    获取具有特定class的元素的src属性值。

    :param driver: WebDriver 实例
    :param class_name: 元素的class名称
    :return: src属性的值
    """
    element = driver.find_element(By.CSS_SELECTOR, f".{class_name}")
    return element.get_attribute('src')

def extract_base64_content(encoded_string):
    """
    从base64编码的字符串中提取出base64内容。
    """
    # 查找 'base64,' 后面的内容
    match = re.search(r'base64,(.*)', encoded_string)
    if match:
        return match.group(1)
    else:
        return None

def decode_base64_to_svg(base64_content):
    """
    将base64内容解码成SVG字符串。
    """
    # 解码 base64 内容
    decoded_bytes = base64.b64decode(base64_content)
    return decoded_bytes.decode('utf-8')

def extract_digits_from_svg(svg_content):
    """
    从SVG内容中提取第二个出现的四位数字。
    """
    # 查找SVG中所有出现的四位数字
    matches = re.findall(r'\d{4}', svg_content)
    if matches and len(matches) >= 2:
        return matches[1]  # 返回列表中的第二个匹配项
    else:
        return None

def click_button(driver, by, identifier):
    """
    点击指定的按钮。

    :param driver: WebDriver 实例
    :param by: 定位元素的方法 (例如 By.ID, By.NAME, By.XPATH, By.CSS_SELECTOR 等)
    :param identifier: 元素的定位标识符 (例如元素的id、name、XPath、CSS选择器等)
    """
    # 定位按钮
    button = driver.find_element(by, identifier)

    # 点击按钮
    button.click()

def click_css_button(driver, css_selector):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    button = driver.find_element(By.CSS_SELECTOR, css_selector)
    button.click()

def click_menu_botten(driver):
    # 点击菜单按钮
    css_selector = ".app-topbar__collapse"
    click_css_button(driver, css_selector)

def add_account(driver, account, password, status, plus):
    #等待
    WebDriverWait(driver, 1000).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cl-dialog__controls")))
    # 调用click_css_button函数来点击增加按钮
    wait = WebDriverWait(driver, 10)
    css_selector = "button.el-button.el-button--primary"
    click_css_button(driver, css_selector)

    wait = WebDriverWait(driver, 10)
    input_text_by_placeholder(driver, "请填写邮箱", account)
    print(account)
    input_text_by_placeholder(driver, "请填写密码", password)
    print(password)

    if(status):
        click_button(driver, By.XPATH, '/html/body/div[6]/div/div/div/div/div/div[1]/form/div/div/div[3]/div/div/div/div/div/div/span')
    if(plus):
        click_button(driver, By.XPATH, '/html/body/div[6]/div/div/div/div/div/div[1]/form/div/div/div[4]/div/div/div/div/div/div/span')

    click_button(driver, By.XPATH, '/html/body/div[6]/div/div/div/div/div/div[2]/button[2]')


# 获取 webdriver 实例
driver = get_webdriver()

# 打开指定的网站
driver.get(url_xyhelper)

# 获取页面标题
title = driver.title
print("页面标题:", title)



while(True):
    try:
        input_text_by_placeholder(driver, "请输入用户名", admin_account)
        break
    except:
        print("waiting")

input_text_by_placeholder(driver, "请输入密码", admin_password)

# 等待 img 元素加载
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.base64")))

# 等待 img 元素加载
wait = WebDriverWait(driver, 10)
src_value = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.base64")))

# 获取 img 元素的 src 属性值
src_value = element.get_attribute('src')
print("获取到的 src 值:", src_value)

# 提取 base64 部分
base64_content = extract_base64_content(src_value)

# 解码为 SVG
svg_content = decode_base64_to_svg(base64_content)

# 从 SVG 中提取四位数字
digits = extract_digits_from_svg(svg_content)
print("获取到的 验证码 值:", digits)

input_text_by_placeholder(driver, "图片验证码", digits)

# 点击登录按钮
click_css_button(driver, "button.el-button.is-round")

# 点击工作台
try:
    wait = WebDriverWait(driver, 10)
    css_selector = ".el-sub-menu__title"
    click_css_button(driver, css_selector)
except:
    click_menu_botten(driver)

# 调用click_css_button函数来点击账号管理按钮
wait = WebDriverWait(driver, 10)
css_selector = "li.el-menu-item span"  # 请替换成实际的CSS选择器
click_css_button(driver, css_selector)

# 调用click_css_button函数来点击刷新按钮
wait = WebDriverWait(driver, 10)
css_selector = "button.el-button"
click_css_button(driver, css_selector)

# 初始化两个空数组来存储账号和密码
accounts = []
passwords = []

# 打开文件并逐行读取内容
with open(file, "r") as file:
    lines = file.readlines()
    for line in lines:
        # 使用split方法按空格分割每一行的内容，并存储到对应数组中
        parts = line.strip().split("--")
        if len(parts) == 2:
            accounts.append(parts[0])
            passwords.append(parts[1])

for i in range(0, len(accounts)):
    print("Doing:", i, "/", len(accounts))
    add_account(driver, accounts[i], passwords[i], True, False)

print("done")
driver.quit()
