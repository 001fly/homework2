username = input("username:") # 用户输入用户名字(username)
userquit = input("If you want to quit, 'q'!\n"
                  "If you want to continue 'c':")  # 可以随时选择退出('q')和继续('c')

if userquit=='q':# 退出
    exit()
else:# 如果不是第一次写入
    # 输出上次的余额以及购买记录
    userquit=='c'# 继续
    f_user=open('user.txt','r',encoding="utf-8")
    userlist = f_user.read().split("#")
    user_dic={}
    for item in userlist:
        item_list=item.split(":")
        user_dic[item_list[0]]=item_list[1]
    if username in user_dic:  #如果不是新用户
        userpass = input("password:")  #输入用户密码(userpassword)
        if username+':'+userpass in userlist:
            index_user=userlist.index(username+':'+userpass)  # 获取用户账号所在列表中的序列号
            f_cart = open('shopcart.txt', 'r', encoding="utf-8")
            f_cart_list=f_cart.read().split("$")  #把购物车文件的内容转化为以"$"来划分的列表
            output = f_cart_list[index_user + 1]  # 在购物车列表中取对应的序列号+1的值为购物记录
            print(output)
            output_list = output.split("\n")
            usersalary_list_spilt = output_list[0].split(" ")
            usersalary = int(usersalary_list_spilt[2])  # 再将写有余额的那一行以"\n"分隔为列表，取出余额值存入变量中
        else:
            print("密码错误，请重新输入:")
    else:
        print("This is your first landing")
        userpass = input("创建用户密码：")  # 创建新用户密码q
        usersalary = input("工资：")  # 输入工资
        f_user = open('user.txt', 'a+', encoding="utf-8")
        user_list = username + ":" + userpass
        f_user.write("#"+user_list)  # 以一定格式添加用户信息
        f_cart = open('shopcart.txt', 'a+', encoding="utf-8")
        f_cart.write("\n")
        usersalary_list = "$" + "Balance is " + usersalary + "\n"  # 将余额以一定格式写入到购物车文件中
        f_cart.write(usersalary_list)
f_cart.close()
f_user.close()
while True:
    fgoods_file = open("Goodslist_file.txt", "r", encoding="utf-8")
    for line_good in enumerate(fgoods_file.readlines()):
        print(line_good)  # 带有序列号的打印购物商品文件
    # goods_file_list = f_goods_file.readlines()
    user_choice = input("Please input the number of your goods you want to buy\n"
                        "If you want to inquire expense, Please input 's'\n"
                        "If you want to quit, Please input input 'q':")  # 交互界面
    if user_choice == "q":  # 退出
        exit()
    elif user_choice == "s":  # 查询消费记录
        f_cart = open('shopcart.txt', 'r', encoding="utf-8")
        #f_user = open('user.txt', 'a+', encoding="utf-8")
        inquire_user_list =username + ":" + userpass
        index_user_cart = userlist.index(inquire_user_list)
        # 取出对应的用户在用户文件中的列表的序列号便于在购物车文件中寻找对应的值
        f_cart_list = f_cart.read().split("$")  # 在购物车文件中以"$"划分为列表
        print(f_cart_list[index_user_cart+1])  # 取出对应的值就是用户对应的购物记录
        f_cart.close()
        f_user.close()

    else: #购物功能
        fgoods_file = open("Goodslist_file.txt", "r", encoding="utf-8")
        goods_list = fgoods_file.readlines()
        goods_price = goods_list[int(user_choice)].split(" ")  # 解析商品文件
        goods_name = goods_price[0]
        goods_price = int(goods_price[1])  # 取出购买的商品的名字以及价格
        usersalary = int(usersalary) - goods_price  # 与用户的工资或者余额进行减法
        if usersalary < 0:
            print("your balance is not enough...")
            continue  # 余额不够
        else:
            f_cart = open('shopcart.txt', 'r+', encoding="utf-8")
            f_user = open('user.txt', 'r', encoding="utf-8")
            f_cart_list=f_cart.read().split("$")
            userlist=f_user.read().split("#")
            user_item = username + ":" + userpass
            index_user=userlist.index(user_item)
            f_cart_add=f_cart_list[index_user+1]
            # 找到对应用户所在购物车文件中对应的余额以及购买记录信息位置
            f_cart_newlist=f_cart_add.split("\n")
            # 将余额信息还有购物信息记录用"\n"划分为列表，以便于后面添加商品在列表中
            f_cart_newlist.append(goods_list[int(user_choice)])
            # 从商品文件列表中取出商品添加商品到购物车列表中
            f_cart.write(" "+str(f_cart_newlist[2:]))
            # 以字符串的形式写入文件中，对列表进行切片，只读取有购物记录的部分
            print("\033[31;1mYour balance is: %s\033[0m\n"
                  "\033[31;1mThe goods '%s' has been added on the cart_list...\033[0m" %
                  (usersalary, goods_name))
            # 高亮显示余额以及当前购买的商品名字
            f_cart.close()
            # 下面是更新购物车列表中的余额
            f_cart = open('shopcart.txt', 'r', encoding="utf-8")
            file_data = ""
            # 用于存储更新之后的文件内容
            count = 0
            for line_cart in f_cart:
                if "$Balance" in line_cart:  # 用于记录$Balance出现的次数
                    count += 1
                    if count == index_user+1:  # 如果正好$Balance出现的次数和对应的第几个用户对应
                        line_cart = line_cart.replace(line_cart, "$Balance is " + str(usersalary) + "\n")
                        # 将这一行更新，余额更新
                file_data += line_cart  # 存储进file_data中
                f_cart = open('shopcart.txt', 'r+', encoding="utf-8")
                f_cart.write(file_data)  # 将file_data 重新写入到购物车文件中
                f_cart.close()
            fgoods_file.close()
            f_user.close()

