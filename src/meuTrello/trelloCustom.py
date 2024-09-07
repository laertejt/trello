import pandas as pd
from datetime import datetime, date, timedelta
from meuTrello.trelloApi import TrelloApi


class TrelloCustom(TrelloApi):
    def __init__(self, key, token) -> None:
        super().__init__(key, token)

    def pegar_df_organizations(self) -> pd.DataFrame:
        lists = super().get_organizations()
        df = pd.DataFrame.from_dict(lists)
        return df
    
    def pegar_df_boards(self, org_id) -> pd.DataFrame:
        lists = super().get_boards(org_id)
        df = pd.DataFrame.from_dict(lists)
        return df

    def pegar_df_lists(self, board_id) -> pd.DataFrame:
        lists = super().get_lists(board_id)
        df = pd.DataFrame.from_dict(lists)
        return df
    
    def pegar_df_cards(self, list_id) -> pd.DataFrame:
        lists = super().get_cards(list_id)
        df = pd.DataFrame.from_dict(lists)
        return df
    
    def pegar_df_checklists(self, card_id) -> pd.DataFrame:
        lists = super().get_checklists(card_id)
        df = pd.DataFrame.from_dict(lists)
        return df
    
    def pegar_df_checkitems(self, checklist_id) -> pd.DataFrame:
        lists = super().get_checkitems(checklist_id)
        df = pd.DataFrame.from_dict(lists)
        return df
    
    def consultar_df_lists(self, org_name, board_name) -> pd.DataFrame:
        # Organizações
        df_org = self.pegar_df_organizations()
        # Boards
        org_id = df_org.query("displayName==@org_name")['id'].values[0]
        df_board = self.pegar_df_boards(org_id)
        # Lists
        board_id = df_board.query("name==@board_name")['id'].values[0]
        df_list = self.pegar_df_lists(board_id)
        return df_list
    
    def consultar_df_checkitems(self, org_name, board_name, list_name, card_name, checklist_name) -> pd.DataFrame:
        df_list = self.consultar_df_lists(org_name, board_name)
        # Cards
        list_id = df_list.query("name==@list_name")['id'].values[0]
        df_card = self.pegar_df_cards(list_id)
        # CheckLists
        checklist_id = df_card.query("name==@card_name")['id'].values[0]
        df_checklist = self.pegar_df_checklists(checklist_id)
        #CheckItems
        checkitem_id = df_checklist.query("name==@checklist_name")['id'].values[0]
        df_checkitem = self.pegar_df_checkitems(checkitem_id)
        return df_checkitem
    
    def criar_card_mensal(self, org_name, board_name, list_name, card_name, checklist_name, checkitem_name, initial_date, final_date, wday, cal) -> None:
        df_list = self.consultar_df_lists(org_name, board_name)
        list_id = df_list.query("name==@list_name")['id'].values[0]
        card_name_date = f'{card_name} {initial_date.strftime("%B %Y")}'
        dic_card = super().create_card(list_id, card_name_date, initial_date, final_date)
        card_id = dic_card['id']
        dic_checklist = super().create_checklists(card_id, checklist_name)
        checklist_id = dic_checklist['id']
        while initial_date <= final_date:
            if initial_date.weekday() in wday:
                checkitem_name_date = f'{checkitem_name} {initial_date.strftime("%d")}'
                dic_checkitem = super().create_checkitems(checklist_id, checkitem_name_date, initial_date)
                print(f'Card {card_name_date} criado com os CheckList {checklist_name} e CheckItem {checkitem_name_date} !!! ')
            initial_date = cal.offset(initial_date, +1)
            initial_date = datetime.combine(initial_date, datetime.min.time())
            initial_date = initial_date + timedelta(hours=8,minutes=0)
            

    
