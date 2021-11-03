import re
import zipfile
import urllib.request
import os.path
import glob

#テキストを読み込む
fp = open("../data/tweet.txt", "rt", encoding="utf-8")
text = fp.read()

# 文単位のリストに分割
sentences = text.split("。")

import MeCab
mecab = MeCab.Tagger("-Ochasen")

# 文単位の名詞リストを生成
noun_list = [
             [v.split()[2] for v in mecab.parse(sentence).splitlines()
             if (len(v.split())>=3 and v.split()[3][:2]=='名詞')]
             for sentence in sentences
             ]

import itertools
from collections import Counter

# 文単位の名詞ペアリストを生成
pair_list = [
             list(itertools.combinations(n, 2))
             for n in noun_list if len(noun_list) >=2
             ]

# 名詞ペアリストの平坦化
all_pairs = []
for u in pair_list:
    all_pairs.extend(u)

# 名詞ペアの頻度をカウント
cnt_pairs = Counter(all_pairs)

import pandas as pd
import numpy as np

tops = sorted(
    cnt_pairs.items(), 
    key=lambda x: x[1], reverse=True
    )[:50]
    
noun_1 = []
noun_2 = []
frequency = []

# データフレームの作成
for n,f in tops:
    noun_1.append(n[0])    
    noun_2.append(n[1])
    frequency.append(f)

df = pd.DataFrame({'前出名詞': noun_1, '後出名詞': noun_2, '出現頻度': frequency})

# 重み付きデータの設定
weighted_edges = np.array(df)

import matplotlib.pyplot as plt
import networkx as nx


# グラフオブジェクトの生成
G = nx.Graph()

# 重み付きデータの読み込み
G.add_weighted_edges_from(weighted_edges)

# ネットワーク図の描画
plt.figure(figsize=(10,10))
nx.draw_networkx(G,
                 node_shape = "s",
                 node_color = "c", 
                 node_size = 500,
                 edge_color = "gray", 
                 font_family = "IPAexGothic") # フォント指定

plt.savefig('co-occurance.png', bbox_inches='tight')