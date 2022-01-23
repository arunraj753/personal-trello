import os
from trello_module import TrelloModule

boards = ["The Coder Board", "The Developer Board", "The Tester Board"]

the_coder_board_lists = [
    "Idea",
    "Brainstorming",
    "Out For Development",
    "Developed",
    "Trashed",
]
the_developer_baord_lists = [
    "Backlogs",
    "Committed Backlogs",
    "Upcoming Sprints",
    "Current Sprint",
    "Out For Testing Sprints",
    "On Hold Sprints",
    "Completed Sprints",
]
the_tester_baord_lists = [
    "Backlogs",
    "Committed Backlogs",
    "Upcoming Sprints",
    "Current Sprint",
    "On Hold Sprints",
    "Completed Sprints",
]
trello_lists = {
    "the_coder_board_lists": the_coder_board_lists,
    "the_developer_board_lists": the_developer_baord_lists,
    "the_tester_board_lists": the_tester_baord_lists,
}
tr = TrelloModule()
trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_api_token = os.environ.get("TRELLO_API_TOKEN")

print("Fetching Trello Boards")
trello_boards_dict = tr.get_or_create_boards(boards)
print("Boards section completed.\nStarting lists")

trello_lists_id_dict = {}
for key in trello_lists.keys():
    board_name = key.replace("_lists", "").replace("_", " ").title()
    board_id = trello_boards_dict[board_name]
    required_lists_on_board = trello_lists[key]
    temp_lists_id_dict = tr.get_or_create_lists(board_id, required_lists_on_board)
    trello_lists_id_dict.update({key: temp_lists_id_dict})
    print(f"Lists completed for {key}")
print("Lists section completed")
