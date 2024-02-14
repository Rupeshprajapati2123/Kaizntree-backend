from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import Product
from .utils import fetch_products_from_database, save_products_to_database
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .data import data
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_products(request):
   
    

    if not Product.objects.exists():
        save_products_to_database(data)

    products = Product.objects.all()

    # Apply filters based on query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    stock_status = request.query_params.get('stock_status')
    
    # Define category variable and initialize to None
    category = None
    
    # Retrieve category query parameter if provided
    if 'category' in request.query_params:
        category = request.query_params['category']

    # Apply filters based on query parameters
    if start_date:
        products = products.filter(date_created__gte=start_date)
    if end_date:
        products = products.filter(date_created__lte=end_date)
    if stock_status:
        products = products.filter(stock_status=stock_status)
    if category:  # Ensure category is not None before applying filter
        products = products.filter(category=category)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



    
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
def home(request): 
    return render(request, 'home.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')

