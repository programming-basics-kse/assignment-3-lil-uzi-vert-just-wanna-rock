import argparse

MEDALISTS = 10

parser = argparse.ArgumentParser(description='Medalists database processing program')
parser.add_argument('input_file', help='Data file address')
parser.add_argument('-medals', nargs=2, metavar = ('COUNTRY', 'YEAR'), help='The top ten medalists from this country at a given Olympiad')
parser.add_argument('-output', metavar='NAME', help='The output file')
args = parser.parse_args()

def medals(input_file, country, year) -> list[list]:
    with open(args.input_file, 'rt') as file:
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