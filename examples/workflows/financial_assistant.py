# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix-AI.org
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


EMAIL_ACCOUNT = os.getenv("SMTP_ACCOUNT")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to: str, subject: str, body: str) -> None:
    if not EMAIL_ACCOUNT or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_ACCOUNT or EMAIL_PASSWORD is not set")

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, to, msg.as_string())
