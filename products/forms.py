from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label="Product name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. Wireless Mouse",
                "autocomplete": "off",
                "class": "input",
            }
        ),
    )
    price = forms.DecimalField(
        min_value=0,
        max_digits=12,
        decimal_places=2,
        label="Price",
        widget=forms.NumberInput(
            attrs={"placeholder": "0.00", "step": "0.01", "class": "input"}
        ),
    )
    quantity = forms.IntegerField(
        min_value=0,
        label="Quantity",
        widget=forms.NumberInput(
            attrs={"placeholder": "0", "min": "0", "class": "input"}
        ),
    )
    image = forms.ImageField(
        required=False,
        label="Product image",
        widget=forms.ClearableFileInput(
            attrs={"accept": "image/*", "class": "input input-file"}
        ),
    )
