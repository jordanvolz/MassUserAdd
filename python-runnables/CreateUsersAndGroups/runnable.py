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
        
        print("Starting Macro MassUserAdd_CreateUserAndGroups")

        filepath = self.config.get("user_file_location")
        skip_header = self.config.get("skip_header")
        print("Processing file %s" %filepath)
        
        result = process_file(filepath,skip_header)
        
        print ("Finished Macro MassUserAdd_CreateUserAndGroups")
        return result
    
    def process_file(filepath,skip_header):
        with open(filepath) as f:
            usersfile = f.readlines()
            for line in usersfile:
                userdetails = line.split(',')
                try: 
                    username = userdetails[0]
                    password = userdetails[1]
                    display_name = userdetails[2]
                    groups = userdetails[3]
                    process_groups(groups)
                    process_user(username,password,display_name,groups)
                    print("Successfully processed user %s" %username)
                except: 
                    print("Error processing line: %s" %line)
                    
        final = ", ".join(feedback)

    def process_groups():
        group_list=groups.split("|")
        for (group in group_list):
            process_group(group)
            
    def process_user(username,password,display_name,groups):
        #grab user list here instead of before to ensure that we don't process duplicates in the file
        allusers = self.client.list_users()
        feedback = []
        try:
            result = next(item for item in allusers if item['login'] == username)
        except StopIteration as error: #user doesn't already exist, create it
            if len(userdetails)>4:
                usergroup.append(userdetails[4])
            new_user = self.client.create_user(username, password, display_name, source_type='LOCAL', groups=[usergroup])
            nuser = (username + " has been created")
            feedback.append(nuser)
        else:
            alreadyused = (username + " is already in use - please use another name")
            feedback.append(alreadyused)
            continue 
    
        