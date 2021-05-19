def populate_test_db_users(User,Group):
    dict1 = {'username':['common','sergeant','general','captain','president'],
             'password':['123456' for i in range(5)],
             'group':['user','sergeant','general','captain','president']
             }

    for index,username in enumerate(dict1['username']):
        password = dict1['password'][index]
        group = dict1['group'][index]
        user = User.objects.create_user(username=username,password=password)
        user_group = Group.objects.create(name=group)
        user.groups.add(user_group)


def populate_test_db_docs(Document):
    doc_dict = {'title':['public document','private document','secret document','top-secret document'],
                'date_expired':["2021-05-09" for i in range(4)],
                'status':['active' for i in range(4)],
                'document_root':['public','private','secret','top-secret']
                }
    for index,title in enumerate(doc_dict['title']):
        date_expired = doc_dict['date_expired'][index]
        status = doc_dict['status'][index]
        document_root = doc_dict['document_root'][index]
        Document.objects.create(title=title,date_expired=date_expired,status=status,document_root=document_root)