# -*- coding: utf-8 -*-

import smtplib,time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import Config
cf = Config.Config()


class SendEmail(object):
    global send_user
    global pwd
    global email_host

    def send_mail(self, user_list, content, sub,file_path=None):
        """
        :param user_list: 收件人列表
        :param content: 邮件内容
        :param sub: 主题
        :return:
        """
        send_user = cf.sender
        password = cf.password
        email_host = cf.smtpserver
        sender_msg = "yinhaitao" + "<" + send_user + ">"
        message = MIMEMultipart()
        message['Subject'] = Header(sub,'utf-8')
        message['From'] = sender_msg
        message['To'] = ";".join(user_list)
        message['Date'] = time.ctime()
        email_text = MIMEText(content, 'plain', 'utf-8')  # 邮件的内容，和内容的格式。这里是txt/plain，纯文本类型。
        email_file = MIMEApplication(open(file_path,'rb').read())  # 第一个参数打开文件read()方法读出所有内容，刚好是字符串格式,第二个参数是希望的编码，这种方法比较简单
        file_name = file_path.split('/')[-1]
        email_file.add_header('Content-Disposition', 'attachment',filename=file_name)  # 这里添加一个标题，Content-Disposition,attachment说明是一个附件，filename说明文件名．mail里有一个get_filename()的方法可以得到附件里的文件名。
        # filename不能随便命名，因为后缀名会影响到文本的格式。例如把"html"换成"txt"，最后加载到QQ邮件的附件就是‘temp.txt’。
        message.attach(email_text)  # 把我们刚才写的邮件内容加进去
        message.attach(email_file)  # 现在我们把编码好的附件也加进去

        server = smtplib.SMTP()
        server.connect(email_host)
        server.login(send_user, password)
        server.sendmail(sender_msg, user_list, message.as_string())
        server.close()

    def send_main(self, pass_num, fail_num,file_path=None):
        pass_num = float(pass_num)
        fail_num = float(fail_num)
        count_nums = pass_num + fail_num
        # 计算通过率
        pass_result = "%.2f%%" %(pass_num/count_nums*100)
        fail_result = "%.2f%%" %(fail_num/count_nums*100)
        user_list = ['yinhaitao@woda.ink']
        sub = "接口自动化测试报告"
        content = "本次自动化测试一共运行的接口数为:%d个, 通过个数为:%d个, 失败个数为:%d个, 通过率为:%s, 失败率为:%s" %(count_nums,pass_num,fail_num,pass_result,fail_result)
        self.send_mail(user_list,content,sub,file_path)
