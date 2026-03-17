"""
URL configuration for TestTask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TestTaskApp import views

urlpatterns = [
    path("ajax/load-categories/", views.load_categories, name="ajax_load_categories"),
    path("ajax/load-subcategories/", views.load_subcategories, name="ajax_load_subcategories"),
    path('', views.Index),
    path('transactions', views.TransactionsView),
    path('transactions/add', views.AddTransaction),
    path('transactions/edit/<int:id>', views.EditTransaction),
    path('transactions/delete/<int:id>', views.DeleteTransaction),
    path('statuses', views.StatusesView),
    path('statuses/add', views.AddStatus),
    path('statuses/edit/<int:id>', views.EditStatus),
    path('statuses/delete/<int:id>', views.DeleteStatus),
    path('types', views.TypesView),
    path('types/add', views.AddType),
    path('types/edit/<int:id>', views.EditType),
    path('types/delete/<int:id>', views.DeleteType),
    path('categories', views.CategoriesView),
    path('categories/add', views.AddCategory),
    path('categories/edit/<int:id>', views.EditCategory),
    path('categories/delete/<int:id>', views.DeleteCategory),
    path('subcategories', views.SubCategoriesView),
    path('subcategories/add', views.AddSubCategory),
    path('subcategories/edit/<int:id>', views.EditSubCategory),
    path('subcategories/delete/<int:id>', views.DeleteSubCategory),
    path('admin/', admin.site.urls),
]
