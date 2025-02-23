# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import smtplib
from email.mime.text import MIMEText

from synthora.agents import VanillaAgent
from synthora.callbacks.output_handler import OutputHandler
from synthora.toolkits.decorators import tool
from synthora.toolkits.finance import FinanceToolkit
from synthora.toolkits.news import NewsToolkit
from synthora.types.enums import Err, Ok, Result
from synthora.workflows import BaseTask, ThreadPoolScheduler


EMAIL_ACCOUNT = os.getenv("SMTP_ACCOUNT")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")


@tool
def send_email(to: str, subject: str, body: str) -> Result[str, Exception]:
    r"""Send an email to the specified email address.

    Args:
        to: The email address of the recipient.
        subject: The subject of the email.
        body: The body of the email.
    """
    if not EMAIL_ACCOUNT or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_ACCOUNT or EMAIL_PASSWORD is not set")

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ACCOUNT, to, msg.as_string())
        return Ok("Email sent successfully")
    except Exception as e:
        return Err(e, str(e))


def get_news_summary(datas):
    urls = [i["url"] for i in datas]
    news_toolkit = NewsToolkit(False)
    return ThreadPoolScheduler.map(
        BaseTask(news_toolkit.get_summary_by_url), urls
    ).run()


def get_company_news_urls(symbol):
    finance_toolkit = FinanceToolkit()
    return finance_toolkit.get_company_news_urls(symbol).unwrap()


def summarize_news(contents):
    print("Summarizing news")
    agent = VanillaAgent.default("Summarize News into a single paragraph")
    return (
        agent.run("\n\n".join([i.unwrap() for i in contents])).unwrap().content
    )


def send_email_to_user(
    *contents,
    email: str,
):
    print(f"Sending Email: {email}")
    print(contents)
    agent = VanillaAgent.default(
        f"Summarize and send an email to {email}.",
        tools=[send_email],
        handlers=[OutputHandler()],
    )
    return agent.run("\n\n".join([i for i in contents])).unwrap().content


stocks = ["AAPL", "TSLA"]

flow = ThreadPoolScheduler.map(
    BaseTask(get_company_news_urls)
    >> BaseTask(get_news_summary)
    >> BaseTask(summarize_news),
    stocks,
) >> BaseTask(send_email_to_user).s(email="xukunliu@syntropix.ai")

print(flow.run())
