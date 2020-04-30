class Card:
    def __init__(self, face, suit):
        """
        Write card class
        """
        self.face = face
        self.suit = suit
        
        # Write name
        if self.face == 2.2:
            self.face_name = "jack"
        elif self.face == 2.4:
            self.face_name = "queen"
        elif self.face == 2.6:
            self.face_name = "king"
        elif self.face == 2.8:
            self.face_name = "ace"
        else:
            self.face_name = int(self.face * 5)
        self.name = f"{self.face_name} of {self.suit}"
