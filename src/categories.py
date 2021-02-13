categories = [
    '2020',
    'alternative',
    'at_home',
    # 'electro',
    'french_variety',
    'in_the_car',
    'hiphop',
    # 'latin',
    'party',
    'pop',
    'popculture',
    'reggae',
    'rnb',
    'romance',
    'rock',
    'toplists',
    'travel'
]


def translate(category_id: str) -> str:
    translation_map = {
        "2020": "2020",
        "alternative": "Alternatif",
        "at_home": "À la maison",
        "french_variety": "Variété française",
        "in_the_car": "Dans la voiture",
        "hiphop": "Hip-hop",
        "party": "En soirée",
        "pop": "Pop",
        "popculture": "Pop culture",
        "reggae": "Reggae",
        "rnb": "RNB",
        "romance": "Romantique",
        "rock": "Rock",
        "toplists": "Charts",
        "travel": "Voyage"
    }
    return translation_map[category_id]
