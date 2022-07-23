from http.server import BaseHTTPRequestHandler, HTTPServer
from inspect import Attribute
import time
import csv
import requests
from bs4 import BeautifulSoup

hostName = "localhost"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
                finalArr = []
                for i in range(19):
                    z = i+1
                    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"+str(z)
                    print("URL", url)


                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

                    r = requests.get(url =url, headers= headers)
                    htmlcontent = r.content
                    soup = BeautifulSoup(htmlcontent, 'html.parser')
                    # print(soup.body.prettify())

                    #NAMES and URLS
                    anchors = soup.find_all('a', class_ ='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
                    Names = []
                    Urls = []
                    for anchor in anchors:
                        Names.append(anchor.text)
                        Urls.append("https://www.amazon.in"+anchor.get('href'))
                    
                    print("Names",Names)

                    print("\n")
                    print("\n")
                    print("\n")
                    print("Urls", Urls)


                    #Ratings
                    print("\n")
                    print("\n")
                    print("\n")

                    ratings = soup.find_all('i', class_ ='a-icon a-icon-star-small a-star-small-4 aok-align-bottom')
                    RatingArr = []
                    for rating in ratings:
                        RatingArr.append(rating.text)

                    print("Ratings",RatingArr)

                    #Reviews
                    print("\n")
                    print("\n")
                    print("\n")

                    reviews = soup.find_all('a', class_ ='a-link-normal s-underline-text s-underline-link-text s-link-style')
                    ReviewArr = []
                    for review in reviews:
                        reviewsSpan = review.find("span", class_ = "a-size-base s-underline-text")
                        if reviewsSpan and reviewsSpan.text:
                            ReviewArr.append(reviewsSpan.text)
                        

                    print("Reviews",ReviewArr)


                    #Price
                    print("\n")
                    print("\n")
                    print("\n")

                    prices = soup.find_all("a", class_ = "a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
                    PriceArr = []
                    for price in prices:
                        pricesSpan = price.find("span", class_ = "a-offscreen")
                        PriceArr.append(pricesSpan.text) 

                    print("Price",PriceArr)

                    


                    fields = ['Name', 'Url', 'Ratings', 'Reviews', 'Price'] 
                    csvArray = []
                    for x in range(len(Names)):
                        print("x", x)
                        tempArr = []
                        tempArr.append(Names[x])
                        if((len(Urls)-1) >= x ):
                            tempArr.append(Urls[x])
                        if((len(RatingArr)-1) >= x ):
                            tempArr.append(RatingArr[x])
                        if((len(ReviewArr)-1) >= x ):
                            tempArr.append(ReviewArr[x])
                        if((len(PriceArr)-1) >= x ):
                            tempArr.append(PriceArr[x])
                        csvArray.append(tempArr);

                    print("arrrayddd", csvArray)
                    finalArr = finalArr + csvArray

                filename = "scraper_data.csv"
        
    # writing to csv file 
                with open(filename, 'w', encoding="utf-8") as csvfile: 
            # creating a csv writer object 
                        csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
                        csvwriter.writerow(fields) 
                
            # writing the data rows 
                        csvwriter.writerows(finalArr)


            #add content here

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
                self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")