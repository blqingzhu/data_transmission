if __name__ == '__main__':
    register_status=0
    print(lambda: register_status == 0, "手机号获取验证码失败")
    register_status=40
    print(lambda: register_status == 0, "手机号获取验证码失败")

    print(lambda: register_status == 0, "手机号获取验证码失败")
