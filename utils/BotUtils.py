category_list = ["Inbounds", "Out_of_Bounds", "Glitchless"]
level_list = ["00-01", "02-03", "04-05", "06-07", "08", "09", "10",
              "11-12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02",
              "Adv_13", "Adv_14", "Adv_15", "Adv_16", "Adv_17", "Adv_18"]


def input_to_category(category):
    """Takes input and converts it to correctly formatted category name"""

    match category.lower():
        case 'inbounds' | 'i': return 'Inbounds'
        case 'oob' | 'o': return 'Out_of_Bounds'
        case 'gless' | 'glitchless' | 'g': return 'Glitchless'
        case _: return None


def input_to_chamber(chamber):
    return chamber.replace('/', '-')


def convert_to_ticks(millis: int):
    return round(millis / 15)


def convert_to_human_time(ticks: int):
    ms = int(ticks) * 15
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}.{int(ms):03d}'
