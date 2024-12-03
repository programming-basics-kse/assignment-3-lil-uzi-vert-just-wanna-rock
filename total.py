class Total:
    input_file: str
    data: dict

    def file_process(self, year):
        slovnik = {}

        spis = []

        with open(self.input_file, "r") as file:
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
        self.data = slovnik

    def __init__(self, input_file: str, year):
        self.input_file = input_file
        self.file_process(year)

    def to_str(self) -> str:
        text = ''
        for i in self.data:
            if self.data[i]["Gold"] == 0 and self.data[i]["Silver"] == 0 and self.data[i]["Bronze"] == 0:
                continue
            text += f"{i}: {self.data[i]["Gold"]}-Gold, {self.data[i]["Silver"]}-Silver, {self.data[i]["Bronze"]}-Bronze\n"
        return text