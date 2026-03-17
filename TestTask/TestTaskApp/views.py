from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Transaction, TransactionCategory, TransactionStatus, TransactionType, Subcategory
from .forms import TransactionForm, TransactionFilterForm


def load_categories(request):
    # Динамическая подгрузка категорий
    type_id = request.GET.get("type_id")
    categories = TransactionCategory.objects.filter(Type_id=type_id).values("id", "CatName")
    return JsonResponse(list(categories), safe=False)


def load_subcategories(request):
    # Динамическая подгрузка подкатегорий
    category_id = request.GET.get("category_id")
    subcategories = Subcategory.objects.filter(Category_id=category_id).values("id", "SubCatName")
    return JsonResponse(list(subcategories), safe=False)


def Index(request):
    return HttpResponseRedirect("/transactions")

def TransactionsView(request):
    # Отрисовка страницы с просмотром данных о ДДС, фильтров для них и формы для добавления новых
    transactions = Transaction.objects.all()
    addform = TransactionForm()
    form = TransactionFilterForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data.get('start_date'):
            transactions = transactions.filter(TransactionDate__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            transactions = transactions.filter(TransactionDate__lte=form.cleaned_data['end_date'])
        if form.cleaned_data.get('status'):
            transactions = transactions.filter(Status=form.cleaned_data['status'])
        if form.cleaned_data.get('type'):
            transactions = transactions.filter(Type=form.cleaned_data['type'])
        if form.cleaned_data.get('category'):
            transactions = transactions.filter(Category=form.cleaned_data['category'])
        if form.cleaned_data.get('subcategory'):
            transactions = transactions.filter(Subcategory=form.cleaned_data['subcategory'])
    return render(request, "transactions.html", {"transactions": transactions, "form": addform, "filterform": form})


def AddTransaction(request):
    # Добавление нового ДДС
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect("/transactions")


def DeleteTransaction(request, id):
    # Удаление выбранного ДДС
    try:
        transaction = Transaction.objects.get(id=id)
        transaction.delete()
        return HttpResponseRedirect("/transactions")
    except Transaction.DoesNotExist:
        return HttpResponseNotFound("<h1>ДДС не найдено</h1>")


def EditTransaction(request, id):
    # Изменение данных выбранного ДДС
    try:
        transaction = Transaction.objects.get(id=id)
        if request.method == "POST":
            form = TransactionForm(request.POST, instance=transaction)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/transactions")
        else:
            form = TransactionForm(instance=transaction)
            return render(request, "TransactionEdit.html", {"transaction": transaction, "form": form})
    except Transaction.DoesNotExist:
        return HttpResponseNotFound("<h1>ДДС не найдено</h1>")


def StatusesView(request):
    # Отображение списка статусов и формы для добавления новых
    statuses = TransactionStatus.objects.all()
    return render(request, "statuses.html", {"statuses": statuses})


def AddStatus(request):
    # Добавление нового статуса
    if request.method == "POST":
        status = TransactionStatus()
        status.StatusName = request.POST.get("name")
        status.save()
    return HttpResponseRedirect("/statuses")


def DeleteStatus(request, id):
    # Удаление выбранного статуса
    try:
        status = TransactionStatus.objects.get(id=id)
        status.delete()
        return HttpResponseRedirect("/statuses")
    except TransactionStatus.DoesNotExist:
        return HttpResponseNotFound("<h1>Статус не найден</h1>")


def EditStatus(request, id):
    # Изменения выбранного статуса
    try:
        status = TransactionStatus.objects.get(id=id)
        if request.method == "POST":
            status.StatusName = request.POST.get("name")
            status.save()
            return HttpResponseRedirect("/statuses")
        else:
            return render(request, "StatusEdit.html", {"status": status})
    except TransactionStatus.DoesNotExist:
        return HttpResponseNotFound("<h1>Статус не найден</h1>")


def TypesView(request):
    # Отображение списка типов и формы для добавления новых
    types = TransactionType.objects.all()
    return render(request, "types.html", {"types": types})


def AddType(request):
    # Добавление нового типа
    if request.method == "POST":
        trtype = TransactionType()
        trtype.TypeName = request.POST.get("name")
        trtype.save()
    return HttpResponseRedirect("/types")


def DeleteType(request, id):
    # Удаление выбранного типа
    try:
        trtype = TransactionType.objects.get(id=id)
        trtype.delete()
        return HttpResponseRedirect("/types")
    except TransactionType.DoesNotExist:
        return HttpResponseNotFound("<h1>Тип не найден</h1>")


def EditType(request, id):
    # Изменение выбранного типа
    try:
        trtype = TransactionType.objects.get(id=id)
        if request.method == "POST":
            trtype.TypeName = request.POST.get("name")
            trtype.save()
            return HttpResponseRedirect("/types")
        else:
            return render(request, "TypeEdit.html", {"trtype": trtype})
    except TransactionType.DoesNotExist:
        return HttpResponseNotFound("<h1>Тип не найден</h1>")


def CategoriesView(request):
    # Отображение списка категорий и формы для добавления новых
    trtypes = TransactionType.objects.all()
    categories = TransactionCategory.objects.all()
    return render(request, "categories.html", {"categories": categories, "types": trtypes})


def AddCategory(request):
    # Добавление новой категории
    if request.method == "POST":
        category = TransactionCategory()
        category.CatName = request.POST.get("name")
        category.Type = TransactionType.objects.get(TypeName=request.POST.get("typeName"))
        category.save()
    return HttpResponseRedirect("/categories")


def DeleteCategory(request, id):
    # Удаление выбранной категории
    try:
        category = TransactionCategory.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect("/categories")
    except TransactionCategory.DoesNotExist:
        return HttpResponseNotFound("<h1>Категория не найдена</h1>")


def EditCategory(request, id):
    # Изменение выбранной категории
    try:
        category = TransactionCategory.objects.get(id=id)
        trtypes = TransactionType.objects.all()
        if request.method == "POST":
            category.CatName = request.POST.get("name")
            category.Type = TransactionType.objects.get(TypeName=request.POST.get("typeName"))
            category.save()
            return HttpResponseRedirect("/categories")
        else:
            return render(request, "CategoryEdit.html", {"category": category, "types": trtypes})
    except TransactionCategory.DoesNotExist:
        return HttpResponseNotFound("<h1>Категория не найдена</h1>")


def SubCategoriesView(request):
    # Отображение подкатегорий и формы для добавления новых
    subcategories = Subcategory.objects.all()
    categories = TransactionCategory.objects.all()
    return render(request, "subcategories.html", {"categories": categories, "subcategories": subcategories})


def AddSubCategory(request):
    # Добавление новой подкатегории
    if request.method == "POST":
        subcategory = Subcategory()
        subcategory.SubCatName = request.POST.get("name")
        subcategory.Category = TransactionCategory.objects.get(CatName=request.POST.get("catName"))
        subcategory.save()
    return HttpResponseRedirect("/subcategories")


def DeleteSubCategory(request, id):
    # Удаление выбранной подкатегории
    try:
        subcategory = Subcategory.objects.get(id=id)
        subcategory.delete()
        return HttpResponseRedirect("/subcategories")
    except Subcategory.DoesNotExist:
        return HttpResponseNotFound("<h1>Подкатегория не найдена</h1>")


def EditSubCategory(request, id):
    # Изменение выбранной подкатегории
    try:
        subcategory = Subcategory.objects.get(id=id)
        categories = TransactionCategory.objects.all()
        if request.method == "POST":
            subcategory.SubCatName = request.POST.get("name")
            subcategory.Category = TransactionCategory.objects.get(CatName=request.POST.get("catName"))
            subcategory.save()
            return HttpResponseRedirect("/subcategories")
        else:
            return render(request, "SubCategoryEdit.html", {"subcategory": subcategory, "categories": categories})
    except Subcategory.DoesNotExist:
        return HttpResponseNotFound("<h1>Подкатегория не найдена</h1>")

