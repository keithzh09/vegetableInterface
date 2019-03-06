# -*- coding: utf-8 -*-
# @time    : 19-2-28
# @author  : lin
from flask import Blueprint
manager_app = Blueprint('manager_app', __name__)
import manager.app,manager.dao