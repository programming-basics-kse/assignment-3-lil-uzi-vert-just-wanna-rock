import argparse
from typing import override

MEDALISTS = 10

def parser_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Medalists database processing program')
    parser.add_argument('input_file', help='Data file address')
    parser.add_argument('-medals', nargs=2, metavar=('COUNTRY', 'YEAR'), help='The top ten medalists from this country at a given Olympiad')
    parser.add_argument('-total', type=int, metavar='NAME', help='The total number of medals in the year')
    parser.add_argument('-overall', nargs='*', metavar='COUNTRY', help='The most successful year of the countries')
    parser.add_argument('-interactive', action='store_true', help='Interactive mode')
    parser.add_argument('-output', metavar='NAME', help='The output file')
    return parser.parse_args()

def medals(input_file, country, year) -> list[list]:
    with open(input_file, 'rt') as file:
        counter = 0
        medalists = []
        next(file)
        for line in file:
            elements = line.split('\t')
            year_line = elements[9]
            team = elements[6]
            noc = elements[7]
            medal = elements[14].split('\n')[0]

            if not (year == year_line and (country == team or country == noc)) or medal == 'NA':
                continue

            name = elements[1]
            discipline = elements[12]

            medalists.append([name, discipline, medal])

            if counter >= MEDALISTS - 1:
                break
            counter += 1
        return medalists

def output_file(output_file_name: str, content: str):
    with open(output_file_name, 'wt') as file:
        file.write(content)

def medals_to_str(medals_out: list[list], output_file_name: str) -> str:
    output_content = ''

    if len(medals_out) == 0:
        output_content = 'No medalists found\nPlease enter the correct country or year.'
    else:
        for i in range(len(medals_out)):
            output_content += f'{i+1}. '
            output_content += f'{medals_out[i][0]} - {medals_out[i][1]} - {medals_out[i][2]}'
            output_content += '\n'
        gold = 0
        silver = 0
        bronze = 0
        for i in medals_out:
            gold += i.count('Gold')
            silver += i.count('Silver')
            bronze += i.count('Bronze')
        output_content += f'Gold: {gold}\n'
        output_content += f'Silver: {silver}\n'
        output_content += f'Bronze: {bronze}'

    return output_content

def total(input_file: str, year):

    slovnik = {}

    spis = []

    with open(input_file,"r") as file:
        for line in file:
            line = line[:-1]
            split = line.split('\t')
            spis.append(split)

        spis.pop(0)


        for i in spis:
            if i[7] not in slovnik:
                slovnik[i[7]] = {}

        for i in slovnik:
            slovnik[i]["Gold"] = 0
            slovnik[i]["Silver"] = 0
            slovnik[i]["Bronze"] = 0


        for i in spis:
            if i[14] == "Gold" and i[9] == str(year):
                slovnik[i[7]]["Gold"] += 1

            if i[14] == "Silver" and i[9] == str(year):
                slovnik[i[7]]["Silver"] += 1

            if i[14] == "Bronze" and i[9] == str(year):
                slovnik[i[7]]["Bronze"] += 1
    return slovnik


def total_to_str(list):

    for i in list:
        if list[i]["Gold"] == 0 and list[i]["Silver"] == 0 and list[i]["Bronze"] == 0:
            continue
        print(f"{i}: {list[i]["Gold"]}-Gold, {list[i]["Silver"]}-Silver, {list[i]["Bronze"]}-Bronze")


def overall(input_file: str, countries: list[str]) -> dict[str, str]:
    result = {}
    for country in countries:
        medals_year: dict[str, int] = {}
        with open(input_file, 'rt') as file:
            next(file)
            for line in file:
                elements = line.split('\n')[0].split('\t')
                team = elements[6]
                noc = elements[7]
                year = elements[9]
                medal = elements[14]
                if medal == 'NA':
                    medal = 0
                else:
                    medal = 1
                if country == team or country == noc:
                    if medals_year.get(year) is None:
                        medals_year[year] = medal
                    else:
                        medals_year[year] += medal
            if medals_year == {}:
                continue
            max_key, max_value = max(medals_year.items(), key=lambda item: item[1])
            result[country] = max_key
    return result

def overall_to_str(overall_out: dict[str, str]) -> str:
    result = ''
    if len(overall_out) == 0:
        result += 'Country not found\nEnter valid countries'
    else:
        for country in overall_out:
            result += '- '
            result += country + ' ' + overall_out[country] + '\n'
    return result

def interactive(input_file: str) -> list:
    country = input('Enter country name: ')
    year_city = {}
    year_medal = {}
    medals_counter = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    with open(input_file, 'rt') as file:
        next(file)
        for line in file:
            elements = line.split('\n')[0].split('\t')
            year = int(elements[9])
            team = elements[6]
            noc = elements[7]
            city = elements[11]
            medal = elements[14]
            medal_name = elements[14]
            if medal == 'NA':
                medal = 0
            else:
                medal = 1

            if country != team and country != noc:
                continue

            if year_city.get(year) is None:
                year_city[year] = city

            if year_medal.get(year) is None:
                year_medal[year] = medal
            else:
                year_medal[year] += medal

            if medal == 1:
                medals_counter[medal_name] += 1

    first_participation_year = min(year_city.keys())
    first_participation = [first_participation_year, year_city[first_participation_year]]

    max_key, max_value = max(year_medal.items(), key=lambda item: item[1])
    most_successful = [max_key, max_value]

    min_key, min_value = min(year_medal.items(), key=lambda item: item[1])
    most_unfortunate = [min_key, min_value]

    average_gold = medals_counter['Gold'] / len(year_medal.keys())
    average_silver = medals_counter['Silver'] / len(year_medal.keys())
    average_bronze = medals_counter['Bronze'] / len(year_medal.keys())
    return [country, first_participation, most_successful, most_unfortunate, [average_gold, average_silver, average_bronze]]

def interactive_to_str(out: list) -> str:
    text = ''
    if len(out) == 0:
        text += 'Country not found\nEnter valid country names'
    else:
        text += f'Statistics of {out[0]}\n'
        text += f'First participation in the Olympics {out[1][0]} in city {out[1][1]}\n'
        text += f'The most successful Olympiad in {out[2][0]}, {out[2][1]} medals\n'
        text += f'The most unsuccessful Olympics in {out[3][0]}, {out[3][1]} medals\n'
        text += f'Average number of medals\n'
        text += f'  Gold: {out[4][0]}\n'
        text += f'  Silver: {out[4][1]}\n'
        text += f'  Bronze: {out[4][2]}\n'
    return text

def main():
    args = parser_arguments()

    if not ((args.medals is not None) ^ (args.total is not None) ^ (args.overall is not None) ^ args.interactive):
        print('Please enter either -medals, or -total, or -overall')
        exit()

    str_data = ''
    if args.medals is not None:
        result = medals(args.input_file, args.medals[0], args.medals[1])
        str_data= medals_to_str(result, args.output)
    elif args.total is not None:
        result = total(args.input_file, args.total)
        str_data = total_to_str(result, args.output)
    elif args.overall is not None:
        result = overall(args.input_file, args.overall)
        str_data = overall_to_str(result)
    elif args.interactive is not None:
        result = interactive(args.input_file)
        str_data = interactive_to_str(result)
    else:
        exit()
    if args.output is not None:
        output_file(args.output, str_data)

    print(str_data)

if __name__ == '__main__':
    main()