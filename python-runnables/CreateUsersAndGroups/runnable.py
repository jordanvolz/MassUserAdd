import dataiku
import dataikuapi
import csv
import pprint
from pprint import pprint
#from pprint_data import data
# This file is the actual code for the Python runnable someidentifier
from dataiku.runnables import Runnable
#client = dataikuapi.DSSClient("localhost:11200", "6mvE00OPKblLSj88yzCaQefNKj1gs87Y")
#client = dataiku.api_client()

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
        filepath = self.config.get("user_file_location")
        with open(filepath) as f:
            usersfile = f.readlines()
            feedback = []
            for line in usersfile:
                userdetails = line.split(',')
                username = userdetails[0]
                allusers = self.client.list_users()
                try:
                    result = next(item for item in allusers if item['login'] == username)
                except StopIteration as error: 
                    username = userdetails[0]
                    password = userdetails[1]
                    display_name = userdetails[2]
                    usergroup = userdetails[3]
                    if len(userdetails)>4:
                        usergroup.append(userdetails[4])
                    new_user = self.client.create_user(username, password, display_name, source_type='LOCAL', groups=[usergroup])
                    nuser = (username + " has been created")
                    feedback.append(nuser)
                else:
                    alreadyused = (username + " is already in use - please use another name")
                    feedback.append(alreadyused)
                    continue

        final = ", ".join(feedback)
        return final


       
    
        