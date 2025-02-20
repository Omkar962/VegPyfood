
from django.urls import path,include
from . import views
from accounts import views as accountViews
urlpatterns = [
    path('',accountViews.vendorDashboard),
    path('profile/',views.vprofile,name="vprofile"),
    path('menu-builder/',views.menu_Builder,name="menu_Builder"),

    path('menu-builder/category/<int:pk>/',views.fooditem_by_category,name="fooditem_by_category"),
    path('menu-builder/category/add/',views.add_category,name="add_category"),
    path('menu-builder/category/edit/<int:pk>',views.edit_category,name="edit_category"),
    path('menu-builder/category/delete/<int:pk>',views.delete_category,name="delete_category"),

    path('menu-builder/fooditem/add/',views.add_fooditem,name="add_fooditem"),
    path('menu-builder/fooditem/edit/<int:pk>',views.edit_fooditem,name="edit_fooditem"),
    path('menu-builder/fooditem/delete/<int:pk>',views.delete_fooditem,name="delete_fooditem"),

    path('opening_hours/',views.opening_hours,name="opening_hours"),
    path('opening_hours/add/',views.add_opening_hours,name="add_opening_hours"),
    path('opening_hours/remove/<int:pk>',views.remove_opening_hours,name="remove_opening_hours"),

]
