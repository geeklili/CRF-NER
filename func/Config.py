# 本地数据库
# MONGODB_CLIENT = "mongodb://127.0.0.1:27017"
MONGODB_CLIENT = "mongodb://192.168.1.8:27017"

# 取jd的数据库
SOURCE_MONGODB_CLIENT = "mongodb://192.168.1.135:27017"
# SOURCE_MONGODB_CLIENT = "mongodb://root:abc123@127.0.0.1:27017"
SOURCE_DATABASE = 'lagou_xiaoxiao'
# SOURCE_DATABASE = 'jd_skillmap'
SOURCE_COLLECTION = 'Android'

# 待标记的数据库和集合
WAIT_POS_DATABASE = 'Android'
WAIT_POS_COLLECTION = 'wait_jd'

# 已经标记的数据和集合
POSED_DATABASE = 'Android'
POSED_COLLECTION = 'posed_jd'

