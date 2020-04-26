class Card:
    def __init__(self, face, suit):
        """
        Write card class
        """
        self.face = face
        self.suit = suit

        # Write name
        if self.face == 11:
            self.face_name = "Jack"
        elif self.face == 12:
            self.face_name = "Queen"
        elif self.face == 13:
            self.face_name = "King"
        elif self.face == 1:
            self.face_name = "Ace"
        else:
            self.face_name = self.face
        self.name = f"{self.face_name} of {self.suit}"