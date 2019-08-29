def get_line(filepath):
    return len(open(filepath).readlines())

def process_file(filepath,skip_header,client,feedback):
    with open(filepath) as f:
        usersfile = f.readlines()
        i = 0 
        for line in usersfile:
            i+=1
            printdku(i,feedback)
            if (skip_header and i==1): 
                continue
            printdku("Processing line %s" %line,feedback)
            userdetails = line.split(',')
            printdku("userdetails %s" %userdetails,feedback)
            try: 
                printdku("in try block")
                username = userdetails[0]
                printdku("username %s" %username)
                password = userdetails[1]
                display_name = userdetails[2]
                groups = userdetails[3].strip().split("|")
                printdku(username,password,display_name,groups)
                feedback = process_groups(groups,client,feedback)
                printdku("group processed")
                feedback = process_user(username,password,display_name,groups,client,feedback)
                printdku("Successfully processed user %s" %username,feedback)
            except: 
                printdku("Error processing line: %s" %line,feedback)
    return feedback


def process_groups(group_list,client,feedback):
    allgroups = client.list_groups()
    for group in group_list:
        try: 
            result = next (group for group in allgroups if group['name'] == group)
        except StopIteration as error: 
            client.create_group(group,group,"LOCAL")
            printdku("Created group %s" %group,feedback)
            return feedback
        else: 
            printdku("Error creating group %s" %group,feedback)
            return feedback

def process_user(username,password,display_name,groups,client,feedback):
    #grab user list here instead of before to ensure that we don't process duplicates in the file
    allusers = client.list_users()
    try:
        result = next(item for item in allusers if item['login'] == username)
    except StopIteration as error: #user doesn't already exist, create it
        new_user = client.create_user(username, password, display_name,'LOCAL', groups)
        printdku("Created user %s" %username,feedback)
        return feedback
    else:
        printdku("Error creating user %s" %username.feedback)
        return feedback

def printdku(string,feedback):
    print(string)
    feedback.append(string)