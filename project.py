from selenium import webdriver
import time

emptyStr = ''
video_id = input('Video ID:')
url = f"https://www.youtube.com/watch?v={video_id}"
chromedriver_path = "chromedriver.exe"

driver = webdriver.Chrome(executable_path=chromedriver_path)
driver.get(url)
driver.implicitly_wait(3)

def go_to_end():
    driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight);")

flag = False

def get_scroll_height():
    return driver.execute_script(f"return document.documentElement.scrollHeight;")
    
while True:
    if get_scroll_height() < 1900:
        continue
    go_to_end()
    break

def get_amount(str):
    to_return = ""
    for char in str:
        if char in ",.0123456789":
            to_return += char
    to_return = to_return.replace(',','.')
    return float(to_return)

def get_currency(str):
    cr = ""
    for char in str:
        if char not in ",.0123456789":
            cr += char
    return cr            

while not flag:
    h2_elements = driver.find_elements_by_tag_name('h2')
    for element in h2_elements:
        try:
            if str(element.text).strip()[0].isdigit():
                comment_count = int(str(element.text).strip().split()[0].replace('.',emptyStr))
                flag = True
        except:
            pass

print("Comment Count:"+str(comment_count))


superchat_count = 0
comment_fetched = 0
flag = False
total = {}
superchats = []
while comment_fetched < comment_count:
    comments = driver.find_elements_by_tag_name('ytd-comment-thread-renderer')
    if len(comments) == comment_fetched:
        continue
    for comment in comments[comment_fetched:]:
        try:
            price = comment.find_element_by_id('comment-chip-price').text
            if price.strip() != emptyStr:
                superchats.append(price)
                superchat_count+=1
                if get_currency(price) not in total: 
                    total[get_currency(price)] = get_amount(price)
                else:
                    total[get_currency(price)] += get_amount(price)
               # print(comment.find_element_by_id('comment-chip-price').text)
        except:
            pass

    comment_fetched = len(comments)
    #print(superchats)
    for currency in total:
        print(f"TOTAL: {total[currency]:.2f}{currency}")
    print(f"COMMENT COUNT:{comment_fetched}")
    print(f"SUPERCHATS FOUND:{superchat_count}")
    go_to_end()

time.sleep(10000)
driver.quit()
