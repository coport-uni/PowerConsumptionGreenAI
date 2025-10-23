# Need to Control GPU power by manual. But other processes can be automated.
from ollama import chat
from ollama import ChatResponse
from openpyxl import Workbook
import time
import logging

class AutomatedLLM():
    def __init__(self):
        '''
        This function initialze .xlsx file and set paramaters for logic

        Input : None
        Output : None
        '''
        self.llm_model = 'gpt-oss:20b'
        self.llm_message = [
            {
                'role': 'user',
                'content': 'Describe about Green AI in 1000 words',
            },
        ]
        self.target_wattage = 380

        self.workbook = Workbook()
        self.worksheet = self.workbook.create_sheet("new_sheet1")

        self.worksheet = self.workbook.active
        self.worksheet["A1"] = "GPU_Percentage"
        self.worksheet["B1"] = "Wh"

        self.workbook.save(filename = "data.xlsx")

    def get_llm_collapsed_time(self):
        '''
        This function get average collapsed time of 3 LLM runs 

        Input : None
        Output : Float
        '''
        total = 0
        iteration = 3

        for i in range(iteration):
            start_time = time.time()
            response: ChatResponse = chat(model = self.llm_model, messages=self.llm_message)
            logging.info(response)
            end_time = time.time()
            elapsed_time = end_time - start_time

            total += elapsed_time

        average_time = round(total / 3, 2)
        logging.warning("Average is : " + str(average_time))

        return average_time

    def run_data_logger(self, percentage_watt : int, count : int):
        '''
        This function logging percentage and Wh data to xlsx file

        Input : Int, Int
        Output : None
        '''
        collapsed_time = self.get_llm_collapsed_time() 

        watt = self.target_wattage / 100 * percentage_watt
        wattperhour = round(watt * collapsed_time / 3600, 2)

        logging.info(f"{percentage_watt} : {wattperhour}")

        self.worksheet[f"A{count}"] = percentage_watt
        self.worksheet[f"B{count}"] = wattperhour

        self.workbook.save(filename = "data.xlsx")

def main():
    '''
    This function orchestrate whole logic

    Input : None
    Output : None
    '''
    al = AutomatedLLM()

    # For modeling loading and warming up
    al.get_llm_collapsed_time()

    # 100, 90, 80, 70, 60, 50, 40, 30 (%)
    for i in range(8):
        iteration = int(input("Please type percentage_watt: "))
        al.run_data_logger(iteration, i+2)


if __name__ == "__main__":
    main()