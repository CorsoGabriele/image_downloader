import re
import urllib.request
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # directory where the immages get saved
    print()
    path_img = input('Write the absolute path where to save the immages: ')
    print()

    # page with the threads
    main_url = "http://boards.4chan.org/wg/"
    url = main_url

    # page number to add to the url
    page = 1

    # list of the threads
    lista_link = []

    #do for every page of the site
    while page <= 10:
        
        print('Processing page {0} of 10'.format(page))

        # headers to connect to the wesite
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)

        # connection to the website
        resp = urllib.request.urlopen(req)
        html = resp.read()
        html.decode('utf-8')

        # research in the html code
        soup = BeautifulSoup(html, 'html.parser')
        lista_a = soup.find_all('a')

        # selection of all threads
        for element in lista_a:
            if 'thread' in element['href'] and not '#' in element['href'] and len(element['href']) > 14:
                lista_link.append(element.get('href'))

        # modify url to navigate throught the pages
        page += 1
        url = main_url + str(page)

    url = main_url

    print('')
    print('Opening the threads...')
    print('')

    # total number of threads
    n_thrd = len(lista_link)
    i = 1

    # in lista_link ci sono la parte di stringa da aggiungere all'url per entrare nel thread

    lista_img = []

    for element in lista_link:
        url_temp = url + element
        #print(url_temp)
        
        print('Thread {0} of {1}'.format(i, n_thrd))
        i += 1

        # connessione al thread e ricerca nell'html
        req_temp = urllib.request.Request(url_temp, headers = headers)
        resp_temp = urllib.request.urlopen(req_temp)
        html_temp = resp_temp.read()
        html_temp.decode('utf-8')
        soup_temp = BeautifulSoup(html_temp, 'html.parser')
        lista_trd = soup_temp.find_all('a')
        
        # ricerca delle immagini nell'html
        for img in lista_trd:

            # //is.4chan.org al posto di //i.4cdn.org a seconda del caso cambiarlo anche nel number_img
            if re.search('(.*\.png)', img['href']) or re.search('(.*\.jpg)', img['href']):

                # tolgo // per l'url 
                image_web = img['href'].replace("//", "")
                lista_img.append(image_web)


    # tolgo le immagini ripetue
    set_img = set(lista_img)
    tot_img = len(set_img)

    #print(set_img)
    print('')
    print('Saving the images...')
    print('')

    # contatore immagini
    x = 1

    for img in set_img:

        print('Image {0} of {1}'.format(x, tot_img))
        x += 1
        
        # creo l'url
        prefix = 'http://'
        link_img = prefix + img 
        
        # prendo il numero dell'immagine per usarlo come nome
        #number_img = img.replace("i.4cdn.org/wg/", "")
        number_img = img[(len(img)-17):]
        name_img = path_img + number_img

        # scarico l'immagine dal link_img in name_img
        urllib.request.urlretrieve(link_img, name_img)
