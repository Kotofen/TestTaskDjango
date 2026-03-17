# forms.py
from django import forms
from .models import Transaction, TransactionCategory, Subcategory, TransactionStatus, TransactionType


class TransactionForm(forms.ModelForm):
    # Форма для добавления новых ДДС
    class Meta:
        model = Transaction
        fields = "__all__"
        widgets = {
            "TransactionDate": forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
            "Type": forms.Select(attrs={"required": True}),
            "Category": forms.Select(attrs={"required": True}),
            "Subcategory": forms.Select(attrs={"required": True}),
            "TransactionSumm": forms.NumberInput(attrs={"required": True, "min": "1"})
        }

    def clean(self):
        # Валидация данных
        cleaned_data = super().clean()

        # Поля которые валидируются
        type_field = cleaned_data.get("Type")
        category = cleaned_data.get("Category")
        subcategory = cleaned_data.get("Subcategory")
        summ = cleaned_data.get("TransactionSumm")

        # Проверка отсутствия необходимых для добавления данных
        if not type_field:
            self.add_error("Type", "Выберите тип транзакции")

        if not category:
            self.add_error("Category", "Выберите категорию")

        if not subcategory:
            self.add_error("Subcategory", "Выберите подкатегорию")

        if summ is None:
            self.add_error("TransactionSumm", "Введите сумму")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["Category"].queryset = TransactionCategory.objects.none()
        self.fields["Subcategory"].queryset = Subcategory.objects.none()

        # Динамическая подгрузка подходящих категорий на основе выбранного типа
        if "Type" in self.data:
            try:
                type_id = int(self.data.get("Type"))
                self.fields["Category"].queryset = TransactionCategory.objects.filter(Type_id=type_id)
            except (ValueError, TypeError):
                pass

        # Динамическая подгрузка подходящих подкатегорий на основе выбранной категории
        if "Category" in self.data:
            try:
                cat_id = int(self.data.get("Category"))
                self.fields["Subcategory"].queryset = Subcategory.objects.filter(Category_id=cat_id)
            except (ValueError, TypeError):
                pass

        # Подгрузка данных о подходящих категориях и подкатегориях во время редактирования
        if self.instance.pk:
            self.fields["Category"].queryset = TransactionCategory.objects.filter(
                Type=self.instance.Type
            )

            self.fields["Subcategory"].queryset = Subcategory.objects.filter(
                Category=self.instance.Category
            )


class TransactionFilterForm(forms.Form):
    # Форма для фильтрации данных о ДДС
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ModelChoiceField(queryset=TransactionStatus.objects.all(), required=False)
    type = forms.ModelChoiceField(queryset=TransactionType.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=TransactionCategory.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False)