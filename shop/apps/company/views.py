from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.core.mail import send_mail

from .forms import ContactsForm


class HomeView(TemplateView):
    """Цей клас представлення відповідає за показ користувачу головну сторінку"""

    template_name = 'company/home.html'


class ContactsView(CreateView):
    """Цей клас представлення відповідає за показ сторінку для збереження контактів"""

    template_name = 'company/contacts.html'
    form_class = ContactsForm
    success_url = reverse_lazy('company:Contacts')

    def form_valid(self, form):

        send_mail(
            'Thank for your subscribe', 'We will send you massages about our products',
            'oleksandr.hnylosyr@gmail.com', [form.cleaned_data['email']]
        )

        return super().form_valid(form)
