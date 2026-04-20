from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import (
    Carrera_Materia,
    Carreras,
    Examenes,
    Inscripcion_Examen,
    Inscripcion_Materia,
    Materias,
    Perfiles,
    Usuarios,
)


class UsuarioAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = Usuarios
        exclude = ('password_hash',)

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = ("nombre", "apellido", "id_perfil")

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')

        if password:
            obj.password_hash = make_password(password)
        super().save_model(request, obj, form, change)

@admin.register(Perfiles)
class PerfilesAdmin(admin.ModelAdmin):
    list_display = ("id_perfil", "descripcion")

@admin.register(Materias)
class MateriasAdmin(admin.ModelAdmin):
    list_display= ("nombre", "anio", "cuatrimestre")

admin.site.register(Examenes)
admin.site.register(Carreras)
admin.site.register(Carrera_Materia)
admin.site.register(Inscripcion_Examen)
admin.site.register(Inscripcion_Materia)
