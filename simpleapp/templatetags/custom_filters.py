from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    Banned_List = ['idiot', 'stupid', 'donkey', 'Stupid', 'редиска', 'Редиска']
    sentence = value.split()
    for i in Banned_List:
        for words in sentence:
            if i in words:
                news = sentence.index(words)
                sentence.remove(words)
                sentence.insert(news, '*' * len(i))
    return " ".join(sentence)