#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

DEVELOPMENT_ENV  = True

app = Flask(__name__)

app_data = {
    "name":         "Peter's Starter Template for a Flask Web App",
    "description":  "A basic Flask app using bootstrap for layout",
    "author":       "Peter Simeth",
    "html_title":   "Peter's Starter Template for a Flask Web App",
    "project_name": "Tennis",
    "keywords":     "flask, webapp, template, basic"
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)


@app.route('/point')
def point():
    return render_template('point.html', app_data=app_data)


@app.route('/register')
def register():
    return render_template('register.html', app_data=app_data)


@app.route('/home')
def home():

    # counting strokes 
    name = "Jacob"
    strokes = ["b", "f", "b", "s", "v", "v", "b", "f", "s", "b"]
    backhand = strokes.count("b")

    return render_template('home.html', name=name ,strokes=strokes, backhand=backhand, app_data=app_data)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
    