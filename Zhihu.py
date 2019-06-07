from selenium import webdriver
from time import sleep
import pandas as pd
import re
import numpy as np
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

driver = webdriver.Chrome('E:\\Python projects\\chromedriver.exe')
driver.get('https://www.zhihu.com/question/308798869/answers/updated?page=1')

pages = int(
    driver.find_element_by_xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div[21]/button[6]').text)
answer = []
for page in range(1, pages + 1):
    driver.get('https://www.zhihu.com/question/308798869/answers/updated?page={:}'.format(page))
    sleep(1)
    answers = driver.find_elements_by_class_name('List-item')
    for i in range(1, len(answers) + 1):
        tmp = driver.find_element_by_xpath(
            '//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div[{:}]/div/div[2]/div[1]/span'.format(str(i))).text
        answer.append(tmp)
    sleep(1)

answer_clean = [re.sub('\n', '', x) for x in answer]
answer_df = pd.DataFrame({'回答': answer_clean})
answer_df.to_csv('e:\\zhihu_shanghai.csv', index=False, encoding='utf-8-sig')


test = pd.read_csv('e:\\zhihu_shanghai.csv', encoding="utf-8")
key = jieba.analyse.extract_tags(test['回答'].str.cat(sep=' '), topK=200, withWeight=True)[20:]
wc_key = {x[0]: x[1] for x in key}
wordcloud = WordCloud(width=480, height=480, margin=0, collocations=False,
                      font_path=r'C:\Windows\Fonts\simsun.ttc').generate_from_frequencies(wc_key)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.savefig('e:\\wordcloud_shanghai.jpg')
plt.show()



jieba_dict = []
with open('E:\Python 3.6\Lib\site-packages\jieba\dict.txt', encoding='utf-8') as f:
    for line in f:
        jieba_dict.append(line)

