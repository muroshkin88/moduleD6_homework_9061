from django import template
 
register = template.Library() # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(

bad_words = [
    'маргала',
    'редиска',
    'фуфло',
    'канай',
]
    
@register.filter(name='censor') # регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция


def censor(testText):
    # фильтр заменяет слова из стоп-листа на '...'
    for word in bad_words:
        testText = testText.lower().replace(word.lower(), '***') # ищем в переданном тексте слова из списка bad_words и меняем их на ***
    return testText