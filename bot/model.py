import json
from pprint import pprint


class Model:
    def __init__(self):
        self.profiles = []
        with open("profile_data.json") as data_file:
            self.profiles = json.load(data_file)

    def hiring_companies(self):
        companies = {}
        for profile in self.profiles:
            company = profile["current_company"]
            if company and profile["is_hiring"]:
                if company not in companies:
                    companies[company] = []
                hiring_for = profile["hiring_for"]
                if hiring_for:
                    companies[company].append(hiring_for)
        return companies

    def company_alumns(self, lookup_company, filter_hiring=False):
        alumns = []
        for profile in self.profiles:
            company = profile["current_company"]
            if company and lookup_company.lower() in company.lower():
                alumns.append(profile)

        if not filter_hiring:
            return alumns

        return [a for a in alumns if a["is_hiring"]]


database = Model()

if __name__ == "__main__":
    m = Model()
    # pprint(m.hiring_companies())
    pprint(m.company_alumns("postmates"))
