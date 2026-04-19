from django import forms
from django.contrib.auth.hashers import make_password, identify_hasher
from django.contrib import admin
from .models import (
    Usuarios,
    Perfiles,
    Materias,
    Examenes,
    Carreras,
    Carrera_Materia,
    Inscripcion_Examen,
    Inscripcion_Materia
    )

class UsuarioAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = Usuarios
        exclude = ['password_hash']

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm

    def save_model(self, request, obj, form, change):
        try:
            identify_hasher(obj.password)
        except:
            obj.password = make_password(obj.password)
        
        super().save_model(request, obj, form, change)

@admin.register(Perfiles)
class PerfilesAdmin(admin.ModelAdmin):
    list_display = ["id_perfil", "descripcion"]

admin.site.register(Materias)
admin.site.register(Examenes)
admin.site.register(Carreras)
admin.site.register(Carrera_Materia)
admin.site.register(Inscripcion_Examen)
admin.site.register(Inscripcion_Materia)
