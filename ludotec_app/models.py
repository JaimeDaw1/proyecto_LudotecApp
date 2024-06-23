from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Mecanica(models.Model):
    nombre_mecanica = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_mecanica
    
     
class Tematica(models.Model):
    nombre_tematica = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tematica
    

class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    min_jugadores = models.IntegerField(validators=[MinValueValidator(1)])
    max_jugadores = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    duracion = models.DurationField()
    dificultad = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    año = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)])
    precio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    mecanicas = models.ManyToManyField('Mecanica')
    tematicas = models.ManyToManyField('Tematica')
    imagen = models.ImageField(upload_to='media/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


    
    def __str__(self):
        return f'{self.nombre}'


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario


    def __str__(self):
        return self.nombre


class Partida(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.SET_NULL, null=True) 
    juego_externo = models.CharField(max_length=100, blank=True, null=True)  # Campo para almacenar el nombre del juego
    jugadores = models.ManyToManyField(Jugador, through='Puntuacion')
    duracion = models.DurationField()
    lugar = models.CharField(max_length=100)
    fecha = models.DateField()
    nombre_juego = models.CharField(max_length=100, blank=True, null=True)  # Campo para almacenar el nombre del juego
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario


    def __str__(self):
        return f'{self.juego}'

    def save(self, *args, **kwargs):
        # Si se proporciona un nombre de juego personalizado y no se selecciona uno de la lista desplegable,
        # se establece el campo 'juego' en None y se utiliza el nombre_juego proporcionado
        if self.nombre_juego and not self.juego_id:
            self.juego = None
        
        # Actualizar automáticamente el nombre del juego si está relacionado
        if self.juego:
            self.nombre_juego = self.juego.nombre

        super().save(*args, **kwargs)


class Puntuacion(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que registra la puntuación
    ganador = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.jugador} - {self.partida} - {self.puntuacion}"

    def clean(self):
        # Validar que el usuario que registra la puntuación sea el mismo que el usuario de la partida
        if self.partida.usuario != self.usuario:
            raise ValidationError("El usuario que registra la puntuación no coincide con el usuario de la partida.")

    def save(self, *args, **kwargs):
        self.clean()  # Ejecutar validación antes de guardar
        super().save(*args, **kwargs)
    

class Feedback(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mensaje = models.TextField()
    valoracion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default = 1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nombre = self.nombre if self.nombre else "Anónimo"
        email = f"Email: {self.email}" if self.email else "Sin email"
        return f"Nombre: {nombre}, Valoración: {self.valoracion}, {email}, Mensaje: {self.mensaje[:50]}..."
    

    
   



