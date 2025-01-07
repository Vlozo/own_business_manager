from services import Manager

class Storage:
    def __init__(self, sheet_id):
        self.manager = Manager()
        self.manager.set_sheet_id(sheet_id)
    
    def register_product(self, product, price, min_storage):
        empty_row = self.manager.find_first_empty_row("Storage!A:A")
        range_name = f'Storage!A{empty_row}:E{empty_row}'
        values = [empty_row - 1, product, 0, price, min_storage]
        return self.manager.insert_data(values, range_name)
    
    def register_action(self, date, action, product, quantity):
        empty_row = self.manager.find_first_empty_row("Movimentações!A:A")
        range_name = f'Movimentações!A{empty_row}:D{empty_row}'
        values = [date, action, product, quantity]
        return self.manager.insert_data(values, range_name)
    
    def sell_product(self, product, quantity, discount):
        empty_row = self.manager.find_first_empty_row("TesteVendas!B:B")
        range_name = f'TesteVendas!A{empty_row}:D{empty_row}'
        values = [product, quantity, None, discount]
        return self.manager.insert_data(values, range_name)


