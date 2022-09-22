from django import template

register = template.Library()

CENSOR_LIST = ['Человек', 'новые', 'буквально', 'редиска', 'моды', 'больше', 'есть', 'скота']


@register.filter()
def censor(value):
    text = value.strip('!.,').split()
    text_out = ''
    for w in text:
        j = w.lower()
        for k in CENSOR_LIST:
            if j.find(k) != -1:
                first = w[0]
                last = (len(w) - 1) * '*'
                w = first + last
        text_out = text_out + ' ' + w
    return f'{text_out}'


