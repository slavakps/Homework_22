from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для продуктов с валидацией запрещенных слов и цены"""

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """Инициализация формы с добавлением CSS-классов"""
        super().__init__(*args, **kwargs)
        self._add_form_control_class()

    def _add_form_control_class(self):
        """Добавляет CSS-классы ко всем полям"""
        # Общие атрибуты для текстовых полей
        text_fields = ['name', 'description', 'price']
        for field_name in text_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Введите {self.fields[field_name].label.lower()}...'
                })

        # Специальные настройки для отдельных полей
        if 'description' in self.fields:
            self.fields['description'].widget.attrs.update({'rows': 4})

        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update({
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            })

        if 'category' in self.fields:
            self.fields['category'].widget.attrs.update({
                'class': 'form-select'
            })

        if 'image' in self.fields:
            self.fields['image'].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data['name']
        self._check_forbidden_words(name, 'названии')
        return name

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data['description']
        self._check_forbidden_words(description, 'описании')
        return description

    def clean_price(self):
        """Валидация цены продукта - не может быть отрицательной"""
        price = self.cleaned_data['price']

        if price is not None and price < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной!')

        if price == 0:
            raise forms.ValidationError('Цена продукта не может быть нулевой!')

        return price

    def _check_forbidden_words(self, text, field_name):
        """Проверка на наличие запрещенных слов"""
        if text:
            text_lower = text.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in text_lower:
                    raise forms.ValidationError(
                        f'Запрещенное слово "{word}" в {field_name} продукта!'
                    )
        return text