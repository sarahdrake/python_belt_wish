from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.forms import widgets
import bcrypt, re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = []
        if len(postData["name"]) < 3 or len(postData["name"]) > 45:
            errors.append("Name must be between 3-45 characters.")
        elif not re.search(r'^[A-Z a-z]+$', postData["name"]):
            errors.append("Name cannot contain numbers or special characters.")
        if len(postData["username"]) < 3 or len(postData["username"]) > 45:
            errors.append("Please enter a username between 3-45 characters.")
        elif not re.search(r'^[A-Za-z0-9 ]+$', postData["username"]):
            errors.append("Username cannot contain special characters.")
        elif len(User.objects.filter(username=postData["username"])) > 0:
            errors.append("Username is already registered.")
        if len(postData["password"]) < 8:
            errors.append("Password must be 8 or more characters.")
        if postData["confirm"] != postData["password"]:
            errors.append("Passwords do not match.")
        if len(postData["hiredate"]) == 0:
            errors.append("Please enter hire date")
        # valid date format check:
        try:
            # attempt m/d/yy format first
            hiredate = datetime.strptime(postData["hiredate"], "%m/%d/%y")
        except ValueError:
            try:
                # attempt m/d/yyyy format next
                hiredate = datetime.strptime(postData["hiredate"], "%m/%d/%Y")
            except ValueError:
                errors.append("Invalid hire date format")
        if hiredate > datetime.now():
            errors.append("Hire date must be from the past")
        if len(errors) == 0:
            user  = User.objects.create(name=postData["name"], hiredate=hiredate, username=postData["username"], pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return (True, user)
        else:
            return (False, errors)

    def authenticate(self, postData):
        if "username" in postData and "password" in postData:
            try:
                user = User.objects.get(username=postData["username"])
            except User.DoesNotExist:
                return (False, "Invalid username/password combination")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid username/password combination")
        else:
            return (False, "Please enter login info")

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=100)
    hiredate = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
class WishlistManager(models.Manager):
    def makeWish(self, postData, user_id):
        errors = []
        # before proceeding any further check to see if user exists
        try:
            curr_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            errors.append("User not found. Please log in again")
            return {"success":False, "error_list":errors}
        # if curr_user exists proceed with blank field validations
        if len(postData["item"]) == 0:
            errors.append("Please enter an item or product")
        if len(postData["item"]) < 3:
            errors.append("Item must contain more than 3 characters")
        if len(errors) == 0:
            wish = Wishlist.objects.create(item=postData["item"], creator=curr_user)
            wish.members.add(curr_user)
            return {"success": True, "wish_object":wish}
        else:
            return {"success": False, "error_list":errors}
    def addWish(self, user_id, wish_id):
        msgs = []
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            msgs.append("User not found! Please log in again")
        try:
            wish = Wishlist.objects.get(id=wish_id)
        except Wishlist.DoesNotExist:
            msgs.append("Wish not found! Please select another item")
        # check to see if user is already a memeber of this wish
        if user in wish.members.all():
            msgs.append("You have already added this wish to your list!")
        # if validations pass then ADD user to the members in instance of the Wish object (as the variable wish)
        if len(msgs) == 0:
            wish.members.add(user)
            msgs.append("You have successfully added {} to wish to your list!". format(wish.item))
            return {"success": True, "msgs":msgs}
        else:
            return {"success": False, "msgs":msgs}

class Wishlist(models.Model):
    item = models.CharField(max_length=100)
    creator = models.ForeignKey(User)
    members = models.ManyToManyField(User, related_name="wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WishlistManager()
