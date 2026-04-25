import requests
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# === 基本配置 ===
QQ_EMAIL = "2062719734@qq.com"
QQ_SMTP_PASS = "bmegdlneuoahchie"
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
RECEIVER = "2062719734@qq.com"

# --- 新闻抓取 ---
def get_hackernews():
    """获取Hacker News 热门新闻（英文）"""
    url = 'https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=15'
    resp = requests.get(url)
    news_list = resp.json()['hits']
    results = []
    for item in news_list:
        if item['title'] and item['url']:
            results.append({'title': item['title'], 'url': item['url']})
        if len(results) >= 10:
            break
    return results

# --- 编排列表 ---
def build_news_list(news_items):
    lines = []
    for i, news in enumerate(news_items, 1):
        title_en = news['title']
        title_cn = translate_to_cn(title_en)
        lines.append(f"{i}. {title_en}\n   {title_cn}\n   {news['url']}\n")
    return '\n'.join(lines)

# --- 邮件发送 ---
def send_mail(subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = QQ_EMAIL
    msg['To'] = RECEIVER
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(QQ_EMAIL, QQ_SMTP_PASS)
        server.sendmail(QQ_EMAIL, [RECEIVER], msg.as_string())

if __name__ == '__main__':
    news = get_hackernews()
    news_list_str = build_news_list(news)
    subject = "daily news"
    send_mail(subject, news_list_str)
