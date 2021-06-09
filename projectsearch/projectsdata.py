#building basic template structure for filtering process
import json

def wascwebsite():
    image = ""
    title = "WASC report"
    members = "Sriya Chilla", "Grace Le" , "Iniyaa Mohanraj" , "Isai Rajaraman", "Ridhima Inukurti"
    scrum_team = "walruses"
    trimester = 3
    keyword = "school"
    comlink = "Insert commercial link here"
    gitlink = "Insert github repo link here"
    description = "This website was built for the WASC committee in order to help them navigate to Del Norte"
    return filterdict( title, members, scrum_team, trimester, keyword, gitlink, comlink, description)

def PieceofthePI():
    image = ""
    title = "Piece of the PI"
    members = "Bradley Bartelt", "Diego Krenz", "DK Khalili-Samani", "Colin Szeto", "Andrew Zhang"
    scrum_team = "Wave"
    trimester = 3
    keyword = "statistics"
    gitlink = ""
    comlink = ""
    description = ""
    return filterdict( title, members, scrum_team, trimester, keyword, gitlink, comlink, description)


def GamesFromtheDecades():
    title = "Games From the Decades"
    members = "Siddhant Ranka", "Kevin Hu", "Sean Tran", "Aditya Surapaneni", "Jacob Rozenkrants"
    scrum_team = "GroceryStore"
    trimester = 3
    keyword = "statistics"
    gitlink = ""
    comlink = ""
    description = ""
    return filterdict(title, members, scrum_team, trimester, keyword, gitlink, comlink, description)

def project4():
    title = ""
    members = ""
    scrum_team = ""
    trimester = 3
    keyword = ""
    gitlink = ""
    comlink = ""
    description = ""
    return filterdict(title, members, scrum_team, trimester, keyword, gitlink, comlink, description)

def project5():
    title = ""
    members = ""
    scrum_team = ""
    trimester = 3
    keyword = ""
    gitlink = ""
    comlink = ""
    description = ""
    return filterdict(title, members, scrum_team, trimester, keyword, gitlink, comlink, description)


def project6():
    title = ""
    members = ""
    scrum_team = ""
    trimester = 3
    keyword = ""
    gitlink = ""
    comlink = ""
    description = ""
    return filterdict(title, members, scrum_team, trimester, keyword, gitlink, comlink, description)

def filterdict(title, members, scrum_team, trimester, keyword, gitlink, comlink, description):
    row = {"title": title, "members": members, "scrum_team": scrum_team, "trimester": trimester, "keyword": keyword, "gitlink": gitlink, "comlink": comlink, "description": description}
    return row

def output():
    outputlist = [wascwebsite(), PieceofthePI(), GamesFromtheDecades()]

#    for row in outputlist:
#        row['keys'] = row["keyword"]
#
    #list of the projects will have CATEGORY data filter
#    category = {"key": "category", "data": [], "default": 'OTHER'}
#    filters = [category]

#    for data_filter in filters:
#        temp_list = []
 #       for row in outputlist:
  #          keys = row[data_filter["key"]].split()
   #         for key in keys:
    #            if key.lower() !=data_filter["default"].lower():
     #               temp_list.append(key)

      #  temp_list = list(set(temp_list))
       # temp_list.sort()
        #temp_list.insert(0, data_filter["default"])
        #data_filter["data"] = temp_list

    #return rows, filters
    return outputlist