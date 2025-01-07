from googleapiclient.discovery import build
from google_api.googleService import authenticate

class Manager:
    def __init__(self):
        self.creds = authenticate()
        self.client = build('sheets', 'v4', credentials=self.creds)
        self.sheet_id = None

    def get_sheet_data(self, RANGE):
        sheet = self.client.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId= self.sheet_id, range=RANGE)
            .execute()
        )
        return result.get("values", [])
    
    def find_first_empty_row(self, SHEET_NAME):
        sheet = self.client.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId= self.sheet_id, range=SHEET_NAME)
            .execute()
        )
        values = result.get("values", [])
        return len(values) + 1
    
    def insert_data(self, VALUES, RANGE_NAME):
        sheet = self.client.spreadsheets()
        body = {
            'values' : [VALUES]
        }
        result = (
            sheet.values()
            .update(spreadsheetId=self.sheet_id, range = RANGE_NAME, valueInputOption='USER_ENTERED', body=body)
            .execute()
        )

        return result
    
    def update_data(self, RANGE_NAME, VALUES):
        range_name = RANGE_NAME
        sheet = self.client.spreadsheets()
        body = {
            'values' : [VALUES]
        }
        result = (
            sheet.values()
            .update(spreadsheetId=self.sheet_id, range = range_name, valueInputOption='USER_ENTERED', body=body)
            .execute()
        )

        return result
    
    def check_item_exists(self, SHEET_RANGE, ITEM_NAME):
        values = self.get_sheet_data(SHEET_RANGE)
        item_set = {row[0] for row in values if row}
        return ITEM_NAME in item_set
    
    def find_item_row(self, SHEET_RANGE, ITEM_NAME):
        values = self.get_sheet_data(SHEET_RANGE)
        item_set = {row[0]: i + 2 for i, row in enumerate(values) if row}
        return item_set.get(ITEM_NAME, None)

    def set_sheet_id(self, SHEET_ID):
        self.sheet_id = SHEET_ID