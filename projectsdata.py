#building basic template structure for filtering process

def project1:
    name = "bob"
    trimester = 1
    keyword = "monkey"
    link = "https:link/fake"

def project2:
    name = "joe"
    trimester = 3
    keyword = "wolf"
    link = "https:link/fake2"

def project3:
    name = "david"
    trimester = 1
    keyword = "dog"
    link = "https:link/fake3"

def project4:
    name = "gordon"
    trimester = 2
    keyword = "cat"
    link = "https:link/fake4"

def project5:
    name = "matt"
    trimester = 2
    keyword = "dog"
    link = "https:link/fake "

def project6:
    name = "ryan"
    trimester = 1
    keyword = "cat5
    link = "https:link/fake6"

def filterdict(name, trimester, keyword, link):
    output = {"name": name, "trimester": trimester, "keyword": keyword, "link": link}\
    return output

def output:
    outputlist = [project1(), project2(), project3(), project4(), project5(), project6()]

