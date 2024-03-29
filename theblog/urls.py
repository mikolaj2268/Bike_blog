from django.urls import path
# from . import views
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, AddCommentView
from .views import export_posts_to_xml, export_user_data_to_excel
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(), name = "home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name = 'article-detail'),
    path('add_post/', AddPostView.as_view(), name = 'add_post'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name = 'update_post'),
    path('article/delete/<int:pk>/', DeletePostView.as_view(), name = 'delete_post'),
    path('add_category/', AddCategoryView.as_view(), name = 'add_category'),
    path('category/<str:categories>',CategoryView, name = 'category'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name = 'add_comment'),
    path('export/xml/', export_posts_to_xml, name='export_posts_xml'),
    path('export/excel/', export_user_data_to_excel, name='export_user_data_excel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
