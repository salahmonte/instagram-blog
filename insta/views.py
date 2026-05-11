from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from .models import Post   # import model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post, Categorie
from .models import Contact
from django.http import HttpResponseForbidden





def home(request):
    featured = Post.objects.filter(featured=True, status='approved')[:1]
    trending = Post.objects.filter(featured=True, status='approved').order_by('-created_at')[:4]

    posts = Post.objects.filter(status='approved').order_by("-created_at")

    paginator = Paginator(posts, 5)  # show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "featured": featured,
        "trending": trending,
        "page_obj": page_obj
    }

    return render(request, "insta/home.html", context)

def about(request):
    return render(request, 'insta/about.html')




def postDetails(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(
        category=post.category
    ).exclude(id=post.id)[:3]   # limit to 3
    return render(request, 'insta/detail_post.html', {  # <--- change here
        'post': post,
        'related_posts': related_posts
    })





def category(request):
    return render(request, 'insta/category.html')


@login_required
def CreatePost(request):
    categories = Categorie.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        body = request.POST.get('body')
        image = request.FILES.get('image')

        category = Categorie.objects.get(id=category_id)

        Post.objects.create(
            author=request.user,
            title=title,
            category=category,
            body=body,
            img=image,
            status='draft'   # important for dashboard counts
        )

        return redirect('dashboard')

    return render(
        request,
        'insta/forms.html',
        {'categories': categories}
    )


@login_required(login_url='login')
def dashboard(request):
    user = request.user

    total_posts = Post.objects.filter(author=user).count()
    published_posts = Post.objects.filter(author=user, status='approved').count()
    draft_posts = Post.objects.filter(author=user).exclude(status='approved').count()

    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
    }

    return render(request, 'insta/dashboard.html', context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 🔐 Only the creator can edit
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    categories = Categorie.objects.all()

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.body = request.POST.get("body")

        category_id = request.POST.get("category")
        if category_id:
            post.category = get_object_or_404(Categorie, id=category_id)

        if request.FILES.get("image"):
            post.img = request.FILES.get("image")

        post.save()
        return redirect("postDetails", pk=post.id)

    return render(request, "insta/edit_post.html", {
        "post": post,
        "categories": categories
    })



@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 🔐 Protect deletion
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect("dashboard")


from django.core.paginator import Paginator

@login_required
def all_posts(request):
    posts = Post.objects.filter(author=request.user).order_by("-created_at")

    paginator = Paginator(posts, 5)  # show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "insta/all_posts.html", {
        "page_obj": page_obj
    })

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        return render(request, 'insta/contact.html', {
            'success': True
        })

    return render(request, 'insta/contact.html')