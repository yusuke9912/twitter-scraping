# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
import urllib

Number = 0


with open('./log.txt', 'w') as f:
    for d in sys.path:
        f.write("%s\n" % d)
        
with open('../data/tweet.txt', 'w') as f:
            f.write("")  
        

keyword = urllib.quote(sys.argv[1])

file_path = "../data/tweet.json"
scroll_count = int(urllib.quote(sys.argv[2]))
scroll_wait_time = 2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

# tweet
def get_tweet():
    
    url = 'https://twitter.com/search?q='+keyword+'&src=typed_query&f=live'
    
    id_list = []
    tweet_list = []
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    
    # ブラウザーを起動
    driver = webdriver.Chrome("/home/ubuntu/environment/public/chromedriver", options=options)
    driver.get(url)

    # articleタグが読み込まれるまで待機（最大15秒）
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'article')))

    
    # 指定回数スクロール
    for i in range(scroll_count):
        
        id_list, tweet_list = get_article(url, id_list, tweet_list, driver)
        
        # スクロール＝ページ移動
        scroll_to_elem(driver)
        
        # ○秒間待つ（サイトに負荷を与えないと同時にコンテンツの読み込み待ち）
        time.sleep(scroll_wait_time)  
    
    # ブラウザ停止
    driver.quit()
    
    return tweet_list

def scroll_to_elem(driver):
    # 最後の要素の一つ前までスクロール
    elems_article = driver.find_elements_by_tag_name('article')
    last_elem = elems_article[-2]
    
    actions = ActionChains(driver);
    actions.move_to_element(last_elem);
    actions.perform();
    
def get_info_of_article(data):
    
    soup = BeautifulSoup(data, features='lxml')
    elems_a = soup.find_all("a")
    
    # 名前
    name_str = elems_a[1].text
    
    id = ''
    name = ''
    if name_str:
        name_list = name_str.split('@')
        name = name_list[0]
        id = name_list[1]
        
    # リンク
    link = elems_a[2].get("href")
    
    # 投稿日時
    datetime = elems_a[2].find("time").get("datetime")
    
    # 投稿
    base_elem = soup.find("div", role="group").parent
    
    tweet = soup.text.replace(name, "").replace(id, "")
    
    info = {}
    info["user_id"] = id
    info["user_name"] = name
    info["link"] = link
    info["datetime"] = datetime
    info["tweet"] = tweet
    
    with open('../data/tweet.txt', 'a') as f:
            f.write(tweet.encode('utf_8'))  

    
    print("<tr>")
    
    global Number
    Number = Number+1
    
    print("<td>"+ str(Number) +"</td>")
        
    print("<td>")
    print(name.encode('utf_8') + "\n")
    print("</td>")    
        
    print("<td>")
    print(datetime.encode('utf_8')[0:10] + "\n")
    print("</td>")
        
    print("<td>")
    print(tweet.encode('utf_8')[1:] + "\n")
    print("</td>")
        
    print("</tr>")

    return info

def get_article(url, id_list, tweet_list, driver):
    elems_article = driver.find_elements_by_tag_name('article')

    for elem_article in elems_article:
        try:
            tag = elem_article.get_attribute('innerHTML')

            elems_a = elem_article.find_elements_by_tag_name('a')
        
            if len(elems_a) < 2:
                continue
            
            href_2 = elems_a[1].get_attribute("href")
        

            #　tweet
            href_tweet = elems_a[2].get_attribute("href")
            
            
            if href_tweet not in id_list:
                
                
                # tweet情報取得
                info = get_info_of_article(tag)

                id_list.append(href_tweet)
                tweet_list.append(info)
        except Exception as e:
            with open('../log.txt', 'a') as f:
                f.write(str(e) + "\n")  
            continue
                
    return id_list, tweet_list


if __name__ == '__main__':
    # tweet情報をlist型で取得
    tweet_list = get_tweet()
    # データフレームに変換
    df = pd.DataFrame(tweet_list)
    # jsonとして保存
    df.to_json(file_path, orient='records',force_ascii= False)