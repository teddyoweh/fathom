from api import clutch
class apollo:
    def __init__(self):
        pass
    
    def people_search(self,keyword):
        
        scraper = clutch()
        return scraper.search_deep(keyword)