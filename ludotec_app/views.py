from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import JuegoForm, FilterForm, Mecanica, Tematica, Juego, PartidaForm, Partida, Puntuacion, EstadisticasJugadorForm, FeedbackForm
from .models import Jugador, Juego, Partida, Puntuacion, Feedback
from django.db.models import Max
from django.db.models import Q
from django.db.models import Case, When, Value, CharField
from datetime import timedelta
from django.db.models import F
from django.db.models import Avg



def home(request):
    if request.method == 'POST' and request.POST.get('form_type') == 'feedback_form':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, 'Gracias por tu feedback!')
            return redirect('home')
    return render(request, 'ludotec_app/home.html')


@login_required(login_url='/usuarios/login/')
def add(request):
    feedback_form = FeedbackForm()
    if request.method == 'POST':
        if request.POST.get('form_type') == 'feedback_form':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Gracias por tu feedback!')
                return redirect('add')
            
            
        form = JuegoForm(request.POST, request.FILES)
        if form.is_valid():
            juego = form.save(usuario=request.user)  # Aquí se pasa el usuario actual al formulario
            nuevas_mecanicas = request.POST.getlist('nuevas_mecanicas')
            nuevas_tematicas = request.POST.getlist('nuevas_tematicas')
            juego.save()  # Guarda el juego en la base de datos para obtener un ID

            #Aquí se procesan y agregan las nuevas mecánicas y temáticas
            for nueva_mecanica in nuevas_mecanicas:
                mecanica_obj, _ = Mecanica.objects.get_or_create(nombre_mecanica=nueva_mecanica)
                juego.mecanicas.add(mecanica_obj)
            for nueva_tematica in nuevas_tematicas:
                tematica_obj, _ = Tematica.objects.get_or_create(nombre_tematica=nueva_tematica)
                juego.tematicas.add(tematica_obj)

            messages.success(request, 'Juego guardado correctamente')
            return redirect('home')  
        else:
            print(form.errors)
    else:
        form = JuegoForm()

    return render(request, 'ludotec_app/add.html', {'form': form})



@login_required(login_url='/usuarios/login/')
def query(request):
    feedback_form = FeedbackForm()
    form = FilterForm(request.POST or None)
    juegos = Juego.objects.filter(usuario=request.user)

    if request.method == 'POST':
        if request.POST.get('form_type') == 'feedback_form':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Gracias por tu feedback!')
                return redirect('query')
            

        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            numero_jugadores = form.cleaned_data.get('numero_jugadores')
            dificultad = form.cleaned_data.get('dificultad')
            precio = form.cleaned_data.get('precio')
            año = form.cleaned_data.get('año')
            duracion = form.cleaned_data.get('duracion')
            mecanicas = form.cleaned_data.get('mecanicas')
            tematicas = form.cleaned_data.get('tematicas')

            if nombre:
                juegos = juegos.filter(nombre__icontains=nombre)
            if numero_jugadores:
                juegos = juegos.filter(min_jugadores__lte=numero_jugadores, max_jugadores__gte=numero_jugadores)
            if dificultad:
                min_difficulty, max_difficulty = dificultad.split('_')
                juegos = juegos.filter(dificultad__gte=min_difficulty, dificultad__lt=max_difficulty)
            if precio:
                if precio == 'lt_20':
                    juegos = juegos.filter(precio__lt=20)
                elif precio == '20_40':
                    juegos = juegos.filter(precio__gte=20, precio__lt=40)
                elif precio == '40_60':
                    juegos = juegos.filter(precio__gte=40, precio__lt=60)
                elif precio == 'gt_60':
                    juegos = juegos.filter(precio__gte=60)
            if año:
                juegos = juegos.filter(año=año)
            if duracion:
                if duracion == 'lt_30':
                    juegos = juegos.filter(duracion__lte=timedelta(minutes=30))
                elif duracion == '30_60':
                    juegos = juegos.filter(duracion__gt=timedelta(minutes=30), duracion__lte=timedelta(hours=1))
                elif duracion == '60_120':
                    juegos = juegos.filter(duracion__gt=timedelta(hours=1), duracion__lte=timedelta(hours=2))
                elif duracion == 'gt_120':
                    juegos = juegos.filter(duracion__gt=timedelta(hours=2))
            if mecanicas:
                juegos = juegos.filter(mecanicas__in=mecanicas)
            if tematicas:
                juegos = juegos.filter(tematicas__in=tematicas)

            if not juegos:
                messages.warning(request, 'No se encontraron juegos que coincidan con los criterios de búsqueda')
            
            form = FilterForm() #Limpia los campos del formulario después de haber mostrado los juegos filtrados.

    return render(request, 'ludotec_app/query.html', {'form': form, 'juegos': juegos})



