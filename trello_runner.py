import os
from trello_module import TrelloModule
from coder_board import CoderBoard

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
# trello_lists = {
#     "the_coder_board_lists": the_coder_board_lists,
#     "the_developer_board_lists": the_developer_baord_lists,
#     "the_tester_board_lists": the_tester_baord_lists,
# }
tr = TrelloModule()
trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")

print("Fetching Trello Boards")
trello_boards_dict = tr.get_or_create_boards(boards)
coder_board_id = trello_boards_dict["the_coder_board"]
developer_board_id = trello_boards_dict["the_developer_board"]
tester_board_id = trello_boards_dict["the_tester_board"]

cb = CoderBoard(coder_board_id, tr)
cb.trello_list_operations()
cb.get_or_create_lables()

# trello_lists_id_dict = {}
# for key in trello_lists.keys():
#     board_name = key.replace("_lists", "").replace("_", " ").title()
#     board_id = trello_boards_dict[board_name]
#     required_lists_on_board = trello_lists[key]
#     temp_lists_id_dict = tr.get_or_create_lists(board_id, required_lists_on_board)
#     trello_lists_id_dict.update({key: temp_lists_id_dict})
#     print(f"Lists completed for {key}")
# print("Lists section completed")
