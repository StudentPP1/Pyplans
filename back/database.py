from pymongo import MongoClient


class Database:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

        print(user_name, password)

        self.cluster = MongoClient("mongodb+srv://owner:8aYQ9MdvCAX2FcTS@cluster0.fclhicg.mongodb.net/?retryWrites=true&w=majority")
        self.collection = self.cluster["database_plans"]["plans"]

        if self.collection.count_documents({"user_name": self.user_name}) == 0 and \
                self.collection.count_documents({"password": self.password}) == 0:

            post = {"user_name": self.user_name,
                    "password": self.password,
                    "plans": {}}
            self.collection.insert_one(post)

        self.plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]

    def _update(self, plans):
        self.collection.update_one({"user_name": self.user_name, "password": self.password}, {"$set": {"plans": plans}})
        self.plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]

    def add_new_project(self, project_name: str):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans.update({project_name: {}})
        self._update(plans)

    def del_project(self, project_name: str):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans.pop(project_name)
        self._update(plans)

    def edit_project_name(self, old_name, new_name):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        items = plans.pop(old_name)
        plans[new_name] = items
        self.collection.update_one({"user_name": self.user_name, "password": self.password}, {"$set": {"plans": plans}})
        self._update(plans)

    def add_new_task(self, project, task):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans[project][task] = False
        self.collection.update_one({"user_name": self.user_name, "password": self.password}, {"$set": {"plans": plans}})
        self._update(plans)

    def del_task(self, project, task):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans[project].pop(task)
        self._update(plans)

    def edit_task(self, project, old_task, new_task):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans[project][new_task] = plans[project].pop(old_task)
        self._update(plans)

    def task_done(self, project, task):
        plans = self.collection.find_one({"user_name": self.user_name, "password": self.password})["plans"]
        plans[project][task] = True
        self._update(plans)
