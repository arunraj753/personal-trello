class CoderBoard:
    def __init__(self, board_id, tr_obj):
        self.required_lists = [
            "Idea",
            "Brainstorming",
            "Out For Development",
            "Developed",
            "Trashed",
        ]
        self.board_id = board_id
        self.tr_obj = tr_obj
        self.labels_required = [
            "Committed",
            "Developing",
            "On Hold",
            "Testing",
            "Developed",
        ]

    def trello_list_operations(self):
        print("Starting The Coder Board Operations")
        board_lists_dict = self.tr_obj.get_lists_on_board(self.board_id)
        board_lists_to_create = [
            list_name
            for list_name in self.required_lists
            if list_name not in board_lists_dict.keys()
        ]
        if board_lists_to_create:
            board_lists_dict.update(
                self.tr_obj.create_lists_on_board(self.board_id, board_lists_to_create)
            )

        self.board_lists_dict = board_lists_dict
        print("List Operations completed")

    def get_or_create_lables(self):
        self.labels = self.tr_obj.get_labels_on_board(self.board_id)

        print(self.labels)
        self.tr_obj.update_label(self.labels["green"], "Committed", "green")

        # self.tr_obj.create_label_on_board(self.board_id, "Developed", "green")
