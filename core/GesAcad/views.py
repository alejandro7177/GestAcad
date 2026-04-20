from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404, redirect, render

from .models import Inscripcion_Materia, Materias, Usuarios


def login_controler(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Usuarios.objects.get(email=username)

            if hashers.check_password(password, user.password_hash):
                request.session['user_id'] = user.id_usuario
                request.session['perfil_id'] = user.id_perfil.__str__()
                return redirect("alumno")
            else:
                return render(request, 'login.html', {'error':'Credecinales Incorrectas!'})
            
        except Usuarios.DoesNotExist:
            return render(request, 'login.html', {'error':'El usuario no existe!'})
    return render(request, 'login.html')

def alumno_controller(request):
    from datetime import datetime
    from itertools import groupby


    today = datetime.now()
    if today.month <= 6:
        cuatrimestre = 1
    else:
        cuatrimestre = 2

    materias = Materias.objects.filter(cuatrimestre=1).order_by("anio", "cuatrimestre", "nombre")
    user_id = request.session.get('user_id')
    inscripciones =Inscripcion_Materia.objects.filter(id_usuario=user_id, estado="Alta")

    incripciones_id = list(inscripciones.values_list("id_materia", flat=True))

    materias_agrupadas = {}
    for anio, grupo in groupby(materias, key=lambda x:x.anio):
        materias_agrupadas[anio] = list(grupo)
    materias_agrupadas = list(materias_agrupadas.items())
    print(f"{materias_agrupadas=}")
    if 'user_id' not in request.session:
        return redirect('login')
    return render(request, 'alumno.html',{
        'materias_agrupadas':materias_agrupadas,
        'inscriptas_alta': incripciones_id
    })

def toggle_inscripcion(request, materia_id):
    materia = get_object_or_404(Materias, id_materia=materia_id)
    user_id = request.session.get('user_id')
    user = Usuarios.objects.filter(id_usuario=user_id).first()

    insc, created = Inscripcion_Materia.objects.get_or_create(
        id_usuario = user,
        id_materia = materia,
        defaults={"estado":"Alta"}
    )

    if not created:
        if insc.estado == "Alta":
            insc.estado = "Baja"
        else:
            insc.estado = "Alta"
        insc.save()

    return redirect('alumno')

