class Tower:

    def __init__(self,content):
        self.content = content

    def height(self):
        return len(self.content)

    def isFull(self):
        return self.height() == 5
    
    def getColor(self):
        if self.height() == 0:
            return "None"
        return self.content[self.height()-1]
    
    def getContent(self):
        return self.content

    def addContent(self,content):
        """Return True/False if movement possible"""
        if(len(content)+self.height() > 5):
            return False 
        self.content.append(content)
        return True

    def removeContent(self):
        contentRemoved = self.content
        self.content = []
        return contentRemoved
        
    
        