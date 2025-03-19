# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages

# # Node.js API Base URL
# NODE_API_BASE = "http://localhost:5000/api/auth"
# NODE_API_POSTS = "http://localhost:5000/api/posts"

# # Signup View
# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         try:
#             response = requests.post(f"{NODE_API_BASE}/signup", json={"username": username, "password": password})

#             if response.status_code == 201:
#                 messages.success(request, "User registered successfully. Please login.")
#                 return redirect("login")
#             else:
#                 error_message = response.json().get("message", "Signup failed") if response.text else "Signup failed"
#                 messages.error(request, error_message)

#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Error connecting to server: {e}")

#     return render(request, "signup.html")

# # Login View
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         try:
#             response = requests.post(f"{NODE_API_BASE}/login", json={"username": username, "password": password})

#             if response.status_code == 200:
#                 data = response.json()
#                 request.session["token"] = data.get("token")  # Store token in session
#                 messages.success(request, "Login successful.")
#                 return redirect("home")
#             else:
#                 messages.error(request, "Invalid credentials")

#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Error connecting to server: {e}")

#     return render(request, "login.html")

# # Logout View
# def logout_view(request):
#     request.session.flush()
#     messages.success(request, "Logged out successfully!")
#     return redirect("login")

# # Home View
# NODE_API_BASE = "http://localhost:5000/api/auth"
# NODE_API_POSTS = "http://localhost:5000/api/posts"

# # Home View
# def home_view(request):
#     token = request.session.get("token")
#     if not token:
#         messages.error(request, "You must be logged in to access this page.")
#         return redirect("login")

#     headers = {"Authorization": f"Bearer {token}"}

#     try:
#         response = requests.get(NODE_API_POSTS, headers=headers)
#         posts = response.json() if response.status_code == 200 else []
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error fetching posts: {e}")
#         posts = []

#     if request.method == "POST":
#         title = request.POST.get("title")
#         content = request.POST.get("content")
#         image = request.FILES.get("image")

#         files = {"image": (image.name, image, image.content_type)} if image else None
#         data = {"title": title, "content": content}

#         try:
#             response = requests.post(NODE_API_POSTS, data=data, files=files, headers=headers)
            
#             if response.status_code == 201:
#                 messages.success(request, "Post uploaded successfully!")
#                 return redirect("home")
#             else:
#                 messages.error(request, f"Failed to upload post: {response.text}")
#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Error connecting to server: {e}")

#     return render(request, "home.html", {"posts": posts})
# # Delete Post View
# def delete_post_view(request, post_id):
#     token = request.session.get("token")
#     if not token:
#         messages.error(request, "You must be logged in to delete posts.")
#         return redirect("login")

#     headers = {"Authorization": f"Bearer {token}"}

#     try:
#         response = requests.delete(f"{NODE_API_POSTS}/{post_id}", headers=headers)
#         if response.status_code == 200:
#             messages.success(request, "Post deleted successfully!")
#         else:
#             messages.error(request, "Failed to delete post.")

#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error connecting to server: {e}")

#     return redirect("home")
import requests
from django.shortcuts import render, redirect
from django.contrib import messages

# Node.js API Base URL
NODE_API_BASE = "http://localhost:5000/api/auth"
NODE_API_POSTS = "http://localhost:5000/api/posts"

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            response = requests.post(f"{NODE_API_BASE}/signup", json={"username": username, "password": password})

            if response.status_code == 201:
                messages.success(request, "User registered successfully. Please login.")
                return redirect("login")
            else:
                error_message = response.json().get("message", "Signup failed") if response.text else "Signup failed"
                messages.error(request, error_message)

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error connecting to server: {e}")

    return render(request, "signup.html")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            response = requests.post(f"{NODE_API_BASE}/login", json={"username": username, "password": password})

            if response.status_code == 200:
                data = response.json()
                request.session["token"] = data.get("token")  # Store token in session
                messages.success(request, "Login successful.")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error connecting to server: {e}")

    return render(request, "login.html")

# Logout View
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Home View
def home_view(request):
    token = request.session.get("token")
    if not token:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    posts = []

    try:
        response = requests.get(NODE_API_POSTS, headers=headers)
        if response.status_code == 200:
            posts = response.json()
            # Ensure all posts have valid IDs
            posts = [post for post in posts if "_id" in post and post["_id"]]
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching posts: {e}")
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        files = {"image": (image.name, image, image.content_type)} if image else None
        data = {"title": title, "content": content}

        try:
            response = requests.post(NODE_API_POSTS, data=data, files=files, headers=headers)
            
            if response.status_code == 201:
                messages.success(request, "Post uploaded successfully!")
                return redirect("home")
            else:
                messages.error(request, f"Failed to upload post: {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error connecting to server: {e}")

    return render(request, "home.html", {"posts": posts})

# Delete Post View
def delete_post_view(request, post_id):
    token = request.session.get("token")
    if not token:
        messages.error(request, "You must be logged in to delete posts.")
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.delete(f"{NODE_API_POSTS}/{post_id}", headers=headers)
        if response.status_code == 200:
            messages.success(request, "Post deleted successfully!")
        else:
            messages.error(request, "Failed to delete post.")

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error connecting to server: {e}")

    return redirect("home")

