from flask import render_template, request, redirect, url_for
from flask_login import login_required


class ViewController:
    @staticmethod
    def main():
        return render_template('index.html')

    @staticmethod
    def home():
        if request.method == 'POST':
            return redirect(url_for('logout'))
        return render_template('home.html')