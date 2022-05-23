from model import User
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required, login_manager, logout_user, login_user
from flask_restful import Api
import hashlib

app_project = Blueprint('project', __name__,
                      url_prefix='/project',
                      template_folder='museum/',
                      static_folder='static',
                      static_url_path='assets')