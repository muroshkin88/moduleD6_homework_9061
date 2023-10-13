from django.urls import path
from .views import NewsList, PostDetail, SearchNews, PostCreateView, PostDeleteView, PostUpdateView, subscription # импортируем наше представление
 
 
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    
    path('', NewsList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('search/', SearchNews.as_view()),
    path('add/', PostCreateView.as_view(), name='add_post'), # сщздаем новую новость
    path('<int:pk>/', PostDetail.as_view(), name='detail_post'),
    path('subscription/', subscription, name='subscription'),
    path('add/<int:pk>', PostUpdateView.as_view(), name='edit_post'), # редактируем новость
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete_post'), # удаляем новость
    path('<int:pk>', PostDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон

]