from projectsearch.projectsdata import output

class Projects:
    def __init__(self):
        self._list = output()

    @property
    def list(self):
        return self._list

    @property
    def filters(self):
        return self.filters

    def get_project(self, team):
        projects = self.list
        for proj in projects:
            if team == proj["scrum_team"]:
                return proj
        return None


if __name__ == '__main__':
    projects_object = Projects()

    #print("Filters")
    #for filter_tag in projects_object.filters:
        #print(filter_tag)

    print("Project Data")
    for project in projects_object._list:
        print(project)
        print(project["scrum_team"])
