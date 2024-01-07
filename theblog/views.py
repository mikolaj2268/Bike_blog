from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy
import xml.etree.ElementTree as ET
from django.http import HttpResponse
import pandas as pd

# def home(request):
#     return render(request, 'home.html', {})


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    # ordering = ['-id']

def CategoryView(request, categories):
    category_posts = Post.objects.filter(category = categories)
    return render(request, 'categories.html', {'categories':categories.title(), 'category_posts':category_posts})



class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')  # Redirect to home page or other page after post is created

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set author as the current logged-in user
        return super(AddPostView, self).form_valid(form)



class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    # fields = '__all__'
    # success_url = reverse_lazy('article-detail')  # Redirect to home page or other page after post is created
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     # Get the referer URL
    #     referer_url = self.request.META.get('HTTP_REFERER')
    #
    #     # If referer URL is present, use it; otherwise, fallback to a predefined page
    #     return referer_url if referer_url else reverse_lazy('home')
class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'
    # fields = ('title', 'body')

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def export_posts_to_xml(request):
    posts = Post.objects.all()  # Fetch all blog posts

    root = ET.Element("posts")
    for post in posts:
        post_element = ET.SubElement(root, "post")
        ET.SubElement(post_element, "title").text = post.title
        ET.SubElement(post_element, "body").text = post.body
        ET.SubElement(post_element, "post_date").text = str(post.post_date)
        ET.SubElement(post_element, "category").text = post.category

        author_element = ET.SubElement(post_element, "author")
        ET.SubElement(author_element, "username").text = post.author.username
        ET.SubElement(author_element, "first_name").text = post.author.first_name
        ET.SubElement(author_element, "last_name").text = post.author.last_name
        ET.SubElement(author_element, "email").text = post.author.email

    tree = ET.ElementTree(root)
    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="posts.xml"'
    tree.write(response, encoding='utf-8', xml_declaration=True)

    return response


def export_user_data_to_excel(request):
    # Filter posts by logged-in user
    user_posts = Post.objects.filter(author=request.user)

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(user_posts.values("title", "body", "post_date", "category")))

    # Create an Excel writer
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="user_data.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response