from flask import session, redirect, flash

def logout():
    session.pop('token', None)  
    flash("Logged out successfully", "success")
    return redirect('/login') 
