from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProveedorForm, CompraForm
from .models import Proveedor, Compra

@login_required
def inicio(request):
    return render(request, 'gestion/inicio.html', {
        'total_proveedores': Proveedor.objects.count(),
        'total_compras': Compra.objects.count(),
        'compras_recientes': Compra.objects.select_related('proveedor', 'usuario')[:5],
    })

@login_required
def proveedores_lista(request):
    busqueda = request.GET.get('q', '').strip()
    proveedores = Proveedor.objects.all()
    if busqueda:
        proveedores = proveedores.filter(Q(razon_social__icontains=busqueda) | Q(nit__icontains=busqueda))
    return render(request, 'gestion/proveedores_lista.html', {'proveedores': proveedores, 'busqueda': busqueda})

@login_required
def proveedor_detalle(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'gestion/proveedor_detalle.html', {'proveedor': proveedor, 'compras': proveedor.compras.select_related('usuario')})

@login_required
def proveedor_crear(request):
    form = ProveedorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        proveedor = form.save()
        messages.success(request, 'Proveedor registrado correctamente.')
        return redirect('proveedor_detalle', pk=proveedor.pk)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Nuevo proveedor', 'volver': 'proveedores_lista'})

@login_required
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Proveedor actualizado correctamente.')
        return redirect('proveedor_detalle', pk=proveedor.pk)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Editar proveedor', 'volver': 'proveedor_detalle', 'volver_pk': pk})

@login_required
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        try:
            proveedor.delete()
            messages.success(request, 'Proveedor eliminado.')
        except ProtectedError:
            messages.error(request, 'No puedes eliminar este proveedor porque tiene compras asociadas.')
        return redirect('proveedores_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': proveedor, 'tipo': 'proveedor', 'volver': 'proveedor_detalle', 'volver_pk': pk})

@login_required
def compras_lista(request):
    compras = Compra.objects.select_related('proveedor', 'usuario')
    estado = request.GET.get('estado', '')
    proveedor_id = request.GET.get('proveedor', '')
    if estado in dict(Compra.ESTADOS):
        compras = compras.filter(estado=estado)
    else:
        estado = ''
    if proveedor_id.isdigit():
        compras = compras.filter(proveedor_id=int(proveedor_id))
    else:
        proveedor_id = ''
    return render(request, 'gestion/compras_lista.html', {
        'compras': compras, 'estados': Compra.ESTADOS, 'estado_seleccionado': estado,
        'proveedores': Proveedor.objects.all(), 'proveedor_seleccionado': proveedor_id,
    })

@login_required
def compra_crear(request):
    form = CompraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        compra = form.save(commit=False)
        compra.usuario = request.user
        compra.save()
        messages.success(request, 'Compra registrada correctamente.')
        return redirect('compra_detalle', pk=compra.pk)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Nueva compra', 'volver': 'compras_lista'})

@login_required
def compra_detalle(request, pk):
    compra = get_object_or_404(Compra.objects.select_related('proveedor', 'usuario'), pk=pk)
    return render(request, 'gestion/compra_detalle.html', {'compra': compra})

@login_required
def compra_editar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    form = CompraForm(request.POST or None, instance=compra)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Compra actualizada correctamente.')
        return redirect('compra_detalle', pk=compra.pk)
    return render(request, 'gestion/formulario.html', {'form': form, 'titulo': 'Editar compra', 'volver': 'compra_detalle', 'volver_pk': pk})

@login_required
def compra_eliminar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada.')
        return redirect('compras_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': compra, 'tipo': 'compra', 'volver': 'compra_detalle', 'volver_pk': pk})
