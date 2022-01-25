import os
from trello_module import TrelloModule
from coder_board import CoderBoard
from developer_board import DeveloperBoard

boards = ["The Coder Board", "The Developer Board", "The Tester Board"]

coder_board_lists_required = [
    "Idea",
    "Brainstorming",
    "Out For Development",
    "Developed",
    "Trashed",
]

developer_baord_lists_required = [
    "Backlogs",
    "Committed Backlogs",
    "Upcoming Sprints",
    "Current Sprint",
    "Out For Testing Sprints",
    "On Hold Sprints",
    "Completed Sprints",
]
tester_baord_lists_required = [
    "Backlogs",
    "Committed Backlogs",
    "Upcoming Sprints",
    "Current Sprint",
    "On Hold Sprints",
    "Completed Sprints",
]
ready_to_commit = "Ready To Commit"
# trello_lists = {
#     "the_coder_board_lists": the_coder_board_lists,
#     "the_developer_board_lists": the_developer_baord_lists,
#     "the_tester_board_lists": the_tester_baord_lists,
# }
trello_ = TrelloModule()
trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")

print("Fetching Trello Boards")
trello_boards_dict = trello_.get_or_create_boards(boards)
coder_board_id = trello_boards_dict["the_coder_board"]
developer_board_id = trello_boards_dict["the_developer_board"]
tester_board_id = trello_boards_dict["the_tester_board"]

coder_obj = CoderBoard(coder_board_id, trello_)
dev_obj = DeveloperBoard(developer_board_id, trello_)
coder_obj.trello_list_operations()
coder_obj.get_or_create_labels()
coder_obj.project_cards()
(
    coderboard_backlog_lists_dict,
    labels_for_dev_board,
) = coder_obj.fetch_backlogs_trello_list()
print("Fetched 'coder_board_backlog_lists' and 'labels_for_dev_board'")
dev_obj.trello_list_operations()
dev_board_labels_dict = dev_obj.get_or_create_labels(list(set(labels_for_dev_board)))
print(dev_board_labels_dict)
exit(0)
cards_to_create_in_dev_backlog = []
for list_name in coderboard_backlog_lists_dict.keys():
    list_id = coderboard_backlog_lists_dict[list_name]
    backlog_cards = trello_.get_cards_in_a_list(list_id)
    for card in backlog_cards:
        card_labels = card["labels"]
        for label in card_labels:
            if label["name"] == ready_to_commit:
                cards_to_create_in_dev_backlog.append(
                    {
                        "name": card["name"],
                        "id": card["id"],
                        "label": list_name.split("-Backlogs")[0],
                    }
                )

print(cards_to_create_in_dev_backlog)
dev_board_backlog_id = dev_obj.lists_on_board_dict["Committed Backlogs"]
print(dev_obj.lists_on_board_dict)

for card in cards_to_create_in_dev_backlog:
    print(card)
    created_card_id = trello_.create_card(dev_board_backlog_id, card["name"])


# developer_obj.trello_list_operations()ed


# trello_lists_id_dict = {}
# for key in trello_lists.keys():
#     board_name = key.replace("_lists", "").replace("_", " ").title()
#     board_id = trello_boards_dict[board_name]
#     required_lists_on_board = trello_lists[key]
#     temp_lists_id_dict = tr.get_or_create_lists(board_id, required_lists_on_board)
#     trello_lists_id_dict.update({key: temp_lists_id_dict})
#     print(f"Lists completed for {key}")
# print("Lists section completed")
