from django import forms
from .models import Equipment

class BorrowingForm(forms.Form):
    name = forms.ChoiceField(choices=[])
    parcel_id = forms.ChoiceField(choices=[])
    brand = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(BorrowingForm, self).__init__(*args, **kwargs)
        
        products = Equipment.objects.filter(status=False)
        
        # Create choices for name, id, and brand
        name_choices = [(product.equipment_id, product.name) for product in products]
        id_choices = [(product.equipment_id, product.parcel_id) for product in products]
        brand_choices = [(product.equipment_id, product.brand) for product in products]

        default_choice = [('', 'Select')]

        # Set choices for the form fields with the default option
        self.fields['name'].choices = default_choice + name_choices
        self.fields['parcel_id'].choices = default_choice + id_choices
        self.fields['brand'].choices = default_choice + brand_choices