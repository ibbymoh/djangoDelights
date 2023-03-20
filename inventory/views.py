from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from .models import *
from .forms import AddMenuItemForm
from django.urls import reverse ,reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime

#These make sure that we are logged in before we can see anything
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required()
def home(request):
    return render(request,'inventory/home.html')

#create a list view of all the ingredients
class IngredientsListView(LoginRequiredMixin,ListView):
    model = Ingredient

#create the view neccesary to edit the ingredients list
class IngredientCreateView(LoginRequiredMixin,CreateView):
    model = Ingredient
    fields = ["name","price","quantity","unit"]

#
class IngredientDeleteView(LoginRequiredMixin,DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredients-list')

class IngredientUpdateView(LoginRequiredMixin,UpdateView):
    model = Ingredient
    fields = ["price","quantity"]
    success_url = reverse_lazy("ingredients-list")
    template_name = 'inventory/ingredient_update.html'


class MenuItemtListView(LoginRequiredMixin,ListView):
    model = MenuItem

class MenuItemCreateView(LoginRequiredMixin,CreateView):
    model = MenuItem
    form_class = AddMenuItemForm

class RecipeRequirementCreateView(LoginRequiredMixin,CreateView,ListView):
    model = RecipeRequirement
    template_name = 'inventory/reciperequirement_list.html'
    fields = ["ingredient","quantity"]
    success_url = reverse_lazy('view-requirements')

    def get_queryset(self):
        name = self.kwargs['name']
        return RecipeRequirement.objects.filter(menu_item__name = name)

    def form_valid(self, form):
        name = self.kwargs['name']
        menu_item = MenuItem.objects.get(name=name)
        form.instance.menu_item = menu_item
        return super().form_valid(form)





class RecipeRequirementUpdateView(LoginRequiredMixin,UpdateView):

    fields = ["quantity"]
    template_name = 'inventory/reciperequirement_update.html'

    def get_queryset(self):
        ingredient_name = self.kwargs['slug']
        return RecipeRequirement.objects.filter(slug=ingredient_name)


    def get_success_url(self):
        # No need for reverse_lazy here, because it's called inside the method
        return reverse('view-requirements', kwargs={'name': self.kwargs['item_name']})


class RecipeRequirementDeleteView(LoginRequiredMixin,DeleteView):


    def get_queryset(self):
        ingredient_name = self.kwargs['slug']
        return RecipeRequirement.objects.filter(slug=ingredient_name)


    def get_success_url(self):
        # No need for reverse_lazy here, because it's called inside the method
        return reverse('view-requirements', kwargs={'name': self.kwargs['item_name']})


class PurchaseListView(LoginRequiredMixin,ListView):
    model = Purchase

"""this function gets called with a model menu-item and we essentially want to access all the recipe requirements 
for this menu-item and compare this to the inventory to see if there is enough ingredients in the inventory to make the item 
and if there is we can update the inventory and if there is not we should return an error message saying that this item cannot 
be made due to low stock. 

step 1: filter all the recipe requirments based on the menu-item name 
step 2: compare the quantity needed in the recipe requirment (reciperequirment.quantity) to the quantity available in the inventory (ingredient.quantity)

"""
@login_required()
def purchaseItem(request,name,price):
    requirements = RecipeRequirement.objects.filter(menu_item__name=name)

    #First we check every ingredient to see if it has the necceary requirements
    for requirement in requirements:
        if requirement.quantity > requirement.ingredient.quantity:
            return HttpResponse('Payment Unsuccesful')

    #if the above passes then we can edit the inventory accordingly
    for requirement in requirements:
        requirement.ingredient.quantity -= requirement.quantity
        requirement.ingredient.save()

    #now we log the purchase
    purchase = Purchase(item=name,datetime= datetime.now(),price=price)
    purchase.save()
    return HttpResponseRedirect(reverse('purchases'))

@login_required()
def viewFinances(request):
    purchases = Purchase.objects.all()
    revenue = 0
    cost = 0
    for purchase in purchases:
        revenue += purchase.price
        requirements = RecipeRequirement.objects.filter(menu_item__name=purchase.item)
        for requirement in requirements:
            cost += (requirement.quantity*requirement.ingredient.price)


    return render(request,template_name='inventory/finances.html/',context= {'cost':cost,'revenue':revenue})