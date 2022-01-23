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
                print("\tFound : ", board["name"])
                boards_dict.update({board["name"]: board["id"]})
                boards_list.remove(board["name"])

        if not boards_list:
            return boards_dict
        endpoint = "1/boards/"
        request_url = self.url + endpoint
        for board_name in boards_list:
            payload = self.payload.copy()
            payload.update({"name": board_name, "defaultLists": "false"})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)
            print(f"\t{board_name} Board Created!!")
            board_id = response.json()["id"]
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

    def get_or_create_lists(self, board_id, trello_list_to_create):
        trello_lists_on_board = self.get_lists_on_board(board_id)

        trello_lists_dict = {}
        for trello_list_name in trello_lists_on_board.keys():
            if trello_list_name in trello_list_to_create:
                print(f"\tFound the list {trello_list_name}")
                trello_list_to_create.remove(trello_list_name)
                trello_lists_dict.update(
                    {trello_list_name: trello_lists_on_board[trello_list_name]}
                )

        if not trello_list_to_create:
            return trello_lists_dict

        endpoint = f"1/boards/{board_id}/lists"
        request_url = self.url + endpoint
        for list_name in trello_list_to_create:
            payload = self.payload.copy()
            payload.update({"name": list_name, "pos": "bottom"})
            response = requests.post(request_url, data=payload)
            self.validate_response_status(response)
            response_json = response.json()
            print(f"\tCreated the list : {list_name}")
            trello_lists_dict.update({response_json["name"]: response_json["id"]})
        return trello_lists_dict
