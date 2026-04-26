from django.contrib.auth import hashers
from django.shortcuts import get_object_or_404, redirect, render

from .models import Carrera_Materia, Inscripcion_Materia, Materias, Usuarios, Carreras

carrera = Carreras.objects.get(id_carrera=2)

def login_valid(func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper


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

@login_valid
def alumno_controller(request):
    from datetime import datetime


    today = datetime.now()
    usuario = Usuarios.get(request.session.get('user_id'))
    carreras = Carreras.carreras_alumno(alumno=usuario)
    
    id_carrera = request.GET.get('carrera')

    if id_carrera:
        carrera = carreras.filter(id_carrera=id_carrera).first()

        materias_agrupadas = Materias.materias_alumnos_ord(
            cuatrimestre= 1 if today.month <= 6 else 2,
            carrera=carrera
        )
    else:
        materias_agrupadas = None

    inscripciones_alta = Inscripcion_Materia.id_materias_alta(usuario)
    
    return render(request, 'alumno.html',{
        'materias_agrupadas':materias_agrupadas,
        'inscriptas_alta': inscripciones_alta,
        'carreras':carreras,
        'carrera_seleccionada': id_carrera
    })

def toggle_inscripcion(request, materia_id):
    materia = get_object_or_404(Materias, id_materia=materia_id)
    usuario = Usuarios.get(id=request.session.get('user_id'))
    id_carrera = request.GET.get('carrera')

    Inscripcion_Materia.dar_alta_baja_Inscripcion_Materia(materia=materia, usuario=usuario)

    return redirect(f'/alumno?carrera={id_carrera}')

