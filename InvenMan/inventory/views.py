from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.timezone import now


# Create your views here.
def projecthomepage(request):
    return render(request,'open.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Borrower


# View to add item details
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item

# View to add item details
# def add_item(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         quantity = request.POST.get('quantity')
#         image = request.FILES.get('image')
#         category = request.POST.get('category')  # Capture category field
#
#         item = Item(
#             name=name,
#             quantity=quantity,
#             image=image,
#             category=category  # Save category to the database
#         )
#         item.save()
#
#         # After saving the item, redirect to the 'view_items' page
#         return redirect('view_items')
#
#     return render(request, 'add_item.html')
# # View to display all items
# from django.shortcuts import render
# from .models import Item

def add_item(request):
    # Check if the user is authenticated
    if not request.session.get('is_authenticated'):
        print("User is not authenticated. Redirecting to login3.")
        return redirect("login3")

    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        category = request.POST.get('category')

        item = Item(
            name=name,
            quantity=quantity,
            image=image,
            category=category
        )
        item.save()
        return redirect("view_items")

    return render(request, "add_item.html")


def view_items(request):
    categories = ['Books', 'Electronics', 'Stationary']
    categorized_items = {category: Item.objects.filter(category=category) for category in categories}
    return render(request, 'view_items.html', {'categorized_items': categorized_items})

# # View to edit item details
# def edit_item(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     if request.method == 'POST':
#         item.name = request.POST.get('name')
#         item.quantity = request.POST.get('quantity')
#         item.image = request.FILES.get('image') or item.image
#         item.save()
#         return redirect('view_items')
#     return render(request, 'edit_item.html', {'item': item})
#
# # View to delete an item
# def delete_item(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('view_items')
#     return render(request, 'delete_item.html', {'item': item})







from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

# Constants for authentication
AUTHORIZED_USERNAME = "KLGLUG"
AUTHORIZED_PASSWORD = "Swecha@123"

# Login1 view (for editing)
def login1(request, item_id=None):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
            return redirect("edit_item", item_id=item_id)  # Redirect to edit_item
        else:
            return render(request, "login1.html", {"error": "Invalid username or password"})
    return render(request, "login1.html")

# Login2 view (for deleting)
def login2(request, item_id=None):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
            return redirect("delete_item", item_id=item_id)  # Redirect to delete_item
        else:
            return render(request, "login2.html", {"error": "Invalid username or password"})
    return render(request, "login2.html")

def login3(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
            # Set session variable to indicate the user is authenticated
            request.session['is_authenticated'] = True
            print("User authenticated and redirected to add_item.")
            return redirect("add_item")
        else:
            return render(request, "login3.html", {"error": "Invalid username or password"})
    return render(request, "login3.html")

# Updated edit_item view
def login4(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
            # Set session variable to indicate the user is authenticated
            request.session['is_authenticated'] = True
            print("User authenticated and redirected to add_item.")
            return redirect("borrowed_items")
        else:
            return render(request, "login4.html", {"error": "Invalid username or password"})
    return render(request, "login4.html")

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.quantity = request.POST.get("quantity")
        item.image = request.FILES.get("image") or item.image
        item.save()
        return redirect("view_items")
    return render(request, "edit_item.html", {"item": item})

# Updated delete_item view
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("view_items")
    return render(request, "delete_item.html", {"item": item})

def borrow_item(request):
    items = Item.objects.all()  # Fetch all available items
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        branch = request.POST.get('branch')
        item_id = request.POST.get('item')
        quantity = int(request.POST.get('quantity'))

        # Fetch the selected item
        item = get_object_or_404(Item, id=item_id)

        # Check if the requested quantity is valid
        if quantity > item.quantity:
            return render(request, 'borrow_form.html', {
                'items': items,
                'error': f"Not enough stock for {item.name}. Only {item.quantity} available."
            })

        # Reduce the stock and save the updated item
        item.quantity -= quantity
        item.save()

        # Save the borrowing details
        borrower = Borrower(
            id_number=id_number,
            name=name,
            email=email,
            branch=branch,
            item=item,
            quantity=quantity
        )
        borrower.save()

        # Send an email to the borrower
        subject = "Item Borrowed from KLGLUG Successfully"
        message = (
            f"Dear {name},\n\n"
            f"You have successfully borrowed the following items from KLGLUG:\n\n"
            f"Item: {item.name}\n"
            f"Quantity: {quantity}\n"
            f"Branch: {branch}\n\n"
            f"Thank you for using our system! Make sure to return the items.\n\n"
            f"Best regards,\nKLGLUG"
        )
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        # Send an email to two specific recipients with full borrower details
        admin_subject = "KLGLUG Borrowing Notification"
        admin_message = (
            f"Borrower Details:\n\n"
            f"ID Number: {id_number}\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Branch: {branch}\n"
            f"Item Borrowed: {item.name}\n"
            f"Quantity Borrowed: {quantity}\n\n"
            f"Please ensure the borr    ower returns the items on time."
        )
        admin_recipient_list = ["idkbro909090@gmail.com"]
        send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, admin_recipient_list)

        # Redirect to the borrowed items page
        return redirect('borrowed_items')

    return render(request, 'borrow_form.html', {'items': items})

# View to display borrowed items
def borrowed_items(request):
    borrowers = Borrower.objects.all()
    return render(request, 'borrowed_items.html', {'borrowers': borrowers})

# View to mark an item as returned
def mark_returned(request, borrower_id):
    borrower = get_object_or_404(Borrower, id=borrower_id)

    if not borrower.is_returned:  # Only update if the item hasn't already been marked as returned
        # Add the borrowed quantity back to the item's available stock
        item = borrower.item
        item.quantity += borrower.quantity
        item.save()

        # Mark the borrow record as returned
        borrower.is_returned = True
        borrower.return_date = now()  # Record the current timestamp
        borrower.save()

    return redirect('borrowed_items')