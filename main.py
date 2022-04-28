from ustc_auto_report import USTCAutoHealthReport
import random,time
# 随机时间延迟，单位为秒
time.sleep(random.randint(0, 300))
bot = USTCAutoHealthReport()
# 登录
bot.login('你的学号', '你的密码')
# 打卡
bot.daily_clock_in('post.json')
# 上传两码
# bot.upload_code()
# time.sleep(random.randint(60, 62))
# 进出校申请
bot.stayinout_apply('apply.json')
