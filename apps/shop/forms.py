
from copy import copy
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.contrib.formtools.wizard import FormWizard
from shop.models import Order

class AddCartForm(forms.Form):
	quantity = forms.IntegerField(min_value=1)

def get_add_cart_form(product):
	option_fields = {}
	for option in product.options():
		if len(option["choices"]) > 1:
			choices = zip(option["choices"], option["choices"])
			option_fields[option["name"]] = forms.ChoiceField(choices=choices)
	return type("AddCartFormProduct", (AddCartForm,), option_fields)

class OrderForm(forms.ModelForm):

	class Meta:
		model = Order
		exclude = ("shipping_type", "shipping", "total", "status")
	
	def _fieldset(self, prefix):
		other = prefix == "other"
		self._prefixes_done = getattr(self, "_prefixes_done", [])
		fieldset = copy(self)
		def is_fieldset_field(name):
			return (not other and name.startswith(prefix)) or (other and 
				not [done for done in self._prefixes_done if name.startswith(done)])
		fieldset.fields = SortedDict([field for field in self.fields.items() 
			if is_fieldset_field(field[0])])
		if not other:
			self._prefixes_done.append(prefix)
		return fieldset
	
	def __getattr__(self, name):
		if not name.startswith("fieldset_"):
			raise AttributeError, name
		return self._fieldset(name.split("fieldset_", 1)[1])

CARD_TYPE_CHOICES = ("Mastercard", "Visa", "Diners", "Amex")
CARD_TYPE_CHOICES = zip(CARD_TYPE_CHOICES, CARD_TYPE_CHOICES)
CARD_MONTHS = range(1, 12)
CARD_MONTHS = zip(CARD_MONTHS, CARD_MONTHS)
CARD_YEARS = ("2009", "2010")
CARD_YEARS = zip(CARD_YEARS, CARD_YEARS)

class PaymentForm(forms.Form):
	
	card_name = forms.CharField()
	card_type = forms.ChoiceField(choices=CARD_TYPE_CHOICES)
	card_number = forms.CharField()
	card_expiry_month = forms.ChoiceField(choices=CARD_MONTHS)
	card_expiry_year = forms.ChoiceField(choices=CARD_YEARS)
	card_ccv = forms.CharField()

class CheckoutWizard(FormWizard):

	def get_template(self, step):
		return "shop/%s.html" % ("billing_shipping", "payment")[int(step)]

	def done(self, request, form_list):
		return HttpResponseRedirect(reverse("shop_complete"))

checkout_wizard = CheckoutWizard([OrderForm, PaymentForm])