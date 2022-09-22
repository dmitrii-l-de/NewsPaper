s = 'хорошо плохо, нормально не будем ходить в воду, По вечераь 9, фбв, 22'


cens_list = ['плохо', 'по', 'фбв']

# def censor_filter(s):
#     for i in cens_list:
#         s = s.lower()
#         s = s.replace(i, '***')
#     return s


# def censor_filter(s):
#     words = s.split()
#     for word in words:
#         value = word.strip('.,?!').lower()
#         if value in cens_list:
#             words[words.index(word)] = '***'
#
#     return ' '.join(words)


# def censor(value):
#     text = value.strip('!.,').split()
#     text_out = ''
#     for w in text:
#         j = w.lower()
#         for k in cens_list:
#             if j.find(k) != -1:
#                 first = w[0]
#                 last = (len(w) - 1) * '*'
#                 w = first + last
#         text_out = text_out + ' ' + w
#     return f'{text_out}'
#
#
# print(censor(s))
#





