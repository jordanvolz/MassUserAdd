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
    for group in group_list:
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