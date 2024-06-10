from bs4 import BeautifulSoup
import time
import requests
import os

print('put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')


def create_posts_dir():
    posts_dir = 'webscraping/posts'
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    return posts_dir


def get_next_file_index(counter_file):
    if os.path.exists(counter_file):
        with open(counter_file,'r') as f:
            index = int(f.read().strip())+ 1
    else:
        index = 1
    with open(counter_file,'w') as f:
        f.write(str(index))
    return index

def find_jobs():
    posts_dir = create_posts_dir()
    counter_file = os.path.join(posts_dir,'counter.txt')
    file_index = get_next_file_index(counter_file)
    file_path = os.path.join(posts_dir,f'jobs_{file_index}.txt')
   
   
 
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text,'lxml')
    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
    
    with open(file_path,'a') as f:
        for index,job in enumerate(jobs):
            published_date = job.find('span',class_='sim-posted').span.text    
            if 'few' in published_date: 
                company_name=job.find('h3',class_='joblist-comp-name').text.replace(' ','')
                skills = job.find('span',class_='srp-skills').text.replace(' ','')
                more_info = job.header.h2.a['href']
                if unfamiliar_skill not in skills:
                    # with open(f'{posts_dir}/{index}.txt','w') as f:
                        f.write(f"Job #{index}\n")
                        f.write(f"Comapany Name:{company_name.strip()} \n")
                        f.write(f"Required Skills:{skills.strip()}\n")
                        f.write(f"more info:{more_info}\n\n")
                        print(f'job {index} saved')




if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait=1
        print(f'Waiting {time_wait} minutes...')
        time.sleep(60)
