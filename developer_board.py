import random


class DeveloperBoard:
    def __init__(self, board_id, trello_obj):
        self.required_lists = [
            "Committed Backlogs",
            "Upcoming Sprints",
            "Current Sprint",
            "Out For Testing Sprints",
            "On Hold Sprints",
            "Completed Sprints",
        ]
        self.board_id = board_id
        self.trello_obj = trello_obj

    def trello_list_operations(self):
        print("Starting The Developer Board Operations")
        lists_on_board_dict = self.trello_obj.get_lists_on_board(self.board_id)
        board_lists_to_create = [
            list_name
            for list_name in self.required_lists
            if list_name not in lists_on_board_dict.keys()
        ]
        if board_lists_to_create:
            lists_on_board_dict.update(
                self.trello_obj.create_lists_on_board(
                    self.board_id, board_lists_to_create
                )
            )

        self.lists_on_board_dict = lists_on_board_dict
        print("List Operations completed for Developer Board")

    def get_or_create_labels(self, labels_needed):
        available_colors = [
            "purple",
            "blue",
            "orange",
            "black",
            "sky",
            "lime",
        ]
        labels_needed.append("test")
        print("labels_needed", labels_needed)
        existing_labels_details = self.trello_obj.get_label_details_on_board(
            self.board_id
        )
        print("existing_labels_details\n", existing_labels_details)
        labels_to_update_id = []
        existing_labels_dict = {}
        for label_detail in existing_labels_details:
            label_id = label_detail["id"]
            label_color = label_detail["color"]
            label_name = label_detail["name"]
            if label_name in labels_needed:
                existing_labels_dict.update({label_name: label_id})
            else:
                if label_color in available_colors:
                    labels_to_update_id.append(label_id)
        print("existing_labels_dict", existing_labels_dict)
        print("labels_to_update_id : ", labels_to_update_id)
        labels_to_create = [
            label_name
            for label_name in labels_needed
            if label_name not in existing_labels_dict.keys()
        ]
        print("labels_to_create : ", labels_to_create)
        count = 0
        for label_name in labels_to_create:
            if count > len(labels_to_update_id):
                response = self.trello_obj.create_label_on_board(
                    self.board_id,
                    label_name,
                    random.choice(available_colors),
                )
            else:
                label_id = labels_to_update_id[count]
                response = self.trello_obj.update_label(label_id, label_name, None)

            existing_labels_dict.update({response["name"]: response["id"]})
            count += 1
        return existing_labels_dict

    def fetch_backlog_cards(self):
        backlog_trello_list_id = self.lists_on_board_dict["Backlogs"]
        return self.trello_obj.get_cards_in_a_list(backlog_trello_list_id)
