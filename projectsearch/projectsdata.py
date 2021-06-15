# building basic template structure for filtering process


def wascwebsite():
    image = ""
    title = "WASC report"
    members = "Sriya Chilla", "Grace Le", "Iniyaa Mohanraj", "Isai Rajaraman", "Ridhima Inukurti"
    scrum_team = "walruses"
    trimester = 3
    keyword = "school"
    comlink = "#"  # Insert commercial link here
    gitlink = "#"  # Insert github repo link here
    runlink = "#"
    scrumlink = "#"
    readmelink = "#"
    description = "This website was built for the WASC committee in order to help them navigate to Del Norte"
    return filterdict(image, title, members, scrum_team, trimester, keyword, gitlink, comlink, runlink, scrumlink, readmelink, description)


def PieceofthePI():
    image = "piece_of_the_pi.png"
    title = "Piece of the PI"
    members = "Bradley Bartelt", "Diego Krenz", "DK Khalili-Samani", "Colin Szeto", "Andrew Zhang"
    scrum_team = "wave2"
    trimester = 3
    keyword = "statistics"
    gitlink = "#"
    comlink = "#"
    runlink = "http://pieceofthepi.pusdcoders.tk/"
    scrumlink = "#"
    readmelink = "#"
    description = "Our project is a pizza social media. To get the best slice of pizza. On our site you can leave reviews on pizza, chat with other users on pizza related topics, upload pictures of pizza, and navigate external pizza sites, all in one location."
    return filterdict(image, title, members, scrum_team, trimester, keyword, gitlink, comlink, runlink, scrumlink, readmelink, description)


def GamesFromtheDecades():
    image = ""
    title = "Games From the Decades"
    members = "Siddhant Ranka", "Kevin Hu", "Sean Tran", "Aditya Surapaneni", "Jacob Rozenkrants"
    scrum_team = "snakeyees"
    trimester = 3
    keyword = "statistics"
    gitlink = "#"
    comlink = "#"
    runlink = "#"
    scrumlink = "#"
    readmelink = "#"
    description = "This project allowed the user to play different video games from different decades. The games specifically were Minesweeper, Uno, and Go Fish."
    return filterdict(image, title, members, scrum_team, trimester, keyword, gitlink, comlink, runlink, scrumlink, readmelink, description)


def Covid19TeaShop():
    image = ""
    title = "Covid-19 Tea Shop"
    members = "Siddhant Ranka, Aidan Rosen, Andrew Hale, "
    scrum_team = "Coconuts"
    trimester = 2
    keyword = "Commerce adn Data"
    gitlink = "https://github.com/Siddhant8/p1-coconuts2"
    comlink = "https://drive.google.com/file/d/1stjN2g0_sbFWiXRue-2ZFMkNQsxnuwyK/view"
    runlink = "#"
    scrumlink = "#"
    readmelink = "https://github.com/Siddhant8/p1-coconuts2"
    description = "An online website was created to simulate an online tea shop. A coronavirus calculator was created to calculate cases during the covid pandemic, and a jukebox was created to make shopping more enjoyable."
    return filterdict(image, title, members, scrum_team, trimester, keyword, gitlink, comlink, runlink, scrumlink, readmelink, description)


def filterdict(image, title, members, scrum_team, trimester, keyword, gitlink, comlink, runlink, scrumlink, readmelink, description):
    row = {"image": image, "title": title, "members": members, "scrum_team": scrum_team, "trimester": trimester,
           "keyword": keyword, "gitlink": gitlink, "comlink": comlink, "runlink": runlink,
           "scrumlink": scrumlink, "readmelink": readmelink, "description": description}
    return row


def output():
    output_list = [wascwebsite(), PieceofthePI(), GamesFromtheDecades()]
    return output_list
