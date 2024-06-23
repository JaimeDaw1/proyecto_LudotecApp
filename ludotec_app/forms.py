from django import forms
from django.forms import ModelForm
from .models import Juego, Mecanica, Tematica, Partida, Jugador, Puntuacion, Feedback
from django.db import transaction
from django.contrib.auth.models import User


class JuegoForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class':'form-control'}))
    min_jugadores = forms.IntegerField(label="Mínimo de jugadores", widget=forms.NumberInput(attrs={'class':'form-control', 'min': 1}))
    max_jugadores = forms.IntegerField(label="Máximo de jugadores", widget=forms.NumberInput(attrs={'class':'form-control', 'min': 1}))
    duracion = forms.DurationField(label="Duración", initial="01:00", widget=forms.TextInput(attrs={'class':'form-control', 'id': 'id_duracion'}))
    dificultad = forms.DecimalField(label="Dificultad (de 1 a 5)", widget=forms.NumberInput(attrs={'class':'form-control', 'min': 1, 'max': 5}))
    año = forms.IntegerField(label="Año de lanzamiento", widget=forms.NumberInput(attrs={'class':'form-control', 'min': 1000}))
    precio = forms.DecimalField(label="Precio", widget=forms.NumberInput(attrs={'class':'form-control', 'min': 0}))
    imagen = forms.ImageField(label="Imagen", required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    descripcion = forms.CharField(label="Descripción", required=False, widget=forms.Textarea(attrs={'class':'form-control ancho', 'rows': 5}))



    class Meta:
        model = Juego
        fields = ['nombre', 'min_jugadores', 'max_jugadores', 'duracion', 'dificultad', 'año', 'precio', 'imagen', 'descripcion', 'mecanicas', 'tematicas']
        widgets = {
            'mecanicas': forms.CheckboxSelectMultiple(attrs={'id': 'id_mecanicas'}),
            'tematicas': forms.CheckboxSelectMultiple(attrs={'id': 'id_tematicas'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mecanicas'].required = False
        self.fields['tematicas'].required = False

        # Obtener todas las mecánicas y temáticas existentes
        all_mecanicas = Mecanica.objects.all()
        all_tematicas = Tematica.objects.all()

        # Crear checkboxes para las mecánicas existentes
        self.fields['mecanicas'].widget = forms.CheckboxSelectMultiple()
        self.fields['mecanicas'].queryset = all_mecanicas

        # Crear checkboxes para las temáticas existentes
        self.fields['tematicas'].widget = forms.CheckboxSelectMultiple()
        self.fields['tematicas'].queryset = all_tematicas

        # Agrega clases de Bootstrap a los checkboxes
        self.fields['mecanicas'].widget.attrs['class'] = 'form-check-input'
        self.fields['tematicas'].widget.attrs['class'] = 'form-check-input'


    
    def clean(self):
        cleaned_data = super().clean()
        nueva_mecanica = cleaned_data.get('nueva_mecanica')
        nueva_tematica = cleaned_data.get('nueva_tematica')

        mecanicas_seleccionadas = cleaned_data.get('mecanicas', [])
        tematicas_seleccionadas = cleaned_data.get('tematicas', [])

        if nueva_mecanica:
            mecanica_obj, _ = Mecanica.objects.get_or_create(nombre_mecanica=nueva_mecanica)
            cleaned_data['mecanicas'] = [mecanica_obj.id]  # Asignar solo el ID de la mecánica

        if nueva_tematica:
            tematica_obj, _ = Tematica.objects.get_or_create(nombre_tematica=nueva_tematica)
            cleaned_data['tematicas'] = [tematica_obj.id]  # Asignar solo el ID de la temática

        cleaned_data['mecanicas'] = mecanicas_seleccionadas
        cleaned_data['tematicas'] = tematicas_seleccionadas

        return cleaned_data
    


    def save(self, usuario=None, commit=True):
        juego = super().save(commit=False)

        if usuario:
            juego.usuario = usuario

        if commit:
            nueva_mecanica = self.cleaned_data.get('nueva_mecanica')
            nueva_tematica = self.cleaned_data.get('nueva_tematica')

            with transaction.atomic():
                if nueva_mecanica:
                    mecanica_obj, _ = Mecanica.objects.get_or_create(nombre_mecanica=nueva_mecanica)
                    mecanica_obj.save()  # Guardar la nueva mecánica en la base de datos
                    juego.mecanicas.add(mecanica_obj)

                if nueva_tematica:
                    tematica_obj, _ = Tematica.objects.get_or_create(nombre_tematica=nueva_tematica)
                    tematica_obj.save()  # Guardar la nueva temática en la base de datos
                    juego.tematicas.add(tematica_obj)

        juego.save()  # Guardar el juego en la base de datos
        self.save_m2m()

        return juego





class FilterForm(forms.Form):
    nombre = forms.CharField(label='Nombre del juego', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero_jugadores = forms.ChoiceField(choices=[('', '---')] + [(i, str(i)) for i in range(1, 13)], label="Número de Jugadores", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    CHOICES_DIFICULTAD = (
        ('', '---'),
        ('1_2', '<2 (Familiar)'),
        ('2_3', '≥2 y <3 (Dificultad Media)'),
        ('3_4', '≥3 y <4 (Dificultad Alta)'),
        ('4_5', '≥4 (Dificultad muy alta)'),
    )
    dificultad = forms.ChoiceField(choices=CHOICES_DIFICULTAD, label='Selecciona la dificultad', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    CHOICES_PRECIO = (
        ('', '---'),
        ('lt_20', '< 20€'),
        ('20_40', '≥ 20€ y < 40€'),
        ('40_60', '≥ 40€ y < 60€'),
        ('gt_60', '> 60€'),
    )
    precio = forms.ChoiceField(choices=CHOICES_PRECIO, label='Selecciona el rango de precio', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    año = forms.IntegerField(label='Selecciona un año', widget=forms.Select(choices=[('', '---')] + [(year, year) for year in range(1980, 2025)], attrs={'class': 'form-control'}), required=False)
    
    
    CHOICES_DURACION = (
        ('', '---'),
        ('lt_30', '≤ 30 min.'),
        ('30_60', '> 30 min. y ≤ 1 hora'),
        ('60_120', '> 1 hora y ≤ 2 horas'),
        ('gt_120', '> 2 horas'),
    )
    duracion = forms.ChoiceField(choices=CHOICES_DURACION, label='Duración', required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    mecanicas = forms.ModelMultipleChoiceField(queryset=Mecanica.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)
    tematicas = forms.ModelMultipleChoiceField(queryset=Tematica.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)


class PartidaForm(forms.ModelForm):
    juego = forms.ModelChoiceField(label="Juego", queryset=Juego.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    juego_externo = forms.CharField(label="Juego externo", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Campo para el juego personalizado
    jugadores = forms.CharField(label="Jugadores", widget=forms.TextInput(attrs={'class': 'form-control'}))
    puntuaciones = forms.CharField(label="Puntuaciones", widget=forms.Textarea(attrs={'class': 'form-control'}))  # Nuevo campo para puntuaciones
    duracion = forms.DurationField(label="Duración (horas/minutos)", initial="01:00", widget=forms.TextInput(attrs={'class': 'form-control'}))
    lugar = forms.CharField(label="Lugar", widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha = forms.DateField(label="Fecha de la partida", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    ganador = forms.CharField(label="Ganador", widget=forms.Select(attrs={'class': 'form-control'}), required=False)


    class Meta:
        model = Partida
        fields = ['juego', 'juego_externo', 'jugadores', 'puntuaciones', 'duracion', 'lugar', 'fecha', 'ganador']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['juego'].queryset = Juego.objects.filter(usuario=user)

        # Obtener jugadores para la lista desplegable de ganador
        jugadores_puntuaciones = self.initial.get('puntuaciones', '')
        jugadores_lista = self.initial.get('jugadores', '').split(',')
        if jugadores_puntuaciones and len(jugadores_lista) > 0:
            jugadores_puntuacion = dict(zip(jugadores_lista, jugadores_puntuaciones.split(',')))
            self.fields['ganador'].choices = [(jugador, jugador) for jugador in jugadores_puntuacion.keys()]

    def clean(self):
        cleaned_data = super().clean()
        juego_seleccionado = cleaned_data.get('juego')
        juego_personalizado = cleaned_data.get('juego_externo')

        if not juego_seleccionado and not juego_personalizado:
            raise forms.ValidationError("Debes seleccionar un juego existente o ingresar un juego personalizado.")

        if juego_personalizado and not juego_seleccionado:
            # Limpiar el campo de juego seleccionado si se ha proporcionado un juego personalizado
            cleaned_data['juego'] = None

        return cleaned_data

    def save(self, commit=True):
        partida = super().save(commit=False)
        juego = self.cleaned_data.get('juego')
        juego_externo = self.cleaned_data.get('juego_externo')

        if juego:
            partida.nombre_juego = juego.nombre
        elif juego_externo:
            partida.nombre_juego = juego_externo

        if commit:
            partida.usuario = self.user  # Asignar el usuario a la partida
            partida.save()

            jugadores_puntuaciones = self.cleaned_data.get('puntuaciones')
            jugadores_lista = self.cleaned_data.get('jugadores').split(',')
            puntuaciones_lista = jugadores_puntuaciones.split(',')

            ganador_seleccionado = self.cleaned_data.get('ganador')

            for nombre_jugador, puntuacion in zip(jugadores_lista, puntuaciones_lista):
                jugador, created = Jugador.objects.get_or_create(nombre=nombre_jugador, usuario=self.user)
                puntuacion_obj, created = Puntuacion.objects.get_or_create(jugador=jugador, partida=partida, usuario=self.user)
                puntuacion_obj.puntuacion = puntuacion

                # Marcar al jugador seleccionado como ganador
                if nombre_jugador == ganador_seleccionado:
                    puntuacion_obj.ganador = True
                else:
                    puntuacion_obj.ganador = False

                puntuacion_obj.save()

        return partida


class EstadisticasJugadorForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        jugadores = Jugador.objects.filter(usuario=user)
        jugadores_choices = [('', '---')] + [(jugador.nombre, jugador.nombre) for jugador in jugadores]
        self.fields['jugador'] = forms.ChoiceField(choices=jugadores_choices)

        juegos = Partida.objects.filter(usuario=user).values_list('nombre_juego', flat=True).distinct()
        juegos_choices = [('', '---')] + [(juego, juego) for juego in juegos]
        self.fields['juego'] = forms.ChoiceField(choices=juegos_choices)



class FeedbackForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre", required=False, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", required=False, widget=forms.EmailInput(attrs={'placeholder': 'Tu email', 'class': 'form-control'}))
    mensaje = forms.CharField(label="Propuesta de mejora", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Escribe tu propuesta de mejora aquí...', 'class': 'form-control'}))
    valoracion = forms.ChoiceField(label="Valoración de Ludotec-App", choices=[(str(i), '★' * i) for i in range(1, 6)], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Feedback
        fields = ['nombre', 'email', 'mensaje', 'valoracion']
