import requests


class TrelloApi:
    def __init__(self, key, token) -> None:
       self.key = key
       self.token = token
       
    def chamar_api(self, url, action=None, query=None) -> dict:
        action = action or "GET"
        query = query or {'key': self.key, 'token': self.token}
        headers = {"Accept": "application/json"}
        response = requests.request(
                    action,
                    url,
                    headers=headers,
                    params=query
                )
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
        
    def get_info(self, url, lista = []) -> list:
        lst = []
        lst_items = self.chamar_api(url)
        tamanho = len(lst_items)
        for n in range(tamanho):
            dic={}
            items = lst_items[n]
            for i in lista:
                dic.update({i: items[i]})
            lst += [dic]
        return lst
    
    def get_board_id(self, board_name) -> str:
        url = "https://api.trello.com/1/members/me/boards"
        lista = ['id', 'name']
        boards = self.get_info(url, lista)
        for dic in boards:
            if dic['name'] == board_name:
                board_id = dic['id']
                print(board_id)
        return board_id
    
    def get_organizations(self) -> list:
        url = "https://api.trello.com/1/members/me/organizations"
        lista = ['id','displayName']
        lst = self.get_info(url, lista)
        return lst
    
    def get_boards(self, org_id) -> list:
        url = f"https://api.trello.com/1/organizations/{org_id}/boards"
        lista = ['id','name']
        lst = self.get_info(url, lista)
        return lst
    
    def get_lists(self, board_id) -> list:
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        lista = ['id','name']
        lst = self.get_info(url, lista)
        return lst
    
    def get_cards(self, list_id) -> list:
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        lista = ['id','name','start','due','dueComplete','closed','dateLastActivity','idChecklists']
        lst = self.get_info(url, lista)
        return lst
    
    def get_checklists(self, card_id) -> list:
        url = f"https://api.trello.com/1/cards/{card_id}/checklists"
        lista = ['id','name']
        lst = self.get_info(url, lista)
        return lst
    
    def get_checkitems(self, checklist_id) -> list:
        url = f"https://api.trello.com/1/checklists/{checklist_id}/checkitems"
        lista = ['id','name', 'due','state']
        lst = self.get_info(url, lista)
        return lst

    def create_organization(self, displayName):
        url = f"https://api.trello.com/1/organizations"
        querystring = {
                        "displayName": displayName,
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)

    def create_board(self, name, idOrganization, defaultLists:str = 'false'):
        url = f"https://api.trello.com/1/board"
        querystring = {
                        "name": name,
                        "idOrganization": idOrganization,
                        "defaultLists": defaultLists,
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)

        
    def create_list(self, name, idBoard,  pos:str = "bottom"):
        url = f"https://api.trello.com/1/list"
        querystring = {
                        "name": name,
                        "idBoard": idBoard,
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)
    
    def create_card(self, list_id, name, start, due, pos:str = "top"):
        url = f"https://api.trello.com/1/cards"
        querystring = {
                        "idList": list_id,
                        "name": name,
                        "start": start,
                        "due": due,
                        "pos": pos, 
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)

    def create_checklists(self, idCard, name, pos:str = "bottom"):
        url = f"https://api.trello.com/1/checklists"
        querystring = {
                        "name": name,
                        "idCard": idCard,
                        "pos": pos,
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)
        
    def create_checkitems(self, idChecklists, name, due, pos:str = "bottom"):
        url = f"https://api.trello.com/1/checklists/{idChecklists}/checkItems"
        querystring = {
                        "name": name,
                        "due": due,
                        "pos": pos,
                        "key": self.key, 
                        "token": self.token
                       }
        return self.chamar_api(url, action="POST", query=querystring)