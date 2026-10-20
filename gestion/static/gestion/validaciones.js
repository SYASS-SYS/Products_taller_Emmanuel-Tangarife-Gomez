// Validaciones sencillas del navegador. Django vuelve a validar los datos en el servidor.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.validar-formulario').forEach(function (form) {
    form.querySelectorAll('input, select, textarea').forEach(function (campo) {
      if (campo.name === 'nit') campo.setAttribute('pattern', '[0-9.\\-]+');
      if (campo.name === 'telefono') campo.setAttribute('pattern', '[0-9+()\\- ]{7,30}');
      if (campo.name === 'valor_total') { campo.setAttribute('min', '0.01'); campo.setAttribute('step', '0.01'); }
      campo.addEventListener('input', function () { validarCampo(campo); });
      campo.addEventListener('change', function () { validarCampo(campo); });
    });
    form.addEventListener('submit', function (event) {
      let primeroInvalido = null;
      form.querySelectorAll('input, select, textarea').forEach(function (campo) {
        if (!validarCampo(campo) && !primeroInvalido) primeroInvalido = campo;
      });
      if (!form.checkValidity() || primeroInvalido) {
        event.preventDefault();
        if (primeroInvalido) primeroInvalido.focus();
      }
    });
  });
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!window.confirm(form.dataset.confirm || '¿Deseas continuar?')) event.preventDefault();
    });
  });
});
function validarCampo(campo) {
  const contenedor = campo.parentElement;
  const error = contenedor.querySelector('.js-error');
  if (!campo.willValidate) return true;
  campo.setCustomValidity('');
  if (campo.name === 'valor_total' && campo.value && Number(campo.value) <= 0) campo.setCustomValidity('El valor debe ser mayor que cero.');
  let mensaje = '';
  if (campo.validity.valueMissing) mensaje = 'Este campo es obligatorio.';
  else if (campo.validity.typeMismatch && campo.type === 'email') mensaje = 'Escribe un correo electrónico válido.';
  else if (campo.validity.patternMismatch && campo.name === 'nit') mensaje = 'Usa solo números, puntos o guion en el NIT.';
  else if (campo.validity.patternMismatch && campo.name === 'telefono') mensaje = 'Revisa el teléfono: usa números y caracteres permitidos.';
  else if (campo.validity.rangeUnderflow && campo.name === 'valor_total') mensaje = 'El valor debe ser mayor que cero.';
  else if (campo.validity.badInput) mensaje = 'Escribe un valor válido.';
  else if (campo.validity.customError) mensaje = campo.validationMessage;
  else if (campo.validity.tooLong) mensaje = 'El texto es demasiado largo.';
  const valido = campo.checkValidity();
  campo.classList.toggle('is-invalid', !valido);
  campo.classList.toggle('is-valid', valido && campo.value.trim() !== '');
  if (error) error.textContent = mensaje;
  return valido;
}