def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    
    if request.method == 'POST':
        if request.POST.get('form_type') == 'feedback_form':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Gracias por tu feedback!')
                return redirect('detalle_juego', juego_id=juego_id)
    
    return render(request, 'ludotec_app/detalle_juego.html', {'juego': juego})


def borrar_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)

    Partida.objects.filter(juego=juego).update(juego=None)
    juego.delete()

    return redirect('query')



@login_required(login_url='/usuarios/login/')
def register(request):
    feedback_form = FeedbackForm()

    if request.method == 'POST':
        if request.POST.get('form_type') == 'feedback_form':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Gracias por tu feedback!')
                return redirect('register')
            

        form = PartidaForm(request.user, request.POST)
        if form.is_valid():
            partida = form.save(commit=False)
            juego_externo = form.cleaned_data.get('juego_externo')
            jugadores = form.cleaned_data.get('jugadores')
            puntuaciones = form.cleaned_data.get('puntuaciones')
            ganador = form.cleaned_data.get('ganador')

            if juego_externo:
                partida.nombre_juego = juego_externo
            else:
                juego = form.cleaned_data.get('juego')
                if juego:
                    partida.nombre_juego = juego.nombre

            if jugadores and puntuaciones:
                jugadores_lista = jugadores.split(',')
                puntuaciones_lista = puntuaciones.split(',')

                if len(jugadores_lista) == len(puntuaciones_lista):
                    # Asignar el usuario a la partida
                    partida.usuario = request.user
                    partida.save()  

                    for nombre_jugador, puntuacion in zip(jugadores_lista, puntuaciones_lista):
                        jugadores = Jugador.objects.filter(nombre=nombre_jugador, usuario=request.user)
                        
                        if jugadores.exists():
                            jugador = jugadores.first()  # Selecciona el primer jugador si hay más de uno
                        else:
                            # Crea un nuevo jugador si no se encuentra ninguno con el nombre especificado
                            jugador = Jugador.objects.create(nombre=nombre_jugador, usuario=request.user)
                        
                        puntuacion_obj = Puntuacion(
                            jugador=jugador,
                            partida=partida,
                            puntuacion=puntuacion,
                            usuario=request.user,
                            ganador=(nombre_jugador == ganador)
                        )
                        puntuacion_obj.save()

                    messages.success(request, 'Partida guardada correctamente')
                    return redirect('home')
                else:
                    messages.error(request, 'Error: La cantidad de jugadores y puntuaciones no coincide.')
            else:
                messages.error(request, 'Error: No se encontraron jugadores o puntuaciones.')
    else:
        form = PartidaForm(request.user)
    return render(request, 'ludotec_app/register.html', {'form': form})



