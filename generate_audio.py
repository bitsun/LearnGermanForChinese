# import argparse
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="generate audio mp3  files from html files")
#     parser.parse_args()
from bs4 import BeautifulSoup
import os
#from TTS.api import TTS
#tts = TTS(model_name="tts_models/de/thorsten/vits", progress_bar=False, gpu=False)
#open an html file
audio_file_id = 1
index_file_name = 'index.template.html'
with open(index_file_name,"rb") as html_file:
    soup = BeautifulSoup(html_file, 'html')
    #find all the list items in the html file
    for list_item in soup.find_all('li'):
        filtered_item_content = [item for item in list_item.contents if item.text != '\n']
        #find the tag with with <a> and href
        template_chap_name = filtered_item_content[2].contents[0]['href']
        dst_chap_file_name = template_chap_name.replace('template.','')
        filtered_item_content[2].contents[0]['href'] = dst_chap_file_name

with open("./out/index.html","w",encoding='utf-8') as html_file:
    html_file.write(str(soup))

input_file_name = 'chap01.template.html'
#get file name without extension
file_name = os.path.splitext(input_file_name)[0]
with open(input_file_name,"rb") as html_file:
    soup = BeautifulSoup(html_file, 'html')
    soup.find_all('a')[0]['href'] = "index.html"
    #find all the list items in the html file
    for list_item in soup.find_all('li'):
        #iterate through the item 
        item_cotent = list_item.contents
        #remove the item which is pure white space
        filtered_item_content = [item for item in item_cotent if item.text != '\n']
        if len(filtered_item_content) != 2:
            raise ("item_cotent length is not 4")
        #get the german string by stripping the html tags
        german_string = filtered_item_content[0].text.split('-')[0]
        #feed the german string tts and save the audio file
        dst_file = './audio/{}_{}'.format(file_name.replace('.template',''),str(audio_file_id).zfill(4)+'.wav')
        # if os.path.exists(dst_file):
        #     print("removing existing file before generate {}".format(dst_file))
        #     os.remove(dst_file)
        # #suppress the output of the tts command
        # tts.tts_to_file(text=german_string,file_path=dst_file)
        # if not os.path.exists(dst_file):
        #     raise ("audio file Not generated for {}".format(german_string))
        # else:
        #     print("audio file generated for {}".format(german_string))
        for content in filtered_item_content[1].contents[0].contents:
            if content.name == 'source':
                content['src'] = dst_file
        audio_file_id += 1
#save the html file
with open("./out/chap01.html","w",encoding='utf-8') as html_file:
    html_file.write(str(soup))

        
