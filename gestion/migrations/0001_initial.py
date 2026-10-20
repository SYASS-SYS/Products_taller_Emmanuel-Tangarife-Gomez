# Initial database migration for CompraFácil.
import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=150, verbose_name='Nombre o razón social')),
                ('nit', models.CharField(max_length=30, unique=True, verbose_name='NIT')),
                ('nombre_contacto', models.CharField(max_length=120, verbose_name='Nombre del contacto')),
                ('telefono', models.CharField(max_length=30, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('direccion', models.CharField(max_length=220, verbose_name='Dirección')),
            ],
            options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores', 'ordering': ['razon_social']},
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_compra', models.CharField(max_length=40, unique=True, verbose_name='Número de compra')),
                ('fecha_compra', models.DateField(verbose_name='Fecha de compra')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Valor total')),
                ('estado', models.CharField(choices=[('registrada', 'Registrada'), ('recibida', 'Recibida'), ('cancelada', 'Cancelada')], default='registrada', max_length=15, verbose_name='Estado')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compras', to='gestion.proveedor', verbose_name='Proveedor')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compras', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={'verbose_name': 'Compra', 'verbose_name_plural': 'Compras', 'ordering': ['-fecha_compra', '-id']},
        ),
    ]
