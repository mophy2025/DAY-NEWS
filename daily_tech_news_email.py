import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# 配置
NEWS_API_KEY = '你的newsapi_key'      # ← 需在 newsapi.org 注册获取
YOUR_EMAIL = '你的邮箱地址'
SMTP_SERVER = 'smtp.qq.com'           # 以QQ邮箱为例，其它邮箱服务器请更换
SMTP_PORT = 465
EMAIL_USER = '你的邮箱账号'
EMAIL_PASS = '你的邮箱授权码'          # 邮箱生成的授权码，不是登录密码

def fetch_top_tech_news():
    url = (
        "https://newsapi.org/v2/top-headlines"
        "?category=technology"
        "&language=en"
        "&pageSize=10"
        f"&apiKey={NEWS_API_KEY}"
    )
    resp = requests.get(url)
    data = resp.json()
    if 'articles' in data:
        return data['articles']
    else:
        return []

def send_email(subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = EMAIL_USER
    msg['To'] = YOUR_EMAIL
    msg['Subject'] = Header(subject, 'utf-8')
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [YOUR_EMAIL], msg.as_string())

def main():
    articles = fetch_top_tech_news()
    if not articles:
        print("未获取到新闻")
        return
    
    s = f"今日全球科技热点 TOP 10（{datetime.now().strftime('%Y-%m-%d')}）\n\n"
    for i, a in enumerate(articles, 1):
        s += f"{i}. {a['title']}\n"
        s += f"   {a.get('url', '')}\n"
        if 'description' in a and a['description']:
            s += f"   摘要: {a['description']}\n"
        s += "\n"
    send_email("今日科技新闻 TOP 10", s)
    print("已发送邮件")

if __name__ == "__main__":
    main()