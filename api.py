import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

class clutch:
    def __init__(self):
        self.headers = {
            "authority": "www.linkedin.com",
            "method": "GET",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Cookie": open("cok.txt").read()
        }

    def get_profile_data(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        code_tags = soup.find_all('code')
        open('test.html','w').write(str(soup))
        def _get_birthDateOn_index_tags(code_tags):
            for _ in range(len(code_tags)):
                if "birthDateOn" in code_tags[_].text.strip('\n').replace('null', 'None').replace('false', 'False').replace('true', 'True'):
                    return _
 
        code_content = code_tags[_get_birthDateOn_index_tags(code_tags)].text.strip('\n').replace('null', 'None').replace('false', 'False').replace('true', 'True')
        profile_data = eval(code_content)['included']
        self.profile_data = profile_data
        
        def _get_birthDateOn_index(included_list):
            for index, item in enumerate(included_list):
                if 'birthDateOn' in item:
                    return index

        data = profile_data[_get_birthDateOn_index(profile_data)]
        
        return self._extract_profile_data(data)

    def _extract_profile_data(self, data):
        x =  {
            'first_name': data['multiLocaleFirstName'][0]['value'],
            'last_name': data['lastName'],
            "name": data['multiLocaleFirstName'][0]['value'] + ' ' + data['lastName'],
            'birthDateOn': data['birthDateOn'],
            'headline': data['headline'],
            'username': data['publicIdentifier'],
            'pronoun': data['pronoun'],
            'influencer': data['influencer'],
            "linkedin_url": f"https://www.linkedin.com/in/{data['publicIdentifier']}",
            
        }
 
        contactinfo = self._get_profile_contact(x['username'])
        x.update(contactinfo)
        return x
        
    def get_posts(self, url):
        url = "https://www.linkedin.com/in/teddyoweh/recent-activity/all/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        code_tags = soup.find_all('code')
        data =soup.find('div',class_='scaffold-finite-scroll__content').find('ul').find_all('li',class_='profile-creator-shared-feed-update__container')    
        print(len(data))
        posts = []
        for x in range(len(data)):
            try:
                item =data[x].find('div',id='fie-impression-container')
                post = {}
            
                post['poster_name'] = item.find('span', class_='update-components-actor__name').text.strip()
                post['post_text'] = item.find('div', class_='update-components-text relative update-components-update-v2__commentary').text.strip()
                post['date'] = item.find('span', class_='update-components-actor__sub-description').text.strip()
                post['images'] = []
                image_links = item.find_all('img', class_='ivm-view-attr__img--centered')
                for image in image_links:
                    post['images'].append(image['src'])
                
                posts.append(post)
            except:
                pass
        return posts  
 
    def _get_profile_contact(self, username):
        url = f"https://www.linkedin.com/in/{username}/overlay/contact-info/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        code_tags = soup.find_all('code')
        open('test.html','w').write(str(soup))
        def _get_birthDateOn_index_tags(code_tags):
            for index, tag in enumerate(code_tags):
                if "325d8aa60877c5d1a8cc282d5c2e2e50" in tag.text.strip('\n').replace('null', 'None').replace('false', 'False').replace('true', 'True'):
                    return index
            return None

        index = _get_birthDateOn_index_tags(code_tags)
        if index is None:
            return None

        code_content = code_tags[index].text.strip('\n').replace('null', 'None').replace('false', 'False').replace('true', 'True')
        profile_data = eval(code_content)['included']

        def _get_birthDateOn_index(included_list):
            for index, item in enumerate(included_list):
                if 'birthDateOn' in item:
                    return index
            return None

        index = _get_birthDateOn_index(profile_data)
        if index is None:
            return None

        profile_data = profile_data[index]

        def extract_profile_data(data):
            result = {}
            if data['emailAddress'] is not None:
                result['email']=data['emailAddress']["emailAddress"]
 
            for website in data['websites']:
                if 'github' in website['url'].lower():
                    result['github'] = website['url']
                elif 'linkedin' in website['url'].lower():
                    result['linkedin'] = website['url']
                elif 'twitter' in website['url'].lower():
                    result['twitter'] = website['url']
                elif 'facebook' in website['url'].lower():
                    result['facebook'] = website['url']
                elif 'dribbble' in website['url'].lower():
                    result['dribbble'] = website['url']
                elif 'behance' in website['url'].lower():
                    result['behance'] = website['url']
                else:
                    result[website['category'].lower()] = website['url']
            return result
        return extract_profile_data(profile_data)

            
    def _search(self, keyword,deep=1):
        result = []
        for i in range(1,deep+1):
            self.url = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=CLUSTER_EXPANSION&page={i}&sid=oJC"
            response = requests.get(self.url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            code_tags = soup.find_all('code')
            code_content = code_tags[16].text.strip('\n').replace('null', 'None').replace('false', 'False').replace('true', 'True')

            users_data = eval(code_content)['included']
            new_data = users_data[self._get_upsell_card_index(users_data)[0]:self._get_upsell_card_index(users_data)[1]]

    
            for item in new_data:
                result.append(self._extract_data(item))

        return result

    def search(self, keyword,deep=1):
        try:
            return self._search(keyword,deep=deep)
        except:
            return self.search(keyword,deep=deep)

    def _get_upsell_card_index(self, included_list):
        a, z = 0, 0
        for index, item in enumerate(included_list):
            if 'template' in item:
                a = index
                break
        for index, item in enumerate(included_list[::-1]):
            if 'template' in item:
                z = len(included_list) - index
                break
        return a, z

    def _extract_data(self, data):
        return {
            'Name': data['title']['text'],
            'location': data['secondarySubtitle']['text'],
            'profile': data['navigationUrl'].split('?')[0]
        }
    
    def search_deep(self, keyword,deep=1):
        users = self.search(keyword,deep=deep)
        result = []
        for user in users:
            try:
                result.append([user,self.get_profile_data(user['profile'])])
            except Exception as e:
                print(e)
                pass
        return result


scraper = clutch()

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to LinkedIn Scraper API'})

@app.route('/search', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type', 'Accept','Access-Control-Allow-Origin'])
def search():
    keyword = request.json.get('keyword')
    print(keyword   )
    if not keyword:
        return jsonify({'error': 'Keyword parameter is required'}), 400
    
    data = scraper.search(keyword)
    return jsonify(data)

@app.route('/profile', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type', 'Accept','Access-Control-Allow-Origin'])
def profile():
    username =  request.json.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    url = f"https://www.linkedin.com/in/{username}"
    data = scraper.get_profile_data(url)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
