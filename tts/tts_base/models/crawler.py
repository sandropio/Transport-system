
from requests import session
from bs4 import BeautifulSoup
import base64
import rsa
import psycopg2
import types



try:
    conn = psycopg2.connect("dbname = 'tts' user = 'odoo' host = 'localhost' password = ''")
except:
    print("შეცდომა")



def download_file(requests,url,job_id):
    try:
        curs = conn.cursor()
        curs.execute(f"SELECT job_no FROM tts_parcel WHERE job_no='{job_id}'")
        job=curs.fetchall()
    except:
        print("შეცდომა")




    if job:
        response_text = requests.get(url)
        html = BeautifulSoup(response_text.content, "html.parser")
     # print(html)
        div=html.find('div', {"class": "tx-shipment-tracking"},recursive=True)
        links=div.findAll("li")

        addresses = []
        addresses.append(job_id)
        for link in links:
            download_link=link.findChildren("a")[0].attrs.get("href")

            file_name=link.findChildren("a")[0].text
            local_filename = '/home/davit/uploads/' + file_name

            # downloaded = check_if_downloaded(local_filename,job_id)
            downloaded = False

            if downloaded:
                continue

            if not downloaded:
                addresses.append(file_name)
                with requests.get(download_link, stream=True) as r:
                    # local_filename = settings.MEDIA_ROOT + '/uploads/' + file_name

                    try:
                        print ("opaa")
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)
                    except Exception as e:
                        print(e)
        print(addresses)
        return addresses




def my_crawler():


    with session() as s:
        payload = {
            'user': 'k#001',
            'pass': '36fiu124a',
            'logintype': 'login',
            'pid': "13,20",
            'redirect_url': 'https://www.ah-logistik.de/services/sendungsverwaltung/',
            'tx_felogin_pi1[noredirect]':'0'

        }

        key_resp = s.get('https://www.ah-logistik.de/index.php?eID=RsaPublicKeyGenerationController')
        key = key_resp.content.decode('utf-8')
        
        key_parts = key.split(":")
        key_last = int(key_parts[1], 16)
        key_first = int(key_parts[0], 16)

        encrypted = rsa.encrypt(b'36fiu124a', rsa.PublicKey(key_first, key_last))
        # message to encrypt is in the above line 'encrypt this message'
        rsa_code = "rsa:" + base64.b64encode(encrypted).decode('utf-8')

        payload['pass'] = rsa_code
        # print("sfdklfksdfds", rsa_code)

        x=s.post("https://www.ah-logistik.de/services/", data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        post_response_text = s.get("https://www.ah-logistik.de/services/sendungsverwaltung/?tx_shipmenttracking_frontend%5Bcustomer%5D=1&tx_shipmenttracking_frontend%5Baction%5D=listClosed&tx_shipmenttracking_frontend%5Bcontroller%5D=Shipment&cHash=0afec17c48a3f5e42fc1eefda3db9700")
        # print(post_response_text.text)
        html = BeautifulSoup(post_response_text.content, "html.parser")
        # print(html)
        table =html.findAll('table', {"class":"table table-striped shipment-table"}, recursive="True")
        rows=table[0].findAll('tr')[1:]
        addresses=[]
        for i in rows:
            try:
                job_id=str((i.findAll("td")[6]).text).split(" ")[1]
            except:
                continue
            if job_id:
                download_link=i.find("a").attrs.get('href')
            if download_link:
                try:
                   x= download_file(s,download_link,job_id)
                   if x:
                        addresses.append(x)

                except Exception :
                    print("va")
                    # logger.error("Error Importing Docs for %s!!!", job_id)

            else:
                pass
        return addresses



if __name__ == "__main__":
  addresses_list=my_crawler()

  for addresses in addresses_list:

      for address in addresses[2::]:
        job_no=addresses[0]
        file_name=addresses[1]
        print("ჯობის ნომერი", job_no,"მისამართი" ,address)






