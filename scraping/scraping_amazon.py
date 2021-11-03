from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
import re
import bs4
import json
import time
 
INSTAGRAM_DOMAIN = "https://www.instagram.com"
MIN_COUNT = 100
KEYWORD = "家系ラーメン"
CHROMEDRIVER = "../chromedriver"
 
# driver取得
def get_driver():
      
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    #options.add_argument('--headless')
    # ブラウザーを起動
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
      
    return driver
 
# 対象ページ取得
def get_text_from_target_page(driver, first_flg, url):
      
    # ターゲット
    driver.get(url)
     
    if first_flg:
        # articleタグが読み込まれるまで待機（最大10秒）
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))
    else:
        driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
      
    text = driver.page_source
          
    return text
 
# 正規表現で値を抽出
def get_search_value(ptn, str):
      
    result = re.search(ptn, str)
      
    if result:
        return result.group(1)
    else:
        return None
     
# info取得
def get_info_from_text(text):
    soup = bs4.BeautifulSoup(text, features='lxml')
      
    try:
        info = {}
        # 投稿（v1Nh3 kIKUG  _bz0w）
        elems = soup.find_all(class_="v1Nh3")
         
        for elem in elems:
            a_elem = elem.find("a")
            href = a_elem["href"]    
            url = INSTAGRAM_DOMAIN + href
            post_id = get_search_value("\/p\/(.*)\/", href)
             
            # img情報
            img_elem = elem.find("img")
            alt = img_elem["alt"]
            src = img_elem["src"]
             
            post_dic = {}
            post_dic["url"] = url
            post_dic["alt"] = alt
            post_dic["src"] = src
             
            info[post_id] = post_dic
              
        return info
         
    except:
        return None
     
# 最後の要素までスクロール
def scroll_to_elem(driver, footer_move_flg):
     
    try:
        if footer_move_flg:
            last_elem = driver.find_element_by_id("fb-root")   
 
 
            actions = ActionChains(driver);
            actions.move_to_element(last_elem);
            actions.perform();
        else:
            # 最後の要素の一つ前までスクロール
            elems = driver.find_elements_by_class_name("weEfm")
            last_elem = elems[-1]
              
            actions = ActionChains(driver);
            actions.move_to_element(last_elem);
            actions.perform();
          
        return True
    except:
        return False
 
# 投稿件数取得
def get_post_count(text):
    try:
        json_str = get_search_value("window._sharedData = (.*);<\/script>", text)
        dict = json.loads(json_str)
        post_count = dict["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["count"]
        return post_count
    except:
        return MIN_COUNT
     
if __name__ == '__main__':
     
    # url
    url = "https://www.instagram.com/explore/tags/" + urllib.parse.quote(KEYWORD) + "/"
 
    # ブラウザーを起動
    driver = get_driver()
 
    # 対象ページのhtmlソース取得
    text_0 = get_text_from_target_page(driver, True, url)
    post_count = get_post_count(text_0)
    print("合計：" + str(post_count))
     
    info_all = {}
    count_info = 0
    buf_count_info = 0
    while count_info < MIN_COUNT:
 
        # スクロール後対象ページのhtmlソース取得
        text_1 = driver.page_source
        info = get_info_from_text(text_1)
         
        if not None:
            info_all.update(info)
         
        count_info = len(info_all)
        time.sleep(1)
        print(count_info)
         
        if buf_count_info==count_info:
            time.sleep(3)
             
        result_flg = scroll_to_elem(driver, False)
        buf_count_info = count_info
         
        if post_count <= count_info:
            break
             
    driver.quit()