import dataiku
import adminfunctions as admin
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
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        i = admin.get_lines(self.config.get("user_file_location"))
        return (i,None)

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        client=dataiku.api_client()
        feedback=[]
        
        admin.printdku("Starting Macro MassUserAdd_CreateUserAndGroups",feedback)

        filepath = self.config.get("user_file_location")
        skip_header = self.config.get("skip_header")
        admin.printdku("Processing file %s" %filepath,feedback)
        
        feedback = admin.process_file(filepath,skip_header,client,feedback,progress_callback)
        
        admin.printdku("Finished Macro MassUserAdd_CreateUserAndGroups",feedback)
        return "<br>".join(feedback)
    

    
        