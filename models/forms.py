from models import BaseTable
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

class BackCallWidget(BaseTable):
    __tablename__ = "back_call_widgets"

    phone_number: Mapped[str]

################################################################


class FormTable(BaseTable):
    __abstract__ = True 

    full_name: Mapped[str]
    phone_number: Mapped[str]
    location: Mapped[str]
    known_from: Mapped[str]
    
################################################################

class BackCallForm(FormTable):
    __tablename__ = "back_call_forms"


class WorkWithUsForm(FormTable):
    __tablename__ = "work_with_us_forms"

    about: Mapped[str] = mapped_column(Text)


class LinkGoogleForm(BaseTable):
    __tablename__ = "link_google_form"

    description: Mapped[str]
    btn_name: Mapped[str]
    btn_url: Mapped[str]
