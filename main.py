import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()




class BaseModel:

    def get_model(self):
        try:
            genai.configure(api_key= os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-2.5-flash")
            return model
        except Exception as e:
            print(e)



class AppFeatures(BaseModel):
    def __init__(self):
        self.__database = {}
        self.first_menu()

    
    def first_menu(self):
        first_input = input("""
        Hi! How would you like to proceed?

            1. Not a member? Register
            2. Already a member? Login
            3. Bhai galti se aa gaya kia? Exit
                            
            """)
        
        if first_input == "1":
            #register
            self.__register()

        elif first_input == "2":
            #login
            self.__login()

        else:
            exit()

    
    def second_menu(self):
        second_input = input("""
        Hi! How would you like to proceed?

        1. Sentiment Analysis
        2. Language Transilation
        3. Language Detection
        """)

        if second_input == "1":
            # Sentiment Analysis
            self.___sentiment_analysis()

        elif second_input == "2":
            # Language Transilation
            self.___language_transilation()

        elif second_input == "3":
            # Language Detection
            self.___language_detection()

        else:
            exit()

    

    def ___sentiment_analysis(self):
        user_text = input("Enter your text: ")
        model = super().get_model()
        response = model.generate_content(f"Give me the sentiment of this sentence: {user_text}")
        results = response.text
        print(results)
        self.second_menu()

    

    def ___language_transilation(self):
        user_text = input("Enter your text: ")
        model = super().get_model()
        response = model.generate_content(f"Give me Bangla transilation of this sentence: {user_text}")
        results = response.text
        print(results)
        self.second_menu()


    def ___language_detection(self):
        user_text = input("Enter your text: ")
        model = super().get_model()
        response = model.generate_content(f"Detect the language of this sentence: {user_text}")
        results = response.text
        print(results)
        self.second_menu()





    

    def __register(self):
        name = input("Enter Your Name: ")
        email = input("Enter Your Email: ")
        password = input("Enter Your Password: ")

        if email in self.__database:
            print("Email already exists.")
            self.first_menu()

        else:
            self.__database[email] = [name, password]
            print("Registration successful. Now you can login!")
            self.first_menu()



    def __login(self):
        email = input("Enter Your Email: ")
        password = input("Enter Your Password: ")

        if email in self.__database:
            if self.__database[email][1] == password:
                print("Login Successfull!")
                # second menu
                self.second_menu()
            else:
                print("Incorrect Password")
                self.__login()
        else:
            print("Email not found. Please register first.")
            self.first_menu()

    



app = AppFeatures()

