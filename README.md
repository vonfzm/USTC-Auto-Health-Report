# USTC-Auto-Health-Report
## 中科大健康打卡平台自动打卡脚本-电报反馈结果

本项目仅供学习使用，来源于不知道愿不愿意透露姓名的已经下架的同名项目（愿意请联系我写上原作者），稍加修改适应了3月30日增加宿舍号后的系统，并加入了电报机器人自动反馈打卡与报备结果。使用方法部分参考了中国滑稽大学(University of Ridiculous of China)健康打卡平台自动打卡脚本。

- [x] 统一身份认证登录
    - [x] 验证码绕过
    - [ ] 验证码识别（能绕过为什么要识别？）
    
- [x] 健康打卡
- [x] 出校报备
- [x] 进出校申请


# 环境

python==3.9

见requirements.txt

# 使用方法

配置Python环境，安装依赖（pip -install -r ）
## 每日打卡
手动打卡并抓包，将除_token外的其他内容以JSON格式放置于post.json文件中，即可结合各类定时程序，调用脚本进行打卡。

示例见post.json。

每天调用一次。

## 进出校申请

手动进行申请并抓包，将除_token、时间参数以外的内容以JSON格式放置于apply.json文件中，即可结合各类定时程序，调用脚本进行进出校申请。

若有多个相同参数，请以list数据类型存放。

每天调用一次。

## 调用示例:
```python
from ustc_auto_report import USTCAutoHealthReport

bot = USTCAutoHealthReport()
# 登录
bot.login('SAxxxxxxxx', 'password')
# 打卡
bot.daily_clock_in('post.json')
# 报备
bot.weekly_report()
# 进出校申请
bot.stayinout_apply('apply.json')
```
