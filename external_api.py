from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


browser_options = Options()
#browser_options.add_argument("--headless")
driver = webdriver.Edge(options=browser_options)
url = "///?"
driver.get(url)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        expression = query_params.get('expression', None)

        if expression is not None:
            # wykonaj operacje na wyrażeniu
            result = str(expression[0])
            print(result)
            result = ChatHandler.SendQuestion(result)
            
            # przygotuj odpowiedź dla klienta
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<html><body><img src="{result}"></body></html>'.encode('utf-8'))
        else:
            # nie podano wyrażenia, zwróć błąd
            self.send_response(69)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Gdzie pytanko wariacie')

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()



class ChatHandler():
    
    def SendQuestion(question):
        driver.find_element(By.XPATH, "//input[@placeholder='Szukaj']").send_keys(question+"\n")

        #respond_element = driver.page_source.encode("utf-8")
        respond_element = driver.find_element(By.XPATH, "//span[@class='f-grid-12 img-wrap replace-img-list']/img")
        respond_element = respond_element.get_attribute("src")
        driver.find_element(By.XPATH, "//input[@placeholder='Szukaj']").clear()

        return respond_element





if __name__ == '__main__':
    run_server(8080)



#driver.get(base_url)
#print(driver.page_source.encode("utf-8"))

#input_el = driver.find_element(By.ID, 'tabelaHTML_filter')
#Found input then send it to chat :)



#Take output from operation
#output_el = driver.find_element(By.ID)
#And return it for client

#print(input_el)

#driver.quit()