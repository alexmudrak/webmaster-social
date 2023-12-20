from typing import Optional

from models.project import ProjectBase
from models.setting import SettingBase


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingCreate):
    pass


class SettingRead(SettingBase):
    pass


class SettingReadWithProject(SettingRead):
    project: Optional[ProjectBase] = None
