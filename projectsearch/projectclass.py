from projectsearch.projectsdata import output

class Projects:
    def __init__(self):
        self._list = output()

    @property
    def list(self):
        return self._list

    def get_project(self, team):
        projects = self.list
        for proj in projects:
            if team == proj["scrum_team"]:
                return proj
        return None

    def get_details(self, title):
        projects = self.list
        for proj in projects:
            if title == proj["title"]:
                return proj
        return None


if __name__ == '__main__':
    projects = Projects()

    print("Project Data")
    for project in projects.list:
        print(project["scrum_team"])
        print(project)
