from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Product, Category, Customer, Order
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, OrderDetailForm, ProductForm
from .decorators.auth import unauthenticated_user, stop_login_signup, admin_only
# Create your views here.

class Index(View):
    def get(self, request):
        # print("You are : ", request.session.get('email'))

        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}

        id = request.GET.get('category_id')
        if id:
            c1 = Category.objects.get(id=id)
            products = c1.product_set.all().order_by('-id')
        else:
            products = Product.objects.all().order_by('-id')
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories
        }
        return render(request, 'store/index.html', context)

    def post(self, request):
        product_id = request.POST.get('product_id')

        cart = request.session.get('cart')
        decrease = request.POST.get('decrease')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if decrease:
                    if quantity <= 1:
                        del cart[product_id]
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        # print('------------quantity: ', request.session.get('cart'))
        return redirect('homepage')

@stop_login_signup
def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()
            # creating a customer data for user
            Customer.objects.create(user=user)
            # adding user to 'customer' group by default
            group = Group.objects.get(name="customer")
            # user.groups.add(group)    #this was not working so we wrote below code
            group.user_set.add(user)
            # messages.success(request, f"Account created successfully for user {username}!!!")
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'store/register.html', context)

@stop_login_signup
def loginUser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password')
            user = authenticate(request, username=un, password=pw)
            if user is not None:
                # this is same as doing below by login but here we're doing explicitly
                request.session['customer_id'] = Customer.objects.get(user=user).id
                request.session['email'] = user.email
                # print("User _ id=: ", user.id)
                # print(Customer.objects.get(user=user))
                login(request, user)
                # print('-' * 30)
                # print(request.user.id)
                # print(request.session['customer_id'])

                re_path = request.GET.get('redirect')
                # print(re_path)
                if re_path:
                    return redirect(re_path)
                return redirect('homepage')
            else:
                messages.info(request, 'Username or Password is incorrect !!!')
                return render(request, 'store/login.html')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    request.session.clear()
    return redirect('login')

class Cart(View):
    def get(self, request):
        cart = request.session.get('cart')
        context = {}
        if cart:
            keys = request.session.get('cart').keys()
            products = Product.get_product_by_ids(keys)
            # print(products)
            context = {
                'products': products
            }
        return render(request, 'store/cart.html', context)

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_product_by_ids(list(cart.keys()))
        """ print(products)
        print("-" * 20)
        print(customer_id)
        print(request.POST) """

        for product in products:
            order = Order(customer=Customer.get_customer_by_id(customer_id),
                          product=product,
                          price=product.price,
                          quantity=cart.get(str(product.id)),
                          address=address,
                          phone=phone
                          )
            # updating the total product quantity
            product.qty = product.qty - cart.get(str(product.id))
            # print(product.id, product.qty)
            if product.qty == 0:
                product.stock = "Out of Stock"
            product.save()
            order.placeOrder()

        # making our cart empty after order is placed
        request.session['cart'] = {}
        return redirect('cart')

class OrdersView(View):
    # @method_decorator(unauthenticated_user)
    def get(self, request):
        customer_id = request.session.get('customer_id')
        customer = Customer.get_customer_by_id(customer_id)
        orders = customer.order_set.all().order_by('-date')
        # print(orders)
        context = {
            'orders': orders
        }
        return render(request, 'store/orders.html', context)

# --------added------------

class SearchProductView(View):
    def get(self, request):
        search_text = request.GET.get('keyword')
        if search_text:
            products = Product.objects.filter(Q(name__icontains=search_text) | Q(category__name__icontains=search_text) | Q(description__icontains=search_text)).order_by('-id')
        else:
            products = Product.objects.all().order_by('-id')
        # print(search_text)
        # print("-" * 20)
        context = {
            'products': products
        }
        return render(request, 'store/searchproduct.html', context)


class ProductDetailView(View):
    def get(self, request, id):
        product = Product.get_product_by_id(id)
        context = {
            'product': product
        }
        return render(request, 'store/productdetail.html', context)


class UserProfileView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, id):
        customer_id = request.session.get('customer_id')
        customer = Customer.objects.get(id=customer_id)

        total_orders = customer.order_set.all().count()
        # print(total_orders)
        context = {
            'customer': customer,
            'total_orders': total_orders
        }
        return render(request, 'store/profile.html', context)

