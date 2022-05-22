level_list = list(['00-01', '02-03', '04-05', '06-07', '08', '09', '10',
                   '11-12', '13', '14', '15', '16', '17', '18', '19', 'e00', 'e01', 'e02',
                   'Adv_13', 'Adv_14', 'Adv_15', 'Adv_16', 'Adv_17', 'Adv_18'])


def input_to_category(category: str) -> str | None:

    if category is None:
        return None

    match category.lower():
        case 'inbounds' | 'i' | 'inbob': return 'Inbounds'
        case 'oob' | 'o': return 'Out_of_Bounds'
        case 'gless' | 'glitchless' | 'g': return 'Glitchless'
        case _: return None


def input_to_chamber(chamber: str) -> str | None:

    if chamber is None:
        return None

    chamber = chamber.replace('-', '').replace('/', '').replace('anced', '')

    if not chamber == '10':
        chamber = chamber.replace('0', '')

    match chamber.lower():
        case '' | '1': return level_list[0]
        case '23' | '2' | '3': return level_list[1]
        case '45' | '4' | '5': return level_list[2]
        case '67' | '6' | '7': return level_list[3]
        case '8': return level_list[4]
        case '9': return level_list[5]
        case '10': return level_list[6]
        case '1112' | '11' | '12': return level_list[7]
        case '13': return level_list[8]
        case '14': return level_list[9]
        case '15': return level_list[10]
        case '16': return level_list[11]
        case '17': return level_list[12]
        case '18': return level_list[13]
        case '19': return level_list[14]
        case 'e': return level_list[15]
        case 'e1': return level_list[16]
        case 'e2': return level_list[17]
        case 'adv13': return level_list[18]
        case 'adv14': return level_list[19]
        case 'adv15': return level_list[20]
        case 'adv16': return level_list[21]
        case 'adv17': return level_list[22]
        case 'adv18': return level_list[23]
        case _: return None
