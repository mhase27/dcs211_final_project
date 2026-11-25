# Fetching PokeAPI
# Author: Maxi Hase, Nov 24, 2026
# Source: https://pokeapi.co/ (homepage), https://pokeapi.co/v2/openapi/operations/pokemon_retrieve (documentation), 
# https://pokeapi.co/api/v2/pokemon/{pokedex_number} (JSON dictionary for a specific Pokemon, where you replace {pokedex_number})
# This code serves to convert the PokeAPI to a CSV file, that I can then use to correct the dataset
# that I use for my final project. I will focus on stats, types, height, and weight, as these are relevant to my 
# data analysis

import requests
import numpy as np
import time
import pandas as pd


def fetchPokemon(pkdx: int) -> dict:
    '''Requests one Pokémon's data from PokéAPI
    Parameters:
    pkdx: the Pokémon's pokédex number
    Returns:
    the JSON response as a dictionary'''
    url = f"https://pokeapi.co/api/v2/pokemon/{pkdx}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def extractValues(json_dict: dict) -> dict:
    '''Builds a smaller dictionary with the wanted keys and entries for a given Pokémon
    Parameters:
        json_dict: the JSON dictionary for a given Pokemon
    Returns:
        a smaller dictionary for the given Pokémon'''
    # initializing dictionary
    pkmn_dict = {'pokedex_number': json_dict['id'], 'api_name': json_dict['name']}
    # creating a dictionary to match the stat names to the other CSV file
    stat_cols = {
        'hp': 'hp',
        'attack': 'attack',
        'defense': 'defense',
        'special-attack': 'sp_attack',
        'special-defense': 'sp_defense',
        'speed': 'speed'
    }
    # creating an entry for each stat individually
    for entry in json_dict['stats']:
        stat_name = entry['stat']['name']
        new_entry = stat_cols[stat_name]
        pkmn_dict[new_entry] = entry['base_stat']
    # converting height and weight to the right units, and adding to dictionary
    pkmn_dict['height_m'] = json_dict['height']/10
    pkmn_dict['weight_kg'] = json_dict['weight']/10
    # adding types to dictionary
    pkmn_dict['type2'] = np.nan
    for entry in json_dict['types']:
        type_no = entry['slot']
        type_name = f"type{type_no}"
        pk_type = entry['type']['name']
        pkmn_dict[type_name] = pk_type
    return pkmn_dict


def main() -> None:
    # initiating a list to turn into a dataframe
    pokeapi_csv = []
    # appending each dictionary for every pokemon
    for pkdx in range(1,802):
        try:
            json_dict = fetchPokemon(pkdx)
            pkmn_dict = extractValues(json_dict)
            pokeapi_csv.append(pkmn_dict)
        except requests.exceptions.RequestException as error:
            print(f"Failed on #{pkdx}: {error}")
        # adding a few prints to indicate that the program is indeed running
        if pkdx%50 == 0:
            print(f"Fetched {pkdx} out of 801")
        time.sleep(0.2)
    # turning the api into a dataframe, and saving the dataframe as a csv file
    pokeapi_df = pd.DataFrame(pokeapi_csv)
    pokeapi_df.to_csv('data/pokeapi.csv', index=False)

if __name__=='__main__':
    main()