import os
import requests

trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")
YOUTUBE_BOARD_NAME = "The Youtube Board"


class TrelloModule:
    payload = {"key": trello_api_key, "token": trello_api_token}
    url = "https://api.trello.com/"

    def validate_response_status(self, response):
        success_codes = [200, 201, 203]
        if response.status_code not in success_codes:
            print("An error occured.\nResponse status code : ", response.status_code)
            print(response.text)
            exit(0)

    def get_user_boards(self):
        endpoint = "1/members/me/boards"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"fields": "name"})
        response = requests.get(request_url, data=payload)
        self.validate_response_status(response)
        return response.json()

    def get_or_create_boards(self, boards_list):

        boards_dict = {}
        boards_json = self.get_user_boards()
        for board in boards_json:
            if board["name"] in boards_list:
                board_name = board["name"].replace(" ", "_").lower()
                print("\tFound : ", board["name"])
                boards_dict.update({board_name: board["id"]})
                boards_list.remove(board["name"])

        if not boards_list:
            return boards_dict
        endpoint = "1/boards/"
        request_url = self.url + endpoint
        for trello_board_name in boards_list:
            payload = self.payload.copy()
            payload.update({"name": trello_board_name, "defaultLists": "false"})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)
            print(f"\t{trello_board_name}  Created!!")
            board_id = response.json()["id"]
            board_name = trello_board_name.replace(" ", "_").lower()
            boards_dict.update({board_name: board_id})
        return boards_dict

    def get_lists_on_board(self, board_id):
        endpoint = f"1/boards/{board_id}/lists"
        request_url = self.url + endpoint
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        return dict(
            [
                (trello_list["name"], trello_list["id"])
                for trello_list in response.json()
            ]
        )

    def create_lists_on_board(self, board_id, trello_list_to_create):
        endpoint = f"1/boards/{board_id}/lists"
        request_url = self.url + endpoint
        created_list_dict = {}
        for list_name in trello_list_to_create:
            payload = self.payload.copy()
            payload.update({"name": list_name, "pos": "bottom"})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)
            response_json = response.json()
            print(f"\tCreated the list : {list_name}")
            created_list_dict.update({response_json["name"]: response_json["id"]})
        return created_list_dict

    def get_labels_on_board(self, board_id):
        response_json = self.get_label_details_on_board(board_id)
        return dict(
            [
                (label_details["color"], label_details["id"])
                for label_details in response_json
            ]
        )

    def get_label_details_on_board(self, board_id):
        endpoint = f"1/boards/{board_id}/labels"
        request_url = self.url + endpoint
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        return response.json()

    def create_label_on_board(self, board_id, label_name, label_color):
        endpoint = f"1/boards/{board_id}/labels"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"name": label_name, "color": label_color})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        print(f"\tCreated label: {label_name} - {label_color}")
        return response.json()

    def update_label(self, label_id, label_name, label_color):
        # PUT /1/labels/{id}
        endpoint = f"1/labels/{label_id}"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"name": label_name, "color": label_color})
        response = requests.put(request_url, data=payload)
        self.validate_response_status(response)
        response_json = response.json()
        print(f"\tUpdated label: {response_json['color']} - {response_json['name']}")
        return response.json()

    def get_cards_in_a_list(self, list_id):
        endpoint = f"1/lists/{list_id}/cards"
        request_url = self.url + endpoint
        response = requests.get(request_url, data=self.payload)
        self.validate_response_status(response)
        response_json = response.json()
        return response_json

    def create_card(self, list_id, card_name, desc=False):
        endpoint = "1/cards"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        payload.update({"idList": list_id, "name": card_name})
        if desc:
            payload.update({"desc": desc})
        response = requests.post(request_url, data=payload)
        self.validate_response_status(response)
        response_json = response.json()
        print(
            f"New Trello Card created with title:{card_name} & id: {response_json['id']}"
        )
        return response_json["id"]

    def update_card(self, card_id, card_name=False, desc=False, list_id=False):
        endpoint = f"1/cards/{card_id}"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        if card_name:
            payload.update({"name": card_name})
        if list_id:
            payload.update({"idList": list_id})
        if desc:
            payload.update({"desc": desc})
        response = requests.put(request_url, data=payload)
        self.validate_response_status(response)
        return response.json()

    def add_label_to_card(self, card_id, label_id):
        endpoint = f"1/cards/{card_id}/idLabels"
        request_url = self.url + endpoint
        payload = self.payload.copy()
        response = requests.post(request_url, data=payload)
        # POST /1/cards/{id}/idLabels
