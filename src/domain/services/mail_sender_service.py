from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


@dataclass
class MailSenderConfigDTO:
    sender: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str


class MailSenderService:
    _smtp_config: MailSenderConfigDTO

    def __init__(self, smtp_config: MailSenderConfigDTO) -> None:
        self._smtp_config = smtp_config

    async def send_login_code_by_email(self, code: str, email: str) -> None:
        smtp_client = aiosmtplib.SMTP(
            hostname=self._smtp_config.smtp_host,
            username=self._smtp_config.smtp_user,
            password=self._smtp_config.smtp_password,
            port=self._smtp_config.smtp_port,
        )

        message = self._build_login_code_email(email, code)
        await smtp_client.connect()
        await smtp_client.sendmail(self._smtp_config.sender, email, message)
        await smtp_client.quit()

    def _build_login_code_email(self, email: str, code: str) -> str:
        message = MIMEMultipart()
        message["Subject"] = "Код для входа в аккаунт"
        message["From"] = self._smtp_config.sender
        message["To"] = email

        html_body = MIMEText(
            f"""
            <html>
                <body>
                    <center><h2>Ваш код подтверждения: </h2><center>
                    <center><h2>{code}</h2></center>
                </body>
            </html>""",
            "html",
            "utf-8",
        )

        message.attach(html_body)
        return message.as_string()
