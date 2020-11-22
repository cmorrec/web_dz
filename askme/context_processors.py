def right_block(request):
    return {'bestMembers': bestMembers,
            'popularTags': popularTags,}

def is_login(request):
    return {'userName': userName,
        'isLogin': isLogin,}
