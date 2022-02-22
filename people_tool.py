import os

def scrape_folder(folder_path):
    with open(str(folder_path[:len(folder_path)-1])+".txt", "w", encoding='utf-8') as f:
        for file_txt in os.listdir(folder_path):
            f.write(folder_path+file_txt+"\n")


scrape_folder("people/")