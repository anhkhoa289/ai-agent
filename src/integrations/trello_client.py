"""
Trello integration client
"""
from typing import List, Dict, Any, Optional
from trello import TrelloClient as TrelloAPI
from ..config.settings import settings


class TrelloClient:
    """Client for interacting with Trello API"""

    def __init__(self):
        """Initialize Trello client"""
        self.client: Optional[TrelloAPI] = None
        if settings.TRELLO_API_KEY and settings.TRELLO_TOKEN:
            self.client = TrelloAPI(
                api_key=settings.TRELLO_API_KEY,
                token=settings.TRELLO_TOKEN
            )

    def get_board_cards(self, board_id: str, list_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get cards from a board

        Args:
            board_id: Trello board ID
            list_name: Optional list name filter

        Returns:
            List of card dictionaries
        """
        if not self.client:
            raise ValueError("Trello client not configured")

        board = self.client.get_board(board_id)
        lists = board.list_lists()

        cards = []
        for trello_list in lists:
            if list_name and trello_list.name != list_name:
                continue

            for card in trello_list.list_cards():
                cards.append({
                    "id": card.id,
                    "name": card.name,
                    "description": card.description,
                    "list": trello_list.name,
                    "due_date": card.due_date,
                    "labels": [label.name for label in card.labels],
                    "members": [member.full_name for member in card.members]
                })

        return cards

    def get_sprint_cards(self, board_id: str, sprint_label: str) -> List[Dict[str, Any]]:
        """
        Get cards for a specific sprint

        Args:
            board_id: Trello board ID
            sprint_label: Sprint label name

        Returns:
            List of sprint card dictionaries
        """
        all_cards = self.get_board_cards(board_id)
        sprint_cards = [
            card for card in all_cards
            if sprint_label in card.get("labels", [])
        ]

        return sprint_cards

    def move_card(self, card_id: str, list_id: str) -> bool:
        """
        Move card to a different list

        Args:
            card_id: Card ID
            list_id: Target list ID

        Returns:
            Success status
        """
        if not self.client:
            raise ValueError("Trello client not configured")

        try:
            card = self.client.get_card(card_id)
            card.change_list(list_id)
            return True
        except Exception as e:
            print(f"Error moving card: {e}")
            return False

    def create_card(self, list_id: str, name: str, description: str,
                   labels: Optional[List[str]] = None) -> Optional[str]:
        """
        Create a new card

        Args:
            list_id: List ID where card will be created
            name: Card name
            description: Card description
            labels: Optional list of label names

        Returns:
            Created card ID or None
        """
        if not self.client:
            raise ValueError("Trello client not configured")

        try:
            trello_list = self.client.get_list(list_id)
            card = trello_list.add_card(name=name, desc=description)

            if labels:
                board = trello_list.board
                board_labels = board.get_labels()
                for label_name in labels:
                    matching_labels = [l for l in board_labels if l.name == label_name]
                    if matching_labels:
                        card.add_label(matching_labels[0])

            return card.id
        except Exception as e:
            print(f"Error creating card: {e}")
            return None

    def add_comment(self, card_id: str, comment: str) -> bool:
        """
        Add comment to card

        Args:
            card_id: Card ID
            comment: Comment text

        Returns:
            Success status
        """
        if not self.client:
            raise ValueError("Trello client not configured")

        try:
            card = self.client.get_card(card_id)
            card.comment(comment)
            return True
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False
