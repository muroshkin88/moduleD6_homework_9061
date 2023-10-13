from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
# from django.shortcuts import render
# from django.views import View # импортируем простую вьюшку
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, SubscribedUsersCategory
from .filters import NewsFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# class News(View):
    
#     def get(self, request):
#         news = Post.objects.order_by('-dateCreat')
#         n = Paginator(news, 1) # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
 
#         news = n.get_page(request.GET.get('page', 1)) # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
#         # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        
#         data = {
#             'news': news,
#         }
#         return render(request, 'news.html', data)
 
class NewsList(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-dateCreat')
    paginate_by = 1 # постраничный вывод в один элемент
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())

        #context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST )  # создаём новую форму

        if form.is_valid():  # если пользователь ввёл всё правильно
            form.save()

        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'post.html' # название шаблона будет product.html
    context_object_name = 'post' # название объекта

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_category'] = Category.objects.filter(subscribed_users=self.request.user)
        else:
            context['user_category'] = None
        return context


class SearchNews(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-dateCreat')
    paginate_by = 1 # постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'add.html'
    form_class = PostForm

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post')
    template_name = 'add.html'
    form_class = PostForm

    # метод get_object
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

def subscription(request):
    category_id = request.GET.get('category_id')
    print (category_id)
    category = Category.objects.get(id=category_id)
    
    if not category.subscribed_users.filter(email=request.user.email).exists():
        user = request.user
        SubscribedUsersCategory.objects.create(subscribed_users=user, category=category)
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))