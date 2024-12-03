class Interactive:
    input_file: str
    data: list

    def file_process(self):
        country = input('Enter country name: ')
        year_city = {}
        year_medal = {}
        medals_counter = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        with open(self.input_file, 'rt') as file:
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

        if year_city == {} or year_medal == {}:
            input_file = []

        first_participation_year = min(year_city.keys())
        first_participation = [first_participation_year, year_city[first_participation_year]]

        max_key, max_value = max(year_medal.items(), key=lambda item: item[1])
        most_successful = [max_key, max_value]

        min_key, min_value = min(year_medal.items(), key=lambda item: item[1])
        most_unfortunate = [min_key, min_value]

        average_gold = medals_counter['Gold'] / len(year_medal.keys())
        average_silver = medals_counter['Silver'] / len(year_medal.keys())
        average_bronze = medals_counter['Bronze'] / len(year_medal.keys())
        self.data = [country, first_participation, most_successful, most_unfortunate,
                [average_gold, average_silver, average_bronze]]

    def __init__(self,input_file: str):
        self.input_file = input_file
        self.file_process()

    def to_str(self):
        text = ''
        if len(self.data) == 0:
            text += 'Country not found\nEnter valid country names'
        else:
            text += f'Statistics of {self.data[0]}\n'
            text += f'First participation in the Olympics {self.data[1][0]} in city {self.data[1][1]}\n'
            text += f'The most successful Olympiad in {self.data[2][0]}, {self.data[2][1]} medals\n'
            text += f'The most unsuccessful Olympics in {self.data[3][0]}, {self.data[3][1]} medals\n'
            text += f'Average number of medals\n'
            text += f'  Gold: {self.data[4][0]}\n'
            text += f'  Silver: {self.data[4][1]}\n'
            text += f'  Bronze: {self.data[4][2]}\n'
        return text