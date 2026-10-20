import re
from django import forms
from .models import Proveedor, Compra

class FormularioBonito(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('placeholder', field.label)

class ProveedorForm(FormularioBonito):
    class Meta:
        model = Proveedor
        fields = ['razon_social', 'nit', 'nombre_contacto', 'telefono', 'correo', 'direccion']
        widgets = {'direccion': forms.TextInput(attrs={'maxlength': 220})}

    def clean_nit(self):
        nit = self.cleaned_data['nit'].strip()
        if not re.fullmatch(r'[0-9.\-]+', nit):
            raise forms.ValidationError('Usa únicamente números, puntos o guion en el NIT.')
        return nit

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        if not re.fullmatch(r'[0-9+()\- ]{7,30}', telefono):
            raise forms.ValidationError('Escribe un teléfono válido (números, espacios, +, paréntesis o guion).')
        return telefono

class CompraForm(FormularioBonito):
    class Meta:
        model = Compra
        fields = ['numero_compra', 'proveedor', 'fecha_compra', 'descripcion', 'valor_total', 'estado']
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'valor_total': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
            'estado': forms.Select(),
        }

    def clean_numero_compra(self):
        numero = self.cleaned_data['numero_compra'].strip()
        if not numero:
            raise forms.ValidationError('El número de compra es obligatorio.')
        return numero

    def clean_valor_total(self):
        valor = self.cleaned_data['valor_total']
        if valor <= 0:
            raise forms.ValidationError('El valor total debe ser mayor que cero.')
        return valor
