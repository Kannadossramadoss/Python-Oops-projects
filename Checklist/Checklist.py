from tabulate import tabulate
import csv
import sys
from datetime import date
import os

class Checklist:
    headers_list = ['S.No','Time slot','Task name','Status']
    def __init__(self, templatefile, outputfile):
        self.templatefile = templatefile
        self.outputfile = outputfile

    def read_csv(self):
        print(self.templatefile)
        if not os.path.isfile(self.templatefile):
            sys.exit("Check list file not found")
        file_to_read = self.templatefile if not os.path.isfile(self.outputfile) else self.outputfile
        with open(file_to_read) as file:
            reader = csv.DictReader(file)
            checklist_list = [[row['S.No'], row['Time slot'], row['Task name'], row['Status']] for row in reader]
        return checklist_list

    def display(self, table_content):
        print(table_content)
        print(tabulate(tabular_data=table_content, headers= Checklist.headers_list , tablefmt="pretty"))
    
    def update_status(self, table_content):
        table_rows = len(table_content)
        while True:
            user_row = input("Enter the row number of task to update: ")
            try:
                user_row = int(user_row)
                if user_row > table_rows:
                    print("Please enter the number in the table: ")
                    self.display(table_content)
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        while True:
            user_status = input("please enter a status Not started, Inprogess, Completed, Incomplete: ").strip().capitalize()
            valid_staus = ['Not started', 'Inprogress', 'Completed', 'Incomplete']
            if user_status in valid_staus:
                break
        table_content[user_row - 1][3] = user_status
        return table_content
    
    def write_csv(self, table_content):
        if not os.path.isfile(self.outputfile):
            with open(self.outputfile, "a") as f:
                pass
        with open(self.outputfile, mode='w', newline='') as outputfile:
                writer = csv.writer(outputfile)
                writer.writerow(Checklist.headers_list)
                writer.writerows(table_content)
        
def main():
    outputfilename = "output_"+date.today().strftime('%d-%m-%Y') +".csv"
    checklist_obj = Checklist(templatefile='Checklist.csv', outputfile=outputfilename)
    checklist = checklist_obj.read_csv()
    checklist_obj.display(table_content=checklist)
    checklist = checklist_obj.update_status(table_content=checklist)
    checklist_obj.display(table_content=checklist)
    checklist_obj.write_csv(table_content=checklist)
        
if __name__ == "__main__":
    main()