class UserProfileEditView(View):

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, id):
        customer_id = request.session.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        form = CustomerProfileForm(instance=customer)
        context = {
            'form': form,
        }
        return render(request, 'store/editprofile.html', context)

    def post(self, request, id):
        customer_id = request.session.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)

        # print("-" * 10)
        if form.is_valid():
            form.save()
            img = form["image"]
            form.image = img
            form.save()
            # print("-----------Updated_-----------------")
            messages.success(request, 'Profile updated successfully!!!')
        return redirect('profile', id=customer_id)


class AllProductsView(View):
    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'products': Product.objects.all()
        }
        return render(request, 'store/all_products.html', context)

class CancelCartView(View):
    def post(self, request):
        cart_id = request.POST.get('product_id')
        cart = request.session.get('cart')
        # print(cart.get(cart_id))
        if cart_id in cart.keys():
            del cart[cart_id]
        request.session['cart'] = cart
        # print(cart.get(cart_id))
        return redirect('cart')

# ------------admin part------------

admin_only_decorators = [login_required(login_url='/login/'), admin_only]
class AdminPanelView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request):
        # print(request.user.groups.all()[0].name)
        orders = Order.objects.all().order_by("-date")
        delivered_orders = Order.objects.filter(status=True).count()
        pending_orders = Order.objects.filter(status=False).count()
        total_orders = orders.count()
        customers = Customer.objects.all().order_by('-id')
        context = {
            'orders': orders,
            'total_orders': total_orders,
            'delivered_orders': delivered_orders,
            'pending_orders': pending_orders,
            'customers': customers,
        }
        return render(request, 'store/admin/adminPanel.html', context)

class OrderDetailUpdateView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request, id):
        order = Order.objects.get(id=id)
        form = OrderDetailForm(instance=order)
        context = {
            'form': form
        }
        return render(request, 'store/admin/order_detail.html', context)

    def post(self, request, id):
        order = Order.objects.get(id=id)
        form = OrderDetailForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully !!! ")
            return redirect('adminpanel')
        else:
            return redirect('orderdetail')

class CustomerFullDetailView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request, id):
        customer = Customer.objects.get(id=id)
        orders = customer.order_set.all().order_by("-date")
        total_order = orders.count()
        pending_orders = customer.order_set.filter(status=False).count()
        delivered_orders = customer.order_set.filter(status=True).count()
        # print(total_order, pending_orders, delivered_orders)
        context = {
            'customer': customer,
            'orders': orders,
            'total_orders': total_order,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders
        }
        return render(request, 'store/admin/customer_full_detail.html', context)

class DeleteOrderView(View):
    @method_decorator(admin_only_decorators)
    def post(self, request, id):
        order = Order.objects.get(id=id)
        if order:
            order.delete()
            messages.success(request, "Order deleted successfully !!!")
            return redirect('adminpanel')

class AdminProductView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request):
        products = Product.objects.all().order_by('-id')
        total_different_shoes = products.count()
        in_stock = Product.objects.filter(stock='In Stock').count()
        out_of_stock = Product.objects.filter(stock='Out of Stock').count()

        context = {
            'products': products,
            'total_different_shoes':total_different_shoes,
            'in_stock':in_stock,
            'out_of_stock':out_of_stock
        }
        return render(request, 'store/admin/admin_products.html', context)


class AddProductView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request):

        form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'store/admin/add_product.html', context)

    @method_decorator(admin_only_decorators)
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully !!!')
            return redirect("adminproducts")
        else:
            context = {
                'form': form
            }
            return render(request, 'store/admin/add_product.html', context)


class EditProductView(View):
    @method_decorator(admin_only_decorators)
    def get(self, request, id):
        product = Product.objects.get(id=id)
        form = ProductForm(instance=product)
        # print(form)
        context = {
            'form': form
        }
        return render(request, 'store/admin/add_product.html', context)

    @method_decorator(admin_only_decorators)
    def post(self, request, id):
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully !!!')
            return redirect("adminproducts")
        else:
            return render(request, 'store/admin/add_product.html', {'form': form})

class DeleteProductView(View):
    @method_decorator(admin_only_decorators)
    def post(self, request, id):
        product = Product.objects.get(id=id)
        if product:
            product.delete()
            messages.success(request, "Product deleted successfully !!!")
        return redirect("adminproducts")
