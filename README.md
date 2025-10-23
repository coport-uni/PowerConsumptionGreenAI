# GPU Green AI Testing
## Overview
* 수업발표자료 준비겸해서...
* 정말 최신 아키텍쳐로 갈수록 효율이 좋을까?
```bash title=setup
conda create -n apc -y
conda activate apc
curl -fsSL https://ollama.com/install.sh | sh

# 
ollama serve
ollama pull gpt-oss:20b

pip install ollama openpyxl 
```
## Code
* https://wikidocs.net/91661
* https://hwangheek.github.io/2019/python-logging/
* https://toycoding.tistory.com/entry/%EC%97%91%EC%85%80-%EC%84%A4%EC%B9%98%EC%97%86%EC%9D%B4-%EC%BB%B4%ED%93%A8%ED%84%B0%EC%97%90%EC%84%9C-%EA%B0%84%EB%8B%A8%ED%95%98%EA%B2%8C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0VSCode-Excel-Viewer#google_vignette
```python title=main.py
# Need to Control GPU power by manual. But other processes can be automated.
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
```

## Output
* In case of 3090
	* Also, there is example data file.
	* ![[Pasted image 20251023142441.png]]
