from typing import Optional

from models.project import ProjectBase
from models.setting import SettingBase


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingCreate):
    pass


class SettingRead(SettingBase):
    id: int
    project_name: Optional[str] = None


class SettingReadWithProject(SettingRead):
    project: Optional[ProjectBase] = None
