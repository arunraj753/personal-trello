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
        lists_on_board_dict = self.tr_obj.get_lists_on_board(self.board_id)
        board_lists_to_create = [
            list_name
            for list_name in self.required_lists
            if list_name not in lists_on_board_dict.keys()
        ]
        if board_lists_to_create:
            lists_on_board_dict.update(
                self.tr_obj.create_lists_on_board(self.board_id, board_lists_to_create)
            )

        self.lists_on_board_dict = lists_on_board_dict
        print("List Operations completed")

    def get_or_create_labels(self):
        self.labels = self.tr_obj.get_labels_on_board(self.board_id)
        self.tr_obj.update_label(self.labels["green"], "Ready To Commit", "green")
        print("Label Operations completed for Coder Board")

    def project_cards(self):
        out_for_development_list_id = self.lists_on_board_dict["Out For Development"]
        project_cards_list = self.tr_obj.get_cards_in_a_list(
            out_for_development_list_id
        )
        print("Fetched cards from 'Out For Development'")
        project_lists_to_create = []
        for card in project_cards_list:
            project_name = card["name"]
            if not project_name + "-Backlogs" in self.lists_on_board_dict.keys():
                project_lists_to_create.append(project_name + "-Backlogs")
            if (
                not project_name + "-Committed Backlogs"
                in self.lists_on_board_dict.keys()
            ):
                project_lists_to_create.append(project_name + "-Committed Backlogs")

        if project_lists_to_create:
            self.lists_on_board_dict.update(
                self.tr_obj.create_lists_on_board(
                    self.board_id, project_lists_to_create
                )
            )
            print("Project cards created")
        else:
            print("All project cards exists")
        self.lists_on_board_dict = self.tr_obj.get_lists_on_board(self.board_id)

        # self.tr_obj.create_label_on_board(self.board_id, "Developed", "green")

    def fetch_not_commited_cards(self):
        self.backlog_trello_lists_dict = self.fetch_backlogs_trello_list()
        print(self.backlog_trello_lists_dict)

    def fetch_backlogs_trello_list(self):
        trello_list_names = self.lists_on_board_dict.keys()
        labels_needed = []
        backlog_trello_lists_dict = {}
        for list_name in trello_list_names:
            splitted_list_name = list_name.split("-Backlogs")
            if len(splitted_list_name) == 2:
                backlog_trello_lists_dict.update(
                    {list_name: self.lists_on_board_dict[list_name]}
                )
                labels_needed.append(splitted_list_name[0])
        return backlog_trello_lists_dict, labels_needed
