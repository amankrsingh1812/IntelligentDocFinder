from bs4 import BeautifulSoup
from urllib.request import urlopen


def filename(extension):
    """ 
    Returns sample file from the samples/ folder
    
    Arguments:
    extension - extension of the req doc
    """
    return f'samples/sample_{extension}.{extension}'

def html_to_text(file):
    """ 
    Returns an intermediate text file corresponding to the html file
    
    Arguments:
    file - HTML file
    
    Returns:
    'samples/sample_intermediate_txt.txt'
    """
    
    intermediate_file = 'samples/sample_intermediate_txt.txt'
    soup = BeautifulSoup(open(filename('html')), features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    txtFileObj = open(intermediate_file, 'w')
    txtFileObj.write(text)
    txtFileObj.close()

    return intermediate_file