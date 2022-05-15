from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

## 简易功能，模拟登录bilibili

# 选择Chrome浏览器
def openChrome():
	return  webdriver.Chrome()   # Chrome浏览器

# 全部元素的方法
def getElementDetail(element):
	print('属性值，元素的文本')
	print(element.text)
	print('属性值，元素的标签名')
	print(element.tag_name)
	print('属性值，元素的大小')
	print(element.size)
	print('元素当前是否处于 enable 状态')
	print(element.is_enabled)
	print('元素当前是否处于被选中状态')
	print(element.is_selected)
	print('获取元素的属性值')
	print(element.get_attribute)
	print('获取元素的属性值')
	print(element.get_property)

# 获取文本
def getElementText(element):
	return element.text

# bilibili模拟登录
def operationAuth(driver,username, password):
	# 打开网页Bilibili
	driver.get("http://www.bilibili.com")

	## 进入到主界面，点击登录按钮来加载登录页面
	#获取bilibili登录按钮的xpath并定义按钮
	# 不等待，当页面加载缓慢的时候会死机
	#search_btn = driver.find_element_by_xpath('//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/li/div/div/span')
	# 显性等待，等待页面加载完成,每0.5s判断一次，直到20s
	search_btn = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/li/div/div/span')))
	# 获取 button 元素的标签名和大小
	#print('tagName = {}, size = {}'.format(
	#    search_btn.tag_name, search_btn.size))
	# 获取 button 的enable 和选中状态
	#print('Enabled = {}, Selected = {}'.format(
	#    search_btn.is_enabled(), search_btn.is_selected()))
	# 获取 button 的类名属性
	#print('Class name = {}'.format(search_btn.get_attribute('class')))
	getElementDetail(search_btn)
	#点击登录按钮
	search_btn.click()

	## 进入到登录页面
	#-------------------------------------------------------------------
	# 定位搜索的输入框
	username_input=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/div/div[2]/div[3]/div[2]/div[1]/input')))
	username_input.click()
	# 清除输入框中的内容
	username_input.clear()
	# 在输入框中模拟输入字符密码
	username_input.send_keys(username)
	# 这里就不用等了，同一个界面
	password_input = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/div[2]/div[2]/div[1]/input')
	password_input.click()
	# 清除输入框中的内容
	password_input.clear()
	# 在输入框中模拟输入字符密码
	password_input.send_keys(password)
	nameofJourney ='Bilibili Health Check'
	takeScreenshots(driver,nameofJourney)
	# 不要每次都点击登录，号封了没法追番^_^, 此处需要手动验证
	#loginButton_OnInputPage =driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/div[3]/div[2]')
	#loginButton_OnInputPage.click()
# 用来做健康检查
def takeScreenshots(driver, nameofJourney):
	time.sleep(0.5)
	screenshot_dir = os.path.join(os.path.dirname(__file__),"logs/screenshots")
	if not os.path.exists(screenshot_dir):
		os.makedirs(screenshot_dir)
	driver.save_screenshot(os.path.join(screenshot_dir, time.strftime(nameofJourney+"%Y%m%d-%H%M%S", time.localtime(time.time())) + ".png"))
	time.sleep(1)

def openBaidu(driver):
	# 第二个网站 百度
	js="window.open('{}','_blank');"
	driver.execute_script(js.format('https://www.baidu.com/'))
	#切换到最新页面
	driver.switch_to.window(driver.window_handles[-1]) 
	baiduSearch_input = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="kw"]')))
	baiduSearch_input.clear()
	baiduSearch_input.send_keys('今天天气')
	baiduSearch_button=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="su"]')))
	baiduSearch_button.click()
	# 此处需要手动通过百度搜索验证
	time.sleep(2)
	#new_alert=driver.switch_to.alert
	#print('出现alert',new_alert.text)
	tianqi_text=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="1"]/div[1]/div[1]/a[1]/p[3]')))
	print(getElementText(tianqi_text))
	nameofJourney='百度天气 Health Check'
	takeScreenshots(driver,nameofJourney)
	# 切换到最旧的窗口
	driver.switch_to.window(driver.window_handles[0])
	time.sleep(0.5)
	# 切换到第二个窗口
	driver.switch_to.window(driver.window_handles[1])

	time.sleep(2)

if __name__ == '__main__':
	driver=openChrome()
	username = ''
	password = ''
	# 加上报错机制，失误直接送走网页，不管怎样都送走,关烦了
	try:
		operationAuth(driver,str(username),str(password))
		openBaidu(driver)
	except Exception as e :
		print(e)
		driver.quit()
	finally:
		print('测试的时候启动，每次执行完自动关闭，别麻烦我')
		driver.quit()

## 基础代码二， Headless 启动
# chrome_options = webdriver.ChromeOptions()
# # 增加无界面选项
# chrome_options.headless = True
# browser = webdriver.Chrome(options=chrome_options)
# print("没有东西啊",browser.title)
# browser.quit()
