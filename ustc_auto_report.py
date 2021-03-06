import json
from bs4 import BeautifulSoup
import datetime
import os
import telegram
import requests

chat_id = '你的频道号/自己账号，是一长串数字嗷'
token = '你机器人的号码'
bot = telegram.Bot(token=token)

from ustc_passport_login import USTCPassportLogin


class USTCAutoHealthReport(object):
    def __init__(self):
        # 用于登录
        self.login_bot = USTCPassportLogin()
        self.sess = self.login_bot.sess
        # CAS身份认证url
        self.cas_url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
        # 打卡url
        self.clock_in_url = 'https://weixine.ustc.edu.cn/2020/daliy_report'
        # 每周报备url
        self.report_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
        # 每日进出校申请url
        self.stayinout_apply_url = 'https://weixine.ustc.edu.cn/2020/apply/daliy/ipost'
        # 上传两码url
        self.upload_code_url = 'https://weixine.ustc.edu.cn/2020/upload/xcm'
        # 身份认证token
        self.token = ''

    def _get_token(self):
        """
        获取打卡时需要提供的验证字段
        """
        response = self.sess.get(self.cas_url)
        s = BeautifulSoup(response.text, 'lxml')
        token = s.find(attrs={'name': '_token'}).get('value')
        return token

    def _check_success(self, response):
        """
        简单check一下有没有成功打卡、报备
        """
        print(response)
        return '成功' in response.text

    def login(self, username, password):
        """
        登录,需要提供用户名、密码
        """
        self.token = ''
        is_success = self.login_bot.login(username, password)
        if is_success:
            self.token = self._get_token()
        return is_success

    def daily_clock_in(self, post_data_file):
        """
        打卡函数，需要提供包含表单内容的json文件
        打卡成功返回True，打卡失败返回False
        """
        try:
            with open(post_data_file, 'r') as f:
                post_data = json.loads(f.read())
            post_data['_token'] = self.token
            response = self.sess.post(self.clock_in_url, data=post_data)
            s1 = self._check_success(response)
            if s1:
                bot.send_message(chat_id=chat_id,text='打卡成功')
            else:
                bot.send_message(chat_id=chat_id,text='打卡失败')
            return s1
        except Exception as e:
            print(e)
            return False
        
    def upload_code(self):
            data = self.sess.get(
                "https://weixine.ustc.edu.cn/2020/upload/xcm"
            ).text
            data = data.encode("ascii", "ignore").decode("utf-8", "ignore")
            soup = BeautifulSoup(data, "html.parser")
            token = soup.find("input", {"name": "_token"})["value"]

            def run_update(fnm, n):
                data = [
                    ("_token", token),
                    ("id", "WU_FILE_0"),
                ]
                files = {
                    "file": (
                        fnm,
                        open(fnm, "rb"),
                        "image/jpeg",
                        {},
                    )
                }
                post = self.sess.post(
                    "https://weixine.ustc.edu.cn/2020/upload/" + str(n) + "/image",
                    data=data,
                    files=files,
                )
                if "true" not in post.text:
                    print("update failed")
                    return False
                return True

            if run_update("Screenshot_Wechat.jpg", 1) & run_update("Screenshot_Alipay.jpg", 2):
                print("update successful")
                return True
            
    def weekly_report(self):
        """
        报备函数
        报备成功返回1，七天内重复报备返回-1，因其他原因报备失败返回0
        """
        try:
            start_date = datetime.datetime.now()
            end_date = start_date + datetime.timedelta(days=6)
            data = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "_token": self.token
            }
            response = self.sess.post(self.report_url, data=data)
            if not self._check_success(response):
                if '你当前处于“在校已出校报备”状态' in response.text:
                    return -1
                return 0
            return 1
        except Exception as e:
            print(e)
            return 0

    def stayinout_apply(self, apply_data_file):
        """
        2022年3月18日起每日进出校申请
        申请成功返回True,申请失败返回False
        :param apply_data_file表单数据文件
        """
        now = datetime.datetime.now()
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date())+'20:00', '%Y-%m-%d%H:%M')
        d_time2 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:55', '%Y-%m-%d%H:%M')
        if now > d_time1 and now<d_time2:
            try:
                with open(apply_data_file, 'r') as f:
                    post_data = json.loads(f.read())
                post_data['_token'] = self.token
                post_data['start_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
                post_data['end_date'] = tomorrow.strftime('%Y-%m-%d 23:59:59')
                response = self.sess.post(self.stayinout_apply_url, data=post_data)
                s2 = self._check_success(response)
                if s2:
                    bot.send_message(chat_id=chat_id,text='报备成功')
                else:
                    bot.send_message(chat_id=chat_id,text='报备失败')
                return s2
            except Exception as e:
                print(e)
                return False
        else:
            try:
                with open(apply_data_file, 'r') as f:
                    post_data = json.loads(f.read())
                post_data['_token'] = self.token
                post_data['start_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
                post_data['end_date'] = now.strftime("%Y-%m-%d 23:59:59")
                response = self.sess.post(self.stayinout_apply_url, data=post_data)
                s2 = self._check_success(response)
                if s2:
                    bot.send_message(chat_id=chat_id,text='报备成功')
                else:
                    bot.send_message(chat_id=chat_id,text='报备失败')
                return s2
            except Exception as e:
                print(e)
                return False
