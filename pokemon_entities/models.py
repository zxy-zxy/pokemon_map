from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def pokemon_directory_path(instance, filename):
    if filename:
        return 'pokemon/{0}/{1}'.format(instance.id, filename)


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_jp = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=pokemon_directory_path)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Title: {}'.format(self.title_ru)

    def __repr__(self):
        return self.__str__()


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name='pokemon_entities'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(80)]
    )
    health = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    strength = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    defense = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    stamina = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    def __str__(self):
        return 'Pokemon: {} with coordinates: {} {}'.format(
            self.pokemon, self.latitude, self.latitude
        )

    def __repr__(self):
        return self.__str__()
