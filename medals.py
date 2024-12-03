MEDALISTS = 10

class Medals:
    input_file: str
    data: list[list]

    def file_process(self, country, year):
        with open(self.input_file, 'rt') as file:
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
        self.data = medalists

    def __init__(self, input_file: str, country, year):
        self.input_file = input_file
        self.file_process(country, year)

    def to_str(self):
        output_content = ''

        if len(self.data) == 0:
            output_content = 'No medalists found\nPlease enter the correct country or year.'
        else:
            for i in range(len(self.data)):
                output_content += f'{i + 1}. '
                output_content += f'{self.data[i][0]} - {self.data[i][1]} - {self.data[i][2]}'
                output_content += '\n'
            gold = 0
            silver = 0
            bronze = 0
            for i in self.data:
                gold += i.count('Gold')
                silver += i.count('Silver')
                bronze += i.count('Bronze')
            output_content += f'Gold: {gold}\n'
            output_content += f'Silver: {silver}\n'
            output_content += f'Bronze: {bronze}'

        return output_content