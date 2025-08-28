from .models import Product, Category, Customer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from prometheus_client import Counter

category_access_counter = Counter(
    'category_access_total',
    'Total number of times each category is accessed',
    ['category_name']
)

def home(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})


def contact(request):
    return render(request, "contact.html")


def category(request, category_name):
    category = category_name.replace("-", " ")
    category_access_counter.labels(category_name=category).inc()
    try:
        category_obj = Category.objects.get(name__iexact=category)
        products = Product.objects.filter(category=category_obj)
        return render(
            request,
            "categories.html",
            {
                "products": products,
                "selected_category": category,
                "categories": Category.objects.all(),
            },
        )
    except Category.DoesNotExist:
        print(f"Category '{category}' does not exist.")
        messages.error(request, "Category not found.")
        return redirect("home")


def all_categories(request):
    return render(
        request,
        "categories.html",
        {
            "products": Product.objects.all(),
            "selected_category": None,
            "categories": Category.objects.all(),
        },
    )


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    else:
        return render(request, "login.html", {"active_tab": "login"})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            return render(
                request, "login.html", {"active_tab": "register", "form": form}
            )

        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone = form.cleaned_data.get("phone")

        user = form.save()

        customer = Customer.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "login.html", {"active_tab": "register", "form": form})


def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
        return render(request, "product.html", {"product": product})
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("home")
