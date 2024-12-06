import argparse

from interactive import Interactive
from medals import Medals
from overall import Overall
from total import Total

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

def output_file(output_file_name: str, content: str):
    with open(output_file_name, 'wt') as file:
        file.write(content)

def main():
    args = parser_arguments()

    if not ((args.medals is not None) ^ (args.total is not None) ^ (args.overall is not None) ^ args.interactive):
        print('Please enter either -medals, or -total, or -overall')
        exit()

    str_data = ''
    if args.medals is not None:
        medals = Medals(args.input_file, args.medals[0], args.medals[1])
        str_data = medals.to_str()
    elif args.total is not None:
        total = Total(args.input_file, args.total)
        str_data = total.to_str()
    elif args.overall is not None:
        overall = Overall(args.input_file, args.overall)
        str_data = overall.to_str()
    elif args.interactive is not None:
        interactive = Interactive(args.input_file)
        str_data = interactive.to_str()
    else:
        exit()
    if args.output is not None:
        output_file(args.output, str_data)

    print(str_data)

if __name__ == '__main__':
    main()