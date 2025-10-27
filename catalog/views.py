from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Главная'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Skystore'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'includes/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Автоматически привязываем продукт к текущему пользователю"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание продукта - Skystore'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'includes/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверяем, что пользователь - владелец продукта"""
        product = self.get_object()

        if product.owner != request.user and not request.user.has_perm('catalog.can_change_product_status'):
            raise PermissionDenied("У вас нет прав для редактирования этого продукта")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование {self.object.name} - Skystore'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'includes/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        """Проверяем, что пользователь - владелец или модератор"""
        product = self.get_object()

        if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("У вас нет прав для удаления этого продукта")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление {self.object.name} - Skystore'
        return context


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    fields = []
    template_name = 'includes/product_unpublish_confirm.html'
    permission_required = 'catalog.can_unpublish_product'

    def form_valid(self, form):
        self.object.status = 'draft'
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Отмена публикации {self.object.name} - Skystore'
        return context


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты - Skystore'
        return context