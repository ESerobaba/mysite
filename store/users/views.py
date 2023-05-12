from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView 


from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from products.models import Basket
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, 'Поздравляем вы успешно зарегистрировались!')
#             return HttpResponseRedirect(redirect_to=reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form, 'title': 'Store - Зарегистрироваться'}
#     return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user,
                               data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    
    baskets = Basket.objects.filter(user=request.user)
    # total_sum= sum(x.sum() for x in baskets)
    # total_quantity=sum(x.quantity for x in baskets)
    # for basket in baskets:
    #     total_sum+=basket.sum()
    #     total_quantity+=basket.quantity
    context = {'title': 'Store - Профиль',
               'form': form,
               'baskets' : baskets,
            #    'total_sum':total_sum,
            #    'total_quantity':total_quantity,
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
