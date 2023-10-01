


import os
import json
import sys
import datetime
import time
from dateutil import parser

with open('data.json', encoding='utf8') as f:
    data = json.load(f)

def get_words():
    messages = data.get('messages')
    content = {}
    for message in messages:
        text = message.get('content').lower()
        if len(text) > 0:
            words = text.split()
            for word in words:
                if word in content:
                    content[word] += 1
                else:
                    content[word] = 1

    return content

def get_chars():
    messages = data.get('messages')
    chars = {}
    for message in messages:
        text = message.get('content').lower()
        if len(text) > 0:
            for char in text:
                if char in chars:
                    chars[char] += 1
                else:
                    chars[char] = 1

    return chars

def find_10_most_common():
    content = get_words()
    sorted_content = sorted(content.items(), key=lambda x: x[1], reverse=True)
    return sorted_content

def find_most_common_long():
    content = get_words()
    sorted_content = sorted(content.items(), key=lambda x: x[1], reverse=True)
    for word in sorted_content:
        if len(word[0]) > 5:
            return word[0]
        
def export_to_csv():
    sorted_content = find_10_most_common()
    with open('output.csv', 'w', encoding='utf8') as f:
        for word in sorted_content:
            f.write(f'{word[0]},{word[1]}\n')


def time_to_response():
    messages = data.get('messages')
    messages = sorted(messages, key=lambda x: timestamp_converter(x.get('timestamp')))
    time_to_response = []
    
    for i in range(len(messages) - 1):
        message = messages[i]
        next_message = messages[i + 1]
        if message.get('author').get('id') == '426757674886103051' and next_message.get('author').get('id') != '426757674886103051':
            time = get_time(next_message) - get_time(message)
            # print (time)
            time_to_response.append(time)

    return sum(time_to_response) / len(time_to_response) / 60


def get_firsts():
    my_firsts = 0
    your_firsts = 0


    messages = data.get('messages')
    messages = sorted(messages, key=lambda x: timestamp_converter(x.get('timestamp')))
    for i in range(1, len(messages)):
        message = messages[i]
        last_message = messages[i - 1]
        if time_diff(last_message, message) > 6 * 60 * 60:
            if message.get('author').get('id') == '426757674886103051':
                my_firsts += 1
            else:
                your_firsts += 1

    print('my firsts', my_firsts)
    print('your firsts', your_firsts)
    print(my_firsts / (my_firsts + your_firsts) * 100)
    return my_firsts, your_firsts   



def get_time(message):
    return timestamp_converter(message.get('timestamp'))

def time_diff(message1, message2):
    return abs(get_time(message2) - get_time(message1))

def timestamp_converter(date):
    return parser.parse(date).timestamp()


def export_chars():
    chars = get_chars()
    with open('chars.csv', 'w', encoding='utf8') as f:
        for char in chars:
            f.write(f'{char},{chars[char]}\n')

if __name__ == '__main__':
    print(find_most_common_long())
    print(time_to_response())
    export_to_csv()
    export_chars()
    get_firsts()