@login_required(login_url='/usuarios/login/')
def statistics(request):
    feedback_form = FeedbackForm()
    user = request.user
    jugadores_disponibles = Jugador.objects.filter(usuario=user)
    juegos_disponibles = Partida.objects.filter(usuario=user).values(juego_nombre=F('nombre_juego')).distinct().order_by('juego_nombre')

    if request.method == 'POST':
        if request.POST.get('form_type') == 'feedback_form':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Gracias por tu feedback!')
                return redirect('statistics')

        jugador_seleccionado_nombre = request.POST.get('jugador', None)
        juego_seleccionado_nombre = request.POST.get('juego', None)

        if jugador_seleccionado_nombre and juego_seleccionado_nombre:
            jugador_seleccionado = Jugador.objects.filter(nombre=jugador_seleccionado_nombre, usuario=user).first()
            partidas_jugador = Partida.objects.filter(jugadores=jugador_seleccionado, nombre_juego=juego_seleccionado_nombre, usuario=user)

            if jugador_seleccionado and partidas_jugador.exists():
                partidas_ganadas = []
                partidas_perdidas = []

                for partida in partidas_jugador:
                    puntuacion_jugador = Puntuacion.objects.filter(partida=partida, jugador=jugador_seleccionado).first()
                    if puntuacion_jugador.ganador:
                        partidas_ganadas.append(partida)
                    else:
                        partidas_perdidas.append(partida)

                puntuaciones_ganadas = Puntuacion.objects.filter(partida__in=partidas_ganadas, jugador=jugador_seleccionado)
                puntuaciones_perdidas = Puntuacion.objects.filter(partida__in=partidas_perdidas, jugador=jugador_seleccionado)

                form = EstadisticasJugadorForm(user, initial={'jugador': jugador_seleccionado_nombre, 'juego': juego_seleccionado_nombre})

                return render(request, 'ludotec_app/statistics.html', {
                    'form': form,
                    'victorias': len(partidas_ganadas),
                    'derrotas': len(partidas_perdidas),
                    'juegos_ganados': partidas_ganadas,
                    'juegos_perdidos': partidas_perdidas,
                    'puntuaciones_ganadas': puntuaciones_ganadas,
                    'puntuaciones_perdidas': puntuaciones_perdidas,
                    'nombre_jugador': jugador_seleccionado_nombre,
                    'nombre_juego': juego_seleccionado_nombre,
                    'juegos': juegos_disponibles,
                    'jugadores': jugadores_disponibles,
                    'juego_seleccionado_id': juego_seleccionado_nombre
                })
            else:
                return render(request, 'ludotec_app/statistics.html', {
                    'form': EstadisticasJugadorForm(),
                    'error_message': 'El jugador o el juego seleccionado no existen',
                    'juegos': juegos_disponibles,
                    'jugadores': jugadores_disponibles
                })

        elif jugador_seleccionado_nombre:
            jugador_seleccionado = Jugador.objects.filter(nombre=jugador_seleccionado_nombre, usuario=user).first()

            if jugador_seleccionado:
                partidas_jugador = Partida.objects.filter(jugadores=jugador_seleccionado, usuario=user)
                partidas_ganadas = []
                partidas_perdidas = []

                for partida in partidas_jugador:
                    puntuacion_jugador = Puntuacion.objects.filter(partida=partida, jugador=jugador_seleccionado).first()
                    if puntuacion_jugador.ganador:
                        partidas_ganadas.append(partida)
                    else:
                        partidas_perdidas.append(partida)

                puntuaciones_ganadas = Puntuacion.objects.filter(partida__in=partidas_ganadas, jugador=jugador_seleccionado)
                puntuaciones_perdidas = Puntuacion.objects.filter(partida__in=partidas_perdidas, jugador=jugador_seleccionado)

                form = EstadisticasJugadorForm(user, initial={'jugador': jugador_seleccionado_nombre})

                return render(request, 'ludotec_app/statistics.html', {
                    'form': form,
                    'victorias': len(partidas_ganadas),
                    'derrotas': len(partidas_perdidas),
                    'juegos_ganados': partidas_ganadas,
                    'juegos_perdidos': partidas_perdidas,
                    'puntuaciones_ganadas': puntuaciones_ganadas,
                    'puntuaciones_perdidas': puntuaciones_perdidas,
                    'nombre_jugador': jugador_seleccionado_nombre,
                    'juegos': juegos_disponibles,
                    'jugadores': jugadores_disponibles
                })
            else:
                return render(request, 'ludotec_app/statistics.html', {
                    'form': EstadisticasJugadorForm(user),
                    'error_message': 'El jugador seleccionado no existe',
                    'juegos': juegos_disponibles,
                    'jugadores': jugadores_disponibles
                })

        elif juego_seleccionado_nombre:
            partidas_juego = Partida.objects.filter(nombre_juego=juego_seleccionado_nombre, usuario=user)
            partidas_info = []

            for partida in partidas_juego:
                jugadores_partida = Puntuacion.objects.filter(partida=partida).select_related('jugador')
                jugadores_info = []
                for puntuacion in jugadores_partida:
                    jugadores_info.append({
                        'nombre': puntuacion.jugador.nombre,
                        'puntuacion': puntuacion.puntuacion,
                        'ganador': puntuacion.ganador
                    })
                partidas_info.append({'partida': partida, 'jugadores': jugadores_info})

            form = EstadisticasJugadorForm(user, initial={'juego': juego_seleccionado_nombre})

            return render(request, 'ludotec_app/statistics.html', {
                'form': form,
                'partidas_info': partidas_info,
                'nombre_juego': juego_seleccionado_nombre,
                'juegos': juegos_disponibles,
                'jugadores': jugadores_disponibles,
                'juego_seleccionado_id': juego_seleccionado_nombre
            })
        else:
            return render(request, 'ludotec_app/statistics.html', {
                'form': EstadisticasJugadorForm(user),
                'error_message': 'Seleccione un jugador y/o un juego',
                'juegos': juegos_disponibles,
                'jugadores': jugadores_disponibles
            })

    else:
        form = EstadisticasJugadorForm(user)
        return render(request, 'ludotec_app/statistics.html', {
            'form': form,
            'juegos': juegos_disponibles,
            'jugadores': jugadores_disponibles
        })


