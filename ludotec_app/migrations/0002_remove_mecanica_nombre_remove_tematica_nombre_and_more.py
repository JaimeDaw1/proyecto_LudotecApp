# Generated by Django 5.0.2 on 2024-03-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludotec_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mecanica',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='tematica',
            name='nombre',
        ),
        migrations.AddField(
            model_name='mecanica',
            name='nombre_mecanica',
            field=models.CharField(choices=[('push_your_luck', 'Push Your Luck'), ('gestion_de_mano', 'Gestión de mano'), ('deckbuilding', 'Deckbuilding'), ('colocacion_de_trabajadores', 'Colocación de Trabajadores'), ('colocacion_de_losetas', 'Colocación de losetas'), ('roll_and_write', 'Roll & Write'), ('draft', 'Draft'), ('control_de_area', 'Control de área'), ('card_driven', 'Card Driven'), ('apuestas', 'Apuestas'), ('subastas', 'Subastas'), ('faroleo', 'Faroleo'), ('economico', 'Económico'), ('comercio/negociacion', 'Comercio/Negociación'), ('cooperativo', 'Cooperativo'), ('solitario', 'Solitario'), ('roles_ocultos', 'Roles ocultos'), ('deduccion', 'Deducción'), ('bazas', 'Bazas'), ('carrera', 'Carrera'), ('set_collection', 'Set Collection'), ('flicking', 'Flicking'), ('destreza', 'Destreza'), ('tiempo_real', 'Tiempo real'), ('memoria', 'Memoria'), ('dibujo', 'Dibujo')], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tematica',
            name='nombre_tematica',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]
