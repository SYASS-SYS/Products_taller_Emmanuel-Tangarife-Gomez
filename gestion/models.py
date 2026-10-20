from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class Proveedor(models.Model):
    razon_social = models.CharField('Nombre o razón social', max_length=150)
    nit = models.CharField('NIT', max_length=30, unique=True)
    nombre_contacto = models.CharField('Nombre del contacto', max_length=120)
    telefono = models.CharField('Teléfono', max_length=30)
    correo = models.EmailField('Correo electrónico')
    direccion = models.CharField('Dirección', max_length=220)

    class Meta:
        ordering = ['razon_social']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f'{self.razon_social} ({self.nit})'

class Compra(models.Model):
    ESTADOS = [
        ('registrada', 'Registrada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    numero_compra = models.CharField('Número de compra', max_length=40, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='compras', verbose_name='Proveedor')
    fecha_compra = models.DateField('Fecha de compra')
    descripcion = models.TextField('Descripción')
    valor_total = models.DecimalField('Valor total', max_digits=14, decimal_places=2, validators=[MinValueValidator(0.01)])
    estado = models.CharField('Estado', max_length=15, choices=ESTADOS, default='registrada')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='compras', verbose_name='Usuario')

    class Meta:
        ordering = ['-fecha_compra', '-id']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'{self.numero_compra} - {self.proveedor.razon_social}'
