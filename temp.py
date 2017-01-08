
def classify_post(users):
    """
    Function to classify whether a comment is a global poke, personal poke, friend poke or a combination of all
    Returns 
    0 - personal poke - nothing in users
    1 - global poke - global
    2 - friend poke - friend user name
    3 - global and friend poke - global and username specified
    4 - 
    """
    if users == '' or users == ' ':
        return 0
    all_users = users.split(' ')
    user_list = []
    global_flag = 0
    friend_flag = 0
    print(all_users)
    for u in all_users:
        if u == 'global':
            global_flag = 1
        else:
            friend_flag = 1
            user_list.append(u)

    print(global_flag, friend_flag)
    if global_flag == 1 and friend_flag == 1:
        return tuple((3, user_list))
    elif global_flag == 1:
        return 1
    elif friend_flag == 1:
        return tuple((2,user_list))

if __name__ == '__main__':
    print(classify_post('global ukshah2'))