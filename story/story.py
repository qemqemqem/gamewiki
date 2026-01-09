from typing import List


class StoryElement:
    # Could be a character, a place, an object, etc.
    def __init__(self, name: str):
        self.text: str = name
        self.mentioned_in_arcs: List[StoryArc] = []


class StoryArc:
    def __init__(self):
        self.details = ""  # TODO
        self.involved_elements: List[StoryElement] = []

class Section:
    def __init__(self, text):
        self.text: str = text
        self.started_arcs: List[StoryArc] = []
        self.ended_arcs: List[StoryArc] = []
        self.mentioned_arcs: List[StoryArc] = []


class Story:
    def __init__(self):
        self.sections = []
        self.outstanding_arcs: List[StoryArc] = []