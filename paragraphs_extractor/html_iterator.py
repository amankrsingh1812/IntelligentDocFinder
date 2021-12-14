from bs4 import BeautifulSoup
from paragraphs_extractor.file_iterator_interface import FileIteratorInterface

class HTMLIterator(FileIteratorInterface):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
        soup = BeautifulSoup(open(filename), features="html.parser")

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
        for chunk in chunks:
            chunk = chunk.replace('\n', '')
            if chunk:
                self.paragraphs.append(chunk)