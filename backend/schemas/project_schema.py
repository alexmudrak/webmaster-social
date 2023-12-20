from typing import List

from models.project import ProjectBase
from models.setting import SettingBase
from pydantic import HttpUrl


class ProjectCreate(ProjectBase):
    url: HttpUrl


class ProjectUpdate(ProjectCreate):
    pass


class ProjectRead(ProjectBase):
    pass


class ProjectReadWithSettings(ProjectRead):
    setting: List[SettingBase] = []
