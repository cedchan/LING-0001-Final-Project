from bs4 import BeautifulSoup
import requests, os, re, json, time

folder_path = 'spoken_addresses/'
overwrite = True
link_head = 'https://www.presidency.ucsb.edu'

# inaugural addresses
# nav_link = 'https://www.presidency.ucsb.edu/documents/app-categories/spoken-addresses-and-remarks/presidential/inaugural-addresses'

# all spoken addresses
nav_link = 'https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks?items_per_page=60'

def request_persistant(link):
    try:
        page = requests.get(link)
        return page
    except:
        print('Request error. Retrying.')
        time.sleep(1)
        return request_persistant(link)

def save_file(data):
    global overwrite, folder_path

    last_name = re.sub('.* (.*)', '\g<1>', data['pres_name'])
    year = re.sub('(\d+)-\d+-\d+.*', '\g<1>', data['date'])
    title_clipped = re.sub('^((?:\w+\s?){1,5}).*', '\g<1>', data['title']).strip()
    save_name = folder_path + f'{year}_{last_name}_{title_clipped}.json'.replace(' ', '_')
    
    if os.path.exists(save_name) and not(overwrite):
        i = 1
        save_name += str(i)
        while os.path.exists(save_name):
            i += 1
            save_name = save_name[:len(save_name) - len(str(i - 1))] + str(i)
    
    with open(save_name, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if not(os.path.exists(folder_path)):
    os.makedirs(folder_path)

has_next_nav = True
while has_next_nav:
    nav = request_persistant(nav_link)
    nav_soup = BeautifulSoup(nav.text, 'lxml')
  
    page_link_containers = nav_soup.find_all(class_='field-title')
    # Searches for <a> within 'field-title' class, pulls 'href' and adds website head
    page_links = [link_head + container.find('a')['href'] for container in page_link_containers]

    for link in page_links:
        page = request_persistant(link)
        page_soup = BeautifulSoup(page.text, 'lxml')

        pres_name_raw = page_soup.find(class_='diet-title')
        pres_name = pres_name_raw.text.strip() if pres_name_raw is not None else ''

        byline_raw = page_soup.find(class_='diet-by-line president')
        byline = byline_raw.text.strip() if byline_raw is not None else ''

        title_raw = page_soup.find(class_='field-ds-doc-title')
        title = title_raw.text.strip() if pres_name_raw is not None else ''

        date_raw = page_soup.find(class_='date-display-single')['content']
        date = re.sub('(\d+-\d+-\d+).*', '\g<1>', date_raw).strip() if date_raw is not None else ''

        garbage_collected = []
        paragraph_containers = page_soup.find(class_='field-docs-content')
        paragraphs_raw = paragraph_containers.find_all('p')
        text_list = []
        for paragraph in paragraphs_raw:
            if len(paragraph.contents) > 1:
                contents = [c.text for c in paragraph.contents]
                content = ' '.join(contents)
            else:
                content = paragraph.text
            
            m = re.match('(.*)(\[.*\])(.*)', content)
            if bool(m):
                garbage_collected.append(m.group(2))
                content = m.group(1) + " " + m.group(3)

            content = re.sub('\s{2,}', ' ', content)
            text_list.append(content)
        text = '\n\n'.join(text_list)
        
        data = {
            'pres_name' : pres_name,
            'byline' : byline,
            'title' : title,
            'date' : date,
            'text' : text,
            'garbage_collected' : garbage_collected
        }

        save_file(data)

    next_container = nav_soup.find(class_='next')
    if next_container:
        next_stub = next_container.find('a')['href']
        nav_link = link_head + next_stub
    else: 
        has_next_nav = False