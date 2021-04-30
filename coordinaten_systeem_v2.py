class Map():
    
    def __init__(self,name,x,y):
        self.name = name        # Naam van het verblijf
        self._map = []          # Standaarddefinitie _map 
        self.x = x              # Breedte in M(eters)
        self.y = y              # Lengte in M(eters)


    def __repr__(self):                         # Print de kaart automatisch, om dit weer te geven typ alleen de naam van de variabele
        for row in self._map:                  
            print()              
            for col in row:        
                if col == 0:
                    print("  ", end='')
                else:
                    print(f" {col}", end='') 
        print()
        print()
        return f"Naam: {self.name}, Lengte: {self.y}m, Breedte: {self.x}m"          # Print extra informatie van de klasse

##### Hieronder de bijbehorende functies #####

    def create(self):                   # Maakt de kaart aan
        x = self.x
        y = self.y
        for i in range(0, y):              # Voor elk element in range(y)
            row = []
            for col in range(0, x):            # Voor elk element in range(x)
                row.append("#")                   # Append "#" aan row
            self._map.append(row)           # Append row aan self._map


    def fill(self):                             # Zorgt er voor dat het verblijf gevult wordt met 0'en en de rand van het verblijf ('#') over blijft.
        for row in range(1, self.y - 1):
            for col in range(1, self.x - 1):
                self._map[row][col] = 0
       

    def add_beacon(self, xdes, ydes, _range):               # Voegt een @ (BT toegangspunt) toe op gekozen coordinaten
        if xdes > 1 and ydes > 1:                           # Checkt of de gekozen posities in het verblijf zit
            if xdes < self.x:
                if ydes < self.y:
                    self._map[ydes - 1][xdes - 1] = "@"
        if self._map[ydes - 1][xdes - 1] == "@":            # Als de beacon succesvol geplaatst is:
            for i in range(_range):                         # Voor elk element in range(0, _range)
                if i != 0:                                  # Als i niet de positie van de beacon is:
                    if ydes - i > 1:                                # Meer checken posities binnen het verblijf
                        self._map[ydes - 1 - i][xdes -1] = "%"
                    if ydes - 1 + i < self.y - 1:
                        self._map[ydes - 1 + i][xdes -1] = "%"
                    if xdes - i > 1:
                        self._map[ydes - 1][xdes -1 - i] = "%"
                    if xdes - 1 + i < self.x - 1:
                        self._map[ydes - 1][xdes -1 + i] = "%"

        
    def print_map(self):
        """This function prints the 2D list-of-lists."""
        for row in self._map:       # row is de hele rij 
            print()              
            for col in row:         # col is het individuele element
                print(col, end='')  # druk dat element af 

# verblijf = Map("Test", 15, 15)
# verblijf.create()
# verblijf.fill()
# verblijf.add_beacon(8,8,4)
# verblijf (voor het printen)

