from flask import Flask, render_template,request
from post import Post
import requests
import smtplib
from email.mime.text import MIMEText

EMAIL = "appberry1111@gmail.com"
PWD = "skadnd12!@#"

# https://www.npoint.io/ 사이트를 이용한 custom json api
BLOG_URL = "https://api.npoint.io/5d2305f59a0bd37d44eb"
response = requests.get(BLOG_URL)
all_post = response.json()

post_contents = []
for post in all_post:
    blog_post = Post(post['id'],post['title'],post['subtitle'],post['body'])
    post_contents.append(blog_post)


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html',posts=post_contents)


@app.route('/about.html')
def get_about_page():
    return render_template('about.html')


@app.route('/contact.html',methods=["GET","POST"])
def get_contact_page():
    success_msg = None
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['useremail']
        phonenumber = request.form['phonenumber']
        message = request.form['usermsg']

        # contact.html에서 메세지 입력 후 smtplib 이용한 메일 전송
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(EMAIL, PWD)

        # 보낼 메시지 설정
        content = f"이름: {name}\nemail: {email}\nphone: {phonenumber}\n{message}"
        msg = MIMEText(content)
        msg['Subject'] = '제목 : New Message'

        # 메일 보내기
        s.sendmail(EMAIL, EMAIL, msg.as_string())

        # 세션 종료
        s.quit()

        success_msg = "Success"
    else:
        success_msg = "Contact Me"

    return render_template('contact.html',msg=success_msg)


@app.route('/post/<post_id>')
def get_post(post_id):
    requested_blog = None
    for content in post_contents:
        if post_id == content.id:
            requested_blog = content

    return render_template("post.html",post=requested_blog)



if __name__ == '__main__':
    app.run(debug=True)