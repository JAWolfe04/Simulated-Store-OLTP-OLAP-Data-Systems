class StoreSystem:
    def __init__(self):
        self.menus = {1:
                      "\nMain Menu\n\n"
                      "Please select your company position\n"
                      "A - Chief Operations Officer\n"
                      "B - Human Resources\n"
                      "C - Chief Financial Officer\n"
                      "D - Chief Product Officer\n"
                      "E - Chief Marketing Officer\n"
                      "F - Supplier\n"
                      "G - Cashier\n"
                      "H - Stock Clerk\n"
                      "I - Customer",
                      2:
                      "\nCOO Options\n\n"
                      "A - Print Position Information\n"
                      "B - List Positions\n"
                      "C - Create Position\n"
                      "D - Set Minimum Position Salary\n"
                      "E - Set Maximum Position Salary\n"
                      "F - Remove Position\n"
                      "G - List Departments\n"
                      "H - Create Department\n"
                      "I - Rename Department\n"
                      "J - Remove Department\n"
                      "K - Print Store Information\n"
                      "L - List Stores\n"
                      "M - Open Store\n"
                      "N - Close Store\n"
                      "O - Get Sales Report",
                      3:
                      "\nHR Options\n\n"
                      "A - Hire Employee\n"
                      "B - Give Raise\n"
                      "C - Transfer Employee\n"
                      "D - Fire Employee\n"
                      "E - Get Employee Report",
                      4:
                      "\nCFO Options\n\n"
                      "A - Get Sales Report",
                      5:
                      "\nCPO Options\n\n"
                      "A - Research Department Products\n"
                      "B - Add Product\n"
                      "C - Remove Product\n"
                      "D - Get Product Report",
                      6:
                      "\nCMO Options\n\n"
                      "A - Add Product Deal\n"
                      "B - Update Product Deal\n"
                      "C - Add Advertisement\n"
                      "D - Update Advertisement\n"
                      "E - Get Product Report",
                      7:
                      "\nSupplier Options\n\n"
                      "A - Restock Product\n"
                      "B - Get Product Report",
                      8:
                      "\nCashier Options\n\n"
                      "A - Create Payment",
                      9:
                      "\nStock Clerk Options\n\n"
                      "A - Restock Shelf",
                      10:
                      "\nCustomer Options\n\n"
                      "A - Start Payments"}
        self.menu_state = 1
        
    def run(self):
        while(self.menu_state):
            print(self.menus.get(self.menu_state))
            print("1 - Main Menu\n"
                  "0 - Exit\n")
            current_menu = self.menu_state
            user_input = input("Enter menu option: ").lower()

            if self.menu_state == 1:
                if user_input == 'a':
                    self.menu_state = 2
                elif user_input == 'b':
                    self.menu_state = 3
                elif user_input == 'c':
                    self.menu_state = 4
                elif user_input == 'd':
                    self.menu_state = 5
                elif user_input == 'e':
                    self.menu_state = 6
                elif user_input == 'f':
                    self.menu_state = 7
                elif user_input == 'g':
                    self.menu_state = 8
                elif user_input == 'h':
                    self.menu_state = 9
                elif user_input == 'i':
                    self.menu_state = 10
            elif self.menu_state == 2:
                pass
            elif self.menu_state == 3:
                pass
            elif self.menu_state == 4:
                pass
            elif self.menu_state == 5:
                pass
            elif self.menu_state == 6:
                pass
            elif self.menu_state == 7:
                pass
            elif self.menu_state == 8:
                pass
            elif self.menu_state == 9:
                pass
            elif self.menu_state == 10:
                pass

            if user_input == '0' or user_input == '1':
                self.menu_state = int(user_input)
            elif current_menu == self.menu_state:
                print("\nInvalid input please select again")
            
if __name__ == "__main__":
    StoreSystem().run()
