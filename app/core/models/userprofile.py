from datetime import timedelta, datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from app.core.config import settings


class User(Base):
    __tablename__ = "hr_panel_user"

    username: Mapped[str] = mapped_column(String(length=100))
    telegram_id: Mapped[int]
    come_to_call: Mapped[bool]
    date_call_id: Mapped[int] = mapped_column(ForeignKey("hr_panel_call.id"))
    start_word_id: Mapped[int] = mapped_column(ForeignKey("hr_panel_codeword.id"))
    call_word_id: Mapped[int] = mapped_column(ForeignKey("hr_panel_codeword.id"))
    candidate_decision_status: Mapped[str] = mapped_column(String(length=6))
    is_invitation_sent: Mapped[bool] = mapped_column(default=False)
    consent_personal_data: Mapped[bool]

    user_profile: Mapped["UserProfile"] = relationship(back_populates="user")


class UserProfile(Base):
    __tablename__ = "hr_panel_userprofile"

    user_id: Mapped[int] = mapped_column(ForeignKey("hr_panel_user.id"))
    internship_conditions: Mapped[bool]
    internship_areas: Mapped[str]
    about_internship: Mapped[str]
    email: Mapped[str] = mapped_column(String(length=100))
    fio: Mapped[str]
    country: Mapped[str] = mapped_column(String(length=100))
    reasons_for_internship: Mapped[str]
    time_for_project: Mapped[str]
    tools: Mapped[str]
    additional_skills: Mapped[str]
    resume: Mapped[str]
    ml_answer: Mapped[str] = mapped_column(String(length=100), default="")
    test_solution: Mapped[str] = mapped_column(String(length=500), default="")
    time_create: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    id_page: Mapped[str] = mapped_column(default="")
    is_new: Mapped[bool] = mapped_column(default=True)
    is_updated: Mapped[bool] = mapped_column(default=False)
    ID: Mapped[str] = mapped_column(default="")
    expire_date_test_task: Mapped[DateTime] = mapped_column(
        DateTime(),
        default=lambda: datetime.now() + timedelta(hours=settings.db.delta),
    )

    user: Mapped["User"] = relationship(back_populates="user_profile")
