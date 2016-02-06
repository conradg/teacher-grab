import urllib.parse
import urllib.request
import requests
import webbrowser

##############################
######## program outline######
##############################

# 1. Load GreatSchools.org search result for given url    DONE
# 2. Extract all school names on page from HTML           DONE
# 3. For each school:
#   a. Find homepage using google I'm feeling lucky.      DONE
#   b. Determine if finalsite, if not, skip.              DONE
#   c. Find faculty page from HTML                        DONE
#   d. Search for music/performing arts staff.            DONE
#   e. Extract name and e-mail of each staff member.      DONE
# 4. Send template e-mail to all staff

great_schools_url = "http://www.greatschools.org/search/search.page?distance=60&gradeLevels=e&gradeLevels=m&gradeLevels=h&st=private&lat=35.3732921&lon=-119.01871249999999&state=CA&locationType=locality,political&normalizedAddress=Bakersfield,%20CA&totalResults=1&locationSearchString=Bakersfield&city=Bakersfield&sortBy=DISTANCE&pageSize=100"

# returns all school names in greatschools search result html
def get_schools(html):
    split_html = html.split('''<div id="school-search-result-link''')[1:]
    school_towns = []
    for entry in split_html:
        link_start = entry.find("<a href")
        link_onwards = entry[link_start:]
        name_start = link_onwards.find(">") + 1
        name_end   = link_onwards[1:].find("<") + 1
        name = link_onwards[name_start:name_end]

        city_class = '''<div class="js-school-search-result-citystatezip small bottom">'''
        city_start = link_onwards.find(city_class) + len(city_class)
        city_end   = link_onwards.find(",")
        city = link_onwards[city_start:city_end]

        school_towns.append((name, city))

    return school_towns

# returns all staff names and emails from filtered page
def get_name_emails(html):
    return [()]


# returns the filtered faculty by a given keyword
def filter_faculty(url,keyword):

    values = {'keyword' : keyword}
    data = urllib.parse.urlencode(values)

    data = data.encode('ascii')

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)

    return response.read().decode('utf-8')


# detects if it is a finalsite. Many schools use finalsite to store their
# faculty information, and it has a predictable format that we can exploit
def is_finalsite(html):
    return '<meta name="poweredby" content="finalsite.com">' in html



# given the school homepage returns the faculty page url
def get_faculty_url(school_url):
    html = url_to_html(school_url)
    return html


# Returns URL of the first google hit for a search term.
def feeling_lucky(search_term):
    var = requests.get(r'https://www.google.com/search?q=' + search_term + '&btnI=I')
    return var.url


# evaluates a url to an html string
def url_to_html(url):
    return urllib.request.urlopen(url).read().decode('cp1252')



def main():
    great_schools_list_html = url_to_html(great_schools_url)
    schools = get_schools(great_schools_list_html)
    for (school,city) in schools:
        url = feeling_lucky(school + " school " + city)
        print(url)
        if "google" in url: continue
        html = url_to_html(url)
        if not is_finalsite(html):
            continue
        webbrowser.open_new_tab(url)
        print (school, "uses finalsite");
        break
        faculty_url = get_faculty_url(url) # NOT IMPLEMENTED
        music_faculty_html = filter_faculty(faculty_url, "music")
        contacts = get_name_emails(music_faculty_html) # NOT IMPLEMENTED


main()

































