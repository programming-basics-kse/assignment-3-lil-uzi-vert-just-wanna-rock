class Overall:
    input_file: str
    data: dict[str,list]

    def file_process(self, countries: list[str]):
        result = {}
        for country in countries:
            medals_year: dict[str, int] = {}
            with open(self.input_file, 'rt') as file:
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
                result[country] = [max_key, max_value]
        self.data = result

    def __init__(self, input_file: str, countries: list[str]):
        self.input_file = input_file
        self.file_process(countries)

    def to_str(self):
        result = ''
        if len(self.data) == 0:
            result += 'Country not found\nEnter valid countries'
        else:
            for country in self.data:
                result += '- '
                result += f'{country} {self.data[country][0]} year {self.data[country][1]} medals\n'
        return result