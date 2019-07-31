from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def pokemon_directory_path(instance, filename):
    if filename:
        return 'pokemon/{0}/{1}'.format(instance.id, filename)


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Заголовок на русском')
    title_en = models.CharField(
        max_length=200, blank=True, verbose_name='Заголовок на английском'
    )
    title_jp = models.CharField(
        max_length=200, blank=True, verbose_name='Заголовок на японском'
    )
    image = models.ImageField(blank=True, null=True, upload_to=pokemon_directory_path)
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='Из кого эволюционировал',
    )
    next_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        verbose_name='В кого эволюционирует',
    )

    def __str__(self):
        return 'Title: {}'.format(self.title_ru)

    def __repr__(self):
        return self.__str__()


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities',
        verbose_name='Покемон',
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(80)],
        verbose_name='Уровень',
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Здоровье',
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Сила',
    )
    defense = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Защита',
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Выносливость',
    )

    def __str__(self):
        return 'Pokemon: {} with coordinates: {} {}'.format(
            self.pokemon, self.latitude, self.latitude
        )

    def __repr__(self):
        return self.__str__()
