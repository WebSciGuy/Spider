from bs4 import BeautifulSoup
import requests
import re
import operator
from stop_words import get_stop_words
from math import sqrt


# extract words from html, using the 'p' tag
def get_word_list(url):
    word_list = []
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    for text in soup.findAll('p'):
        if text.text is None:
            continue
        content = text.text
        # words to lowercase and split into an array
        words = content.lower().split()

        for word in words:
            # clear non-chars
            cleaned_word = clean_word(word)
            if len(cleaned_word) > 0:
                word_list.append(cleaned_word)

    return word_list


# clean up words with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word

def create_frequency_table(word_list):
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')
    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list


def cosine_similarity(url, comp_url):
    try:
        page_words = get_word_list(url)
        word_count = create_frequency_table(page_words)
        sorted_frequency_list = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
        sorted_theme_frequency_list = remove_stop_words(sorted_frequency_list)
        if len(sorted_theme_frequency_list) > 20:
            sorted_theme_frequency_list = sorted_theme_frequency_list[:20]

        sqr_total = 0
        sqr_list = []
        for key, value in sorted_theme_frequency_list:
            sqr_value = int(value * value)
            sqr_total = sum([sqr_total, sqr_value])
            sqr_list.append([key, value, sqr_value])
        sqrt_calc = sqrt(sqr_total)

        sqr_calc_list = []
        for key,value,calc in sqr_list:
            calc_value = float(value / sqrt_calc)
            sqr_calc_list.append([key,value, calc, calc_value])

        comp_temp_list = []
        for key, value in sorted_theme_frequency_list:
            if key not in comp_temp_list:
                comp_temp_list.append(str(key))

        comp_page_words = get_word_list(comp_url)
        compResults = {}
        for word in comp_temp_list:
            compResults.update({word:comp_page_words.count(word)})

        comp_frequency_list = []
        for key, value in compResults.items():
            tempVal = [key,value]
            comp_frequency_list.append(tempVal)

        comp_sqr_total = 0
        comp_sqr_list = []
        for key, value in comp_frequency_list:
            comp_sqr_value = int(value * value)
            comp_sqr_total = sum([comp_sqr_total, comp_sqr_value])
            comp_sqr_list.append([key, value, comp_sqr_value])
        comp_sqrt_calc = sqrt(comp_sqr_total)

        comp_sqr_calc_list = []
        for key,value,calc in comp_sqr_list:
            calc_value = float(value / comp_sqrt_calc)
            comp_sqr_calc_list.append([key,value, calc, calc_value])


        multiples_list = [row[3] for row in sqr_calc_list]
        comp_multiples_list = [row[3] for row in comp_sqr_calc_list]
        cos_calc = [x*y for x,y in zip(multiples_list, comp_multiples_list)]
        cos_sim = sum(cos_calc)
        print(url + ' and ' + comp_url + ' cosine similarity is ' + str(cos_sim))

        return cos_sim
    except:
        cos_sim = 0.0
        print(url + ' and ' + comp_url + ' cosine similarity, due to page error is ' + str(cos_sim))
        return cos_sim


