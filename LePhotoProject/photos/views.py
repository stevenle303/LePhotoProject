from turtle import title
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ContactForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'photos/home.html')
    

def loginUser(request):
    page = 'login'
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')
        else:
            messages.error(request,'username or password not correct')
            return redirect('login')

    return render(request, 'photos/login_register.html', {'page': page})

  


def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('gallery')
        else:
            messages.error(request,'Please make a stronger password!!')
            return redirect('register')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('photos/emails/contactform.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('The contact form subject', 'This is the message', 'noreplysteven.com', {'lesteven303@gmail.com'}, html_message=html)
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'photos/contact.html',{
        'form': form
    })

@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(category__name__contains=category,category__user=user)

    categories = Category.objects.filter(user=user)
    
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            title=data['title'],
            description=data['description'],
            image=image,
        )

        return redirect('gallery')



    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

    
def deletePhoto(request,pk):
    if request.method=='POST':
        photo = Photo.objects.get(id=pk)
        photo.delete()
        return redirect('gallery')



    
