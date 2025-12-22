def chance_summon(chance: float, tripled: bool = True):
    if tripled:
        return (chance**3 + 2*(chance**2)*(1-chance))*100
    return (chance**2)*100

if __name__ == '__main__':
    print("Warrior > Dragon > Spellcaster > Zombie > Beast > Warrior")
    _x = (5-int(input("Level (1-4): ")))/6
    _tripled = input("Are you rolling 3? Say yes if so. ").lower() == "yes"
    print("Chance:", chance_summon(chance=_x, tripled=_tripled), end="%\n")
