class Card:
    def __init__(self, face, suit):
        """
        Write card class
        """
        self.face = face
        self.suit = suit
        
        # Write name
        if self.face == 11:
            self.face_name = "jack"
        elif self.face == 12:
            self.face_name = "queen"
        elif self.face == 13:
            self.face_name = "king"
        elif self.face == 14:
            self.face_name = "ace"
        else:
            self.face_name = self.face
        self.name = f"{self.face_name} of {self.suit}"