@login_required(login_url='/usuarios/login/')
def boardgame_statistic(request, juego_id):
    user = request.user
    juego = get_object_or_404(Juego, id=juego_id, usuario=user)  # Filtramos el juego por el usuario

    feedback_form = FeedbackForm()

    if request.method == 'POST' and request.POST.get('form_type') == 'feedback_form':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, 'Gracias por tu feedback!')
            return redirect('boardgame_statistic', juego_id=juego_id)
    else:
        feedback_form = FeedbackForm()

    # Filtramos las partidas por el juego y el usuario
    partidas_juego = Partida.objects.filter(juego=juego, usuario=user)
    partidas_info = []

    for partida in partidas_juego:
        puntuaciones = Puntuacion.objects.filter(partida=partida).select_related('jugador')
        if puntuaciones.exists():
            max_puntuacion = puntuaciones.aggregate(max_puntuacion=Max('puntuacion'))['max_puntuacion']
            jugadores_info = []

            for puntuacion in puntuaciones:
                jugadores_info.append({
                    'nombre': puntuacion.jugador.nombre,
                    'puntuacion': puntuacion.puntuacion,
                    'max_puntuacion': puntuacion.puntuacion == max_puntuacion
                })

            partidas_info.append({'partida': partida, 'jugadores': jugadores_info})

    return render(request, 'ludotec_app/boardgame_statistic.html', {
        'juego': juego,
        'partidas_info': partidas_info
    })
    



@login_required
@staff_member_required
def feedback(request):
    feedback_list = Feedback.objects.all().order_by('-timestamp')
    valoracion_media = Feedback.objects.aggregate(Avg('valoracion'))['valoracion__avg']
    if valoracion_media is None:
        valoracion_media = 0
    return render(request, 'ludotec_app/feedback.html', {
        'feedback_list': feedback_list,
        'valoracion_media': valoracion_media,
    })
    