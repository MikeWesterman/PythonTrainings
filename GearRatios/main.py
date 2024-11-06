from Schematic import Schematic

if __name__ == "__main__":
    schematic = Schematic(["467..114..",
                 "...*......",
                 "..35..633.", 
                 "......#...",
                 "617*......",
                 ".....+.58." ,
                 "..592....." ,
                 "......755." ,
                 "...$.*...." ,
                 ".664.598.."])
    
    part_number_sum = schematic.Sum_Part_Numbers()
    print(part_number_sum)