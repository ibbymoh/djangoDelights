from django.urls import path

from .views import  *



urlpatterns = [
    path('ingredients/',IngredientsListView.as_view(),name="ingredients-list"),
    path('ingredient/add',IngredientCreateView.as_view(),name="ingredient-add"),
    path('',home,name="home"),
    path('ingredient/<slug:slug>/delete/',IngredientDeleteView.as_view(),name="ingredient-delete"),
    path('ingredient/<slug:slug>/update/',IngredientUpdateView.as_view(),name="ingredient-update"),
    path('menu-items/',MenuItemtListView.as_view(),name="menu-item-list"),
    path('menu-item/add',MenuItemCreateView.as_view(),name="menu-item-add"),
    path('<name>/requirements/',RecipeRequirementCreateView.as_view(),name="view-requirements"),
    path('<item_name>/requirements/<slug:slug>/delete/',RecipeRequirementDeleteView.as_view(),name="delete-requirement"),
    path('<item_name>/requirements/<slug:slug>/update/',RecipeRequirementUpdateView.as_view(),name="update-requirements"),
    path('purchases/',PurchaseListView.as_view(),name='purchases'),
    path('success/<name>/<price>/',purchaseItem,name="purchase-item"),
    path('finances/',viewFinances,name="financial-page")

]