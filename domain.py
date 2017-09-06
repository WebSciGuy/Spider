from urllib.parse import urlparse


# Extract the domain, but also allow for .co.uk and other formats.
def get_domain_name(url):
    try:
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain
    except:
        return ''

#  code to test script
# print(get_domain_name('https://sussed.soton.ac.uk/cp/home/displaylogin'))