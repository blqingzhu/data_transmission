import random

# 所有大小写字母
import string


# 所有手机号前缀
phon_prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
                "155", "156", "157", "158", "159", "186", "187", "188"]

# 1 姓氏（所有姓氏）
NAME_XING = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
             '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
             '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
             '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
             '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
             '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
             '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危',
             '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '锺', '徐', '丘', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍',
             '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓',
             '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁',
             '荀', '羊', '於', '惠', '甄', '麹', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫',
             '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫',
             '甯', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司', '韶',
             '郜', '黎', '蓟', '薄', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙',
             '池', '乔', '阴', '鬱', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵',
             '冉', '宰', '郦', '雍', '郤', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦', '尚', '农',
             '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎',
             '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄', '阙', '东',
             '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚',
             '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '后', '荆', '红',
             '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫',
             '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '锺离', '宇文',
             '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官', '司寇', '仉', '督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正',
             '壤驷', '公良', '拓跋', '夹谷', '宰父', '穀梁', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '段干', '百里', '东郭', '南门',
             '呼延', '归海', '羊舌', '微生', '岳', '帅', '缑', '亢', '况', '後', '有', '琴', '梁丘', '左丘', '东门', '西门', '商', '牟',
             '佘', '佴', '伯', '赏', '南宫', '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '第五', '言', '福']
# 2 名字
MING = ['壮', '昱杰', '开虎', '凯信', '永斌', '方洲', '长发', '可人', '天弘', '炫锐', '富明', '俊枫', '小玉', '蓝', '琬郡', '琛青', '予舴', '妙妙', '梓茵',
        '海蓉', '语娜', '馨琦', '晓馥', '佳翊']


# 随机字符串
def random_string():
    string_len = random.randint(6, 12)  # 指定一个范围随机取整数
    return ''.join(random.sample(string.ascii_letters + string.digits, string_len))
    # return ''.join(random.sample(ran_str, num))


# 随机生成手机号码
def phoneNO():
    return random.choice(phon_prelist) + "".join(random.choice("0123456789") for i in range(8))


def random_emil():
    email_len = random.randint(6, 12)  # 指定一个范围随机取整数
    email_end = random.choice(('@163.com', '@qq.com', '@sina.com', '@126.com'))  # 随机取一个元素
    # 在小写、大写、特殊字符、数字里分别每样取一个字符，长度为4
    email_s = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase) + random.choice(
        string.punctuation) + random.choice(string.digits)
    # 剩下的2-8个字符在大小写、特殊字符、数字中随机取出来
    str = string.digits + string.punctuation + string.ascii_letters
    str_len = email_len - 4
    email_e = random.sample(str, str_len)  # 随机选取几个元素，返回list
    email_start = list(email_s) + email_e  # 字符串转list
    random.shuffle(email_start)  # 打乱列表，返回值为空
    email = ''.join(email_start) + email_end   # 一个完整的邮箱号  list转字符串
    return email


def random_name_str():
    # step1 生成姓
    while True:
        xing_one = NAME_XING[random.randint(0, len(NAME_XING) - 1)]
        if len(xing_one) == 1:
            xing = xing_one
            break
    # step2 生成名
    ming = ''
    ming = MING[random.randint(0, len(MING) - 1)]
    return xing + ming
