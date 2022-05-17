level_list = list(['00-01', '02-03', '04-05', '06-07', '08', '09', '10',
                   '11-12', '13', '14', '15', '16', '17', '18', '19', 'e00', 'e01', 'e02',
                   'Adv_13', 'Adv_14', 'Adv_15', 'Adv_16', 'Adv_17', 'Adv_18'])


def input_to_category(category: str) -> str | None:
    match category.lower():
        case 'inbounds' | 'i': return 'Inbounds'
        case 'oob' | 'o': return 'Out_of_Bounds'
        case 'gless' | 'glitchless' | 'g': return 'Glitchless'
        case _: return None


def input_to_chamber(chamber: str) -> str | None:
    chamber_wanted = chamber.lower().replace('/', '-').replace('adv', 'adv_')
    return chamber_wanted if level_list.__contains__(chamber_wanted) else None
