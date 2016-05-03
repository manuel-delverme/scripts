import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import selenium
from selenium import webdriver
from pyvirtualdisplay import Display

FOLDER_ID = "0B2sLP-kqnlMWRE11WDNHeHJXV28"

def upload_file(drive, file_path):
    file_name = file_path.split("/")[-1]
    uploaded_file = drive.CreateFile({
                "title": file_name, 
                "parents":  [ {"id": FOLDER_ID} ],
                "mimeType": "application/pdf"
            })
    uploaded_file.SetContentFile(file_path)
    uploaded_file.Upload()

def main():
    file_path = sys.argv[1]

    # display = Display(visible=0, size=(800, 600))
    # display.start()

    browser = webdriver.Firefox()
    browser.get('https://idp.polito.it/idp/x509mixed-login')
    
    username = selenium.find_element_by_id("j_username")
    password = selenium.find_element_by_id("j_password")

    username.send_keys("s186541")
    password.send_keys("mappamondo01")

    selenium.find_element_by_name("submit").click()
    browser.get('https://didattica.polito.it/pls/portal30/sviluppo.chiama_materia?cod_ins=06LSLLM&incarico=204685')
    browser.get('https://didattica.polito.it/pls/portal30/sviluppo.pagina_corso.main?t=3')
    content = browser.find_element_by_css_selector('#filesDiv > table > tbody > tr > td > a')

    #tidy-up
    browser.quit()
    # display.stop() # ignore any output from this.

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("cred.json")
    drive = GoogleDrive(gauth)
    upload_file(drive, file_path)

# main()

# display = Display(visible=1, size=(1200, 1200))
# display.start()

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/tmp')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')

browser = webdriver.Firefox(profile)
browser.get('https://idp.polito.it/idp/x509mixed-login')

username = browser.find_element_by_id("j_username")
password = browser.find_element_by_id("j_password")

username.send_keys("s186541")
password.send_keys("mappamondo01")

password.submit()

link = "Portale della Didattica"
browser.find_element_by_xpath("//a[contains(text(), '{}')]".format(link)).click()

link = "Automatic control"
browser.find_element_by_xpath("//a[contains(text(), '{}')]".format(link)).click()

# link = "Materiale",
browser.get('https://didattica.polito.it/pls/portal30/sviluppo.pagina_corso.main?t=3')

link = "Lesson Handouts"
browser.find_element_by_xpath("//a[contains(text(), '{}')]".format(link)).click()

pdfs = browser.find_elements_by_css_selector('#filesDiv > table > tbody > tr > td > a')

for pdf in pdfs:
    browser.get(pdf.get_attribute("href"))
