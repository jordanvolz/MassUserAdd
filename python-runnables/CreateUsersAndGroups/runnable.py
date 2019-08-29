import dataiku
from dataiku.runnables import Runnable


class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.client=dataiku.api_client()
        self.feedback=[]
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        
        printdku("Starting Macro MassUserAdd_CreateUserAndGroups")

        filepath = self.config.get("user_file_location")
        skip_header = self.config.get("skip_header")
        printdku("Processing file %s" %filepath)
        
        result = process_file(filepath,skip_header)
        
        printdku("Finished Macro MassUserAdd_CreateUserAndGroups")
        return "<br>".join(self.feedback)
    
    def process_file(filepath,skip_header):
        with open(filepath) as f:
            usersfile = f.readlines()
            i = 0 
            for line in usersfile:
                i+=1
                if (skip_header and i==1): continue
                printdku("Processing line %s" %line)
                userdetails = line.split(',')
                try: 
                    username = userdetails[0]
                    password = userdetails[1]
                    display_name = userdetails[2]
                    groups = userdetails[3]
                    process_groups(groups)
                    process_user(username,password,display_name,groups)
                    printdku("Successfully processed user %s" %username)
                except: 
                    printdku("Error processing line: %s" %line)
                    

    def process_groups(groups):
        group_list=groups.split("|")
        allgroups = self.client.list_groups()
        for (group in group_list):
            try: 
                result = next (group for group in allgroups if group['name'] == group)
            except StopIteration as error: 
                self.client.create_group(group,group,"LOCAL")
                printdku("Created group %s" %group)
            else: 
                printdku("Error creating group %s" %group)
            
    def process_user(username,password,display_name,groups):
        #grab user list here instead of before to ensure that we don't process duplicates in the file
        allusers = self.client.list_users()
        feedback = []
        try:
            result = next(item for item in allusers if item['login'] == username)
        except StopIteration as error: #user doesn't already exist, create it
            new_user = self.client.create_user(username, password, display_name,'LOCAL', groups)
            printdku("Created user %s" %username)
        else:
            printdku("Error creating user %s" %username)
            
    def printdku(string):
        print(string)
        self.feedback=append(string)
    
        