from flask import Flask, render_template, redirect, request

def error(the_error):
    the_error = str(the_error)
    return render_template("error.html", error_t=the_error)
