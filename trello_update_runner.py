import os
from trello_module import TrelloModule
from coder_board import CoderBoard
from developer_board import DeveloperBoard

dev_and_coder_dict = {
    "Committed Backlogs": "Committed",
    "Upcoming Sprints": "Committed",
    "Current Sprint": "Developing",
    "Out For Testing Sprints": "Testing",
    "On Hold Sprints": "On Hold",
    "Completed Sprints": "Developed",
}
READY_TO_COMMIT = "Ready To Commit"
boards = ["The Coder Board", "The Developer Board", "The Tester Board"]
trello_ = TrelloModule()
trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")
print("Fetching Trello Boards")
trello_boards_dict = trello_.get_or_create_boards(boards)
coder_board_id = trello_boards_dict["the_coder_board"]
developer_board_id = trello_boards_dict["the_developer_board"]
tester_board_id = trello_boards_dict["the_tester_board"]
coder_obj = CoderBoard(coder_board_id, trello_)
coder_obj.board_labels = {
    "Ready To Commit": "red",
    "Committed": "orange",
    "On Hold": "yellow",
    "Developing": "blue",
    "Testing": "purple",
    "Developed": "green",
}
dev_obj = DeveloperBoard(developer_board_id, trello_)
coder_obj.trello_list_operations()
coder_obj.labels = trello_.get_labels_on_board(coder_board_id)
coder_obj.project_cards()
(
    coderboard_backlog_lists_dict,
    labels_for_dev_board,
) = coder_obj.fetch_backlogs_trello_list()
print("Fetched coder_board_backlog_lists and labels_for_dev_board")
dev_obj.trello_list_operations()
dev_board_labels_dict = dev_obj.get_or_create_labels(list(set(labels_for_dev_board)))


cards_to_create_in_dev_backlog = []
dev_board_backlog_id = dev_obj.lists_on_board_dict["Committed Backlogs"]

for list_name in coderboard_backlog_lists_dict.keys():
    list_id = coderboard_backlog_lists_dict[list_name]
    backlog_cards = trello_.get_cards_in_a_list(list_id)
    for card in backlog_cards:
        card_labels = card["labels"]
        for label in card_labels:
            if label["name"] == READY_TO_COMMIT:
                project_name = list_name.split("-Backlogs")[0]
                project_commited_list_name = project_name + "-Committed Backlogs"
                created_card_id = trello_.create_card(
                    dev_board_backlog_id, card["name"]
                )
                trello_.add_label_to_card(
                    created_card_id,
                    dev_board_labels_dict[project_name],
                )
                trello_.update_card(
                    card["id"],
                    list_id=coder_obj.lists_on_board_dict[project_commited_list_name],
                    desc=f"linked_card:{created_card_id}",
                    labels_id=[coder_obj.labels["orange"]],
                )

dev_board_cards = trello_.get_cards_on_a_board(developer_board_id)

dev_board_cards_dict = {}
# dev_board_cards_dict format {card_id : card_list_id}
for card in dev_board_cards:
    dev_board_cards_dict.update({card["id"]: card["idList"]})
# print(all_cards)
# for card in dev_board_cards:
#     print(card, "\n")
dev_board_lists = trello_.get_lists_on_board(developer_board_id)
dev_board_lists_dict = {}
# Format {'list_id': '61efaf75b5f1af86af758061', 'list_name': 'Committed Backlogs'}
for trello_list in dev_board_lists:
    dev_board_lists_dict.update({trello_list["id"]: trello_list["name"]})


coder_board_cards = trello_.get_cards_on_a_board(coder_board_id)
# print("coder_obj.lists_on_board_dict\n", coder_obj.lists_on_board_dict)

for card in coder_board_cards:
    card_id = card["id"]
    desc = card["desc"]
    card_label_id = card["idLabels"]

    if desc:
        linked_card_ = desc.split("linked_card:")
        if len(linked_card_) == 2:
            linked_card_id = linked_card_[1]
            linked_card_list_id = dev_board_cards_dict.get(linked_card_id, None)
            if linked_card_list_id:
                list_name = dev_board_lists_dict.get(linked_card_list_id, None)
                if list_name:
                    label_name = dev_and_coder_dict[list_name]
                    # print(label_name)
                    label_color = coder_obj.board_labels[label_name]

                    if not card_label_id == [coder_obj.labels[label_color]]:

                        print(
                            label_color,
                            list_name,
                        )

                        trello_.update_card(
                            card_id,
                            labels_id=[coder_obj.labels[label_color]],
                        )


print("To commit cards from the coder board are commited")
