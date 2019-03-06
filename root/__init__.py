# -*- coding: utf-8 -*-
# @time    : 19-2-28
# @author  : lin
from flask import Blueprint
root_app = Blueprint('root_app', __name__)
import root.app, root.dao