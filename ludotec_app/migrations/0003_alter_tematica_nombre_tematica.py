# Generated by Django 5.0.2 on 2024-03-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludotec_app', '0002_remove_mecanica_nombre_remove_tematica_nombre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tematica',
            name='nombre_tematica',
            field=models.CharField(choices=[('animales', 'Animales'), ('aventuras_exploracion', 'Aventuras y exploración'), ('deportes', 'Deportes'), ('abstracto', 'Abstracto'), ('agricultura', 'Agricultura'), ('arte/literatura', 'Arte/Literatura'), ('carreras', 'Carreras'), ('ciencia_ficcion', 'Ciencia Ficción'), ('civilizaciones', 'Civilizaciones'), ('comercio', 'Comercio'), ('construccion_ciudades', 'Construcción de ciudades'), ('misterio', 'Misterio'), ('comida/bebida', 'Comidas/Bebidas'), ('fantasia', 'Fantasía'), ('familiar', 'Familiar'), ('guerra', 'Guerra'), ('historia', 'Historia'), ('medicina', 'Medicina'), ('medieval', 'Medieval'), ('naturaleza', 'Naturaleza'), ('oeste', 'Oeste'), ('oriental', 'Oriental'), ('party', 'Party'), ('piratas', 'Piratas'), ('politica', 'Política'), ('terror', 'Terror'), ('trenes', 'Trenes'), ('tv/series/cine', 'Tv/Series/Cine'), ('zombies', 'Zombies')], max_length=100),
        ),
    ]