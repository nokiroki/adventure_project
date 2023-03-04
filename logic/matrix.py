from exceptions import NameNotExistsException


class Matrix:

    def __init__(self, names, matrix=None):
        self.matrix = matrix
        if not self.matrix:
            self.matrix = [[0] * len(names) for i in range(len(names))]
        else:
            self.matrix = [list(map(lambda s: int(s), store)) for store in self.matrix]
        self.names = names
        self.bank = {'debt': {}, 'to_return': {}}

    def money_to_person(self, name):
        price = 0
        i = self.get_id_by_name(name)
        for s in self.matrix: price += s[i]
        
        return price

    def money_from_person(self, name):
        price = 0
        i = self.get_id_by_name(name)
        for p in self.matrix[i]: price += p
        return price

    def money_from_to(self, name_from, name_to):
        return self.matrix[self.get_id_by_name(name_from)][self.get_id_by_name(name_to)]

    def no_zero_price_generator(self):
        for i, row in enumerate(self.matrix):
            for j, price in enumerate(row):
                if price != 0:
                    yield price, self.names[i], self.names[j]

    def get_id_by_name(self, name):
        if name in self.names:
            return self.names.index(name)
        else: 
            print('exception!')
            raise NameNotExistsException('Имя не существует!')

    def add_money_to_debt(self, money, name_from, name_to):
        if name_to == name_from: return False
        i = self.get_id_by_name(name_to)
        try:
            self.matrix[self.get_id_by_name(name_from)][i] += money
            return True
        except NameNotExistsException:
            return False

    def remove_money_from_debt(self, money, name_from, name_to):
        if name_to == name_from: return False
        i = self.get_id_by_name(name_from)
        try:
            money_exist = self.matrix[i][self.get_id_by_name(name_to)]
            if (money_exist - money) < 0:
                money_to_add = money - money_exist
                money_exist = 0
            else:
                money_exist -= money
                money_to_add = 0
            if money_to_add != 0: self.add_money_to_debt(money_to_add, name_to, name_from)
            self.matrix[i][self.get_id_by_name(name_to)] = money_exist
            return True
        except NameNotExistsException:
            return False

    def add_money_equally(self, money, name_to, people_to_remove):
        num = len(self.names) if people_to_remove is None else len(self.names) - len(people_to_remove)
        part_money = int(money / num)
        self.add_money_separated(part_money, name_to, people_to_remove)

    def add_money_separated(self, part_money, name_to, people_to_remove):
        for name_from in self.names:
            if people_to_remove:
                if self.get_id_by_name(name_from) in people_to_remove:
                    continue
            self.add_money_to_debt(part_money, name_from, name_to)

    def add_money_to_bank(self, person, money):
        try:
            self.bank['debt'].update({self.get_id_by_name(person): money})
            return True
        except NameNotExistsException: return False
    
    def add_debt_to_bank(self, person, money):
        try:
            self.bank['to_return'].update({self.get_id_by_name(person): money})
            return True
        except NameNotExistsException: return False

    def clear_bank(self):
        for creditor in self.bank['debt']:
            for debter in self.bank['to_return']:
                if self.bank['debt'][creditor] == 0:
                    self.bank['debt'].pop(creditor)
                    break
                if self.bank['debt'][creditor] > self.bank['to_return'][debter]:
                    to_remove_debter =  self.bank['to_return'][debter]
                    to_remove_creditor = to_remove_debter
                else:
                    to_remove_debter =  self.bank['to_return'][debter] - self.bank['debt'][creditor]
                    to_remove_creditor = self.bank['debt'][creditor]
                self.bank['debt'][creditor] -= to_remove_creditor
                self.bank['to_return'][debter] -= to_remove_debter
                if debter != creditor:
                    self.matrix[debter][creditor] += to_remove_debter
                if self.bank['to_return'][debter] == 0:
                    self.bank['to_return'].pop(debter)

    def create_named_matrix(self):
        alls = [['/////'] + self.names]
        if self.matrix:
            for num, n in enumerate(self.names):
                alls.append([n] + self.matrix[num])
        return alls


    def update_procedure(self):
        for i, row in enumerate(self.matrix):
            for j, price in enumerate(row[i:]):
                actual_j = j+i
                if price != 0:
                    second_price = self.matrix[actual_j][i]
                    if second_price != 0:
                        if price > second_price:
                            price -= second_price
                            second_price = 0
                        else:
                            second_price -= price
                            price = 0
                        self.matrix[i][actual_j] = price
                        self.matrix[actual_j][i] = second_price


        for i, row in enumerate(self.matrix):
            to_person = self.money_to_person(self.names[i])
            from_person = self.money_from_person(self.names[i])
            if to_person != 0 and from_person != 0:
                for num, money in enumerate(row):
                    if to_person != 0 and from_person != 0:
                        restore_dict = dict()
                        update_flag = False
                        for num_person, row_second in enumerate(self.matrix):
                            money_own = row_second[i]
                            money_temp = money
                            if money_own < money_temp and update_flag != True:
                                update_flag = True
                            if money_own != 0 and self.matrix[num_person][num] != 0:
                                restore_dict.update({num_person:money_own})
                                money_temp -= money_own
                                if money_temp <= 0:
                                    update_flag = True
                                    break
                        if not update_flag: continue
                        for name in restore_dict:
                            diff = 0
                            money_own = restore_dict[name]
                            if money > money_own:
                                money -= money_own
                                diff = money_own
                                money_own = 0
                            else:
                                money_own -= money
                                diff = money
                                money = 0
                            self.matrix[i][num] = money
                            self.matrix[name][i] = money_own
                            self.matrix[name][num] += diff

                        to_person = self.money_to_person(self.names[i])
                        from_person = self.money_from_person(self.names[i])

                    else: break
