from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from .models import User, Wishlist


def index(request):
    if "id" in request.session:
        return redirect('/dashboard')
    return render(request, 'wishlist/index.html')

def process(request):
    # this method will use call on REGISTRATION validations made in models and either set session.id to the valid user.id and redirect to home page or return relevant error messages and redirect back home
    if request.method != "POST":
        return redirect('/')
    else:
        user_valid = User.objects.validate(request.POST)
    if user_valid[0] == True:
        request.session["id"] = user_valid[1].id
        return redirect('/dashboard')
    else:
        for msg in user_valid[1]:
            messages.add_message(request, messages.INFO, msg)
        return redirect('/')
def login(request):
    # this method will use call on LOGIN validations made in models and either set session.id to the valid user.id and redirect to home page or return relevant error messages and redirect back home
    if request.method != "POST":
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        if user[0] == True:
            request.session["id"] = user[1].id
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')
def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect('/')

def success(request):
    # this method will render the homepage template-- will need to send along filtered user, differentiated wish objects to be parsed through in the template for displaying purposes
    if "id" not in request.session:
        messages.info(request, "Pleaes log in or register")
        return redirect('/')
    try:
        user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.info(request, "User not found. Please register")
        return redirect('/')

    my_wishes = Wishlist.objects.filter(members=user)

    other_wishes = Wishlist.objects.all().exclude(members=user)
    return render(request, 'wishlist/success.html', {"user": user, "my_wishes":my_wishes, "other_wishes": other_wishes})

def addwish(request):
    # this method is used to make sure that only user.id's that are in session access the corresponding url and RENDER the add wish template
    if "id" not in request.session:
        messages.info(request, "Plese login or register")
        return redirect('/')
    return render(request, 'wishlist/add.html')

def addprocess(request):
    if request.method != "POST":
        messages.info(request, "Please use the form to add a wish list item")
        return redirect('/dashboard')
    if "id" not in request.session:
        messages.info(request, "Please log in or register")
        return redirect('/')
    wish_valid = Wishlist.objects.makeWish(request.POST, request.session["id"])
    if wish_valid["success"] == True:
        return redirect('/wish_items/{}'. format(wish_valid["wish_object"].id))
    else:
        for msg in wish_valid["error_list"]:
            messages.info(request, msg)
        return redirect('/add')

def item(request, item_id):
    # this method will render wish.html. Need to pass through user object (as curr_user), wishlist object (as item), another wishlist object (as members of the wish but excluding the creator username).
    if "id" not in request.session:
        messages.info(request, "Please log in or register")
        return redirect('/')
    try:
        curr_user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.info(reqeust, "Your session has expired. Please log in or register")
        return redirect('/')
    try:
        item = Wishlist.objects.get(id=item_id)
    except Wishlist.DoesNotExist:
        messages.info(request, "Wish not found!")
        return redirect('/dashboard')

    return render(request, 'wishlist/wish.html', {"user":curr_user, "item":item, "members":item.members.all()})

def addtowishlist(request, item_id):
    if "id" not in request.session:
        messages.info(request, "Please log in or register.")
        return redirect('/')
    try:
        item = Wishlist.objects.get(id=item_id)
    except Wishlist.DoesNotExist:
        messages.info(request, "Wish not found!")
        return redirect('/dashboard')
    try:
        curr_user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.info(reqeust, "Your session has expired. Please log in or register")
        return redirect('/')

    valid_add = Wishlist.objects.addWish(request.session["id"], item_id)

    for msg in valid_add["msgs"]:
        messages.info(request, msg)
    return redirect('/dashboard')

def delete(request, item_id):
    try:
        target = Wishlist.objects.get(id=item_id)
    except Wishlist.DoesNotExist:
            messages.info(request, "Wish not found!")
            return redirect('/dashboard')
    target.delete()
    return redirect('/')

def remove(request, item_id):
    if "id" not in request.session:
        messages.info(request, "Pleaes log in or register")
        return redirect('/')
    try:
        curr_user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.info(reqeust, "Your session has expired. Please log in or register")
        return redirect('/')
    try:
        remove_wish = Wishlist.objects.get(id=item_id)
    except Wishlist.DoesNotExist:
        messages.info(reqeust, "Wish not found!")
        return redirect('/dashboard')
    remove_wish.members.remove(curr_user)
    return redirect('/dashboard')
