


class Total:

    input_file: dict
    output: str




    def __init__(self, input_file: str):
        self.input_file = input_file


    def total(self, year):

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
        input_file = slovnik

    def total_to_str(self) -> str:
        text = ""
        for i in self.output:
            if self.output[i]["Gold"] == 0 and self.output[i]["Silver"] == 0 and self.output[i]["Bronze"] == 0:
                continue
            text += f"{i}: {self.output[i]["Gold"]}-Gold, {self.output[i]["Silver"]}-Silver, {self.output[i]["Bronze"]}-Bronze\n"
        output = text