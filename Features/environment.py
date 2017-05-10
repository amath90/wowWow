from selenium import webdriver


def before_all(context):
    print("Executing before all")

def before_feature(context, feature):
    print("Before feature\n")

#Scenario level objects are popped off context when scenario exit
def before_scenario(context,scenario):
    context.browser = webdriver.Chrome("c:\Python36\Lib\site-packages\selenium\webdriver\chromedriver_win32\chromedriver.exe")
    print("Before scenario\n")

def after_scenario(context,scenario):
    context.browser.quit()
    print("After scenario\n")

def after_feature(context,feature):
    print("\nAfter feature")
aaaaaaa
def after_all(context):
    print("Executing after all")
