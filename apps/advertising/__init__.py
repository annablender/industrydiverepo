import random

ADS = [
    {
        'company_name': 'Fast Banana',
        'copy': 'get your bananas fast!',
        'logo': 'fastbanana.png',
        'url': 'https://www.logolynx.com/topic/fake+company',
    },
    {
        'company_name': 'SpaceCube',
        'copy': 'space for your cubes!',
        'logo': 'spacecube.png',
        'url': 'https://www.logolynx.com/topic/fake+company',
    },
    {
        'company_name': 'Cyberdyne Systems',
        'copy': "it's not self aware, yet!",
        'logo': 'cyberdyne.jpeg',
        'url': 'https://www.logolynx.com/topic/fake+company',
    },
    {
        'company_name': 'Weyland-Yutani Corp',
        'copy': 'Out of this world job opportunities!',
        'logo': 'weyland.png',
        'url': 'https://www.logolynx.com/topic/fake+company',
    },
    {
        'company_name': 'Industry Dive',
        'copy': 'Want to read more great stories? Sign up for a newsletter!',
        'logo': 'industry-dive.png',
        'url': 'https://industrydive.com',
    },
]


def get_ad():
    return random.choice(ADS)
