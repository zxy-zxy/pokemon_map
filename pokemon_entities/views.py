import folium
import json

from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50))
    folium.Marker([lat, lon], tooltip=name, icon=icon).add_to(folium_map)


def build_pokemon_image_url(request, pokemon):
    image_url = 'http://{}/{}'.format(
        request.get_host().strip('/'),
        str(pokemon.image.url).strip('/')
    )

    return image_url


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.select_related()
    unique_pokemons_on_page = set()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:

        image_url = DEFAULT_IMAGE_URL
        if pokemon_entity.pokemon.image:
            image_url = build_pokemon_image_url(request, pokemon_entity.pokemon)

        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru,
            image_url,
        )
        unique_pokemons_on_page.add(pokemon_entity.pokemon)

    pokemons_on_page = [
        {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        }
        for pokemon in unique_pokemons_on_page
    ]

    return render(
        request,
        "mainpage.html",
        context={'map': folium_map._repr_html_(), 'pokemons': pokemons_on_page},
    )


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Pokemon not found</h1>')

    pokemon_entities = PokemonEntity.objects.filter(pokemon_id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:

        image_url = DEFAULT_IMAGE_URL
        if pokemon_entity.pokemon.image:
            image_url = build_pokemon_image_url(request, pokemon)

        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon.title_ru,
            image_url,
        )

    pokemon_repr = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
    }

    return render(
        request,
        "pokemon.html",
        context={'map': folium_map._repr_html_(), 'pokemon': pokemon_repr},
    )
