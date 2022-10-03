from src import Controller 

def main():
    main_window = Controller.Controller()
    main_window.mainLoop()

team = {"lead": "Nolan Smithers", "backend": "Alicia Unterreiner", "frontend": "Shreya Shetty"}
print("Software Lead is:", team["lead"])
print("Backend is:", team["backend"])
print("Frontend is:" , team["frontend"])
    ###### NOTHING ELSE SHOULD GO IN main(), JUST THE ABOVE 2 LINES OF CODE ######
main()
