from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', blabla=restaurant_id)
    return "page to create a new menu item."

@app.route('/')
# def DefaultRestaurantMenu():
#    restaurant = session.query(Restaurant).first()
#    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
#    output = ''
#    for i in items:
#        output += i.name
#        output += '</br>'


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    print 'OK'
    editeditem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        session.add(editeditem)
        session.commit()
        flash("the item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant_inf = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editmenuitem.html', restaurant=restaurant_id, menu=menu_id, edited_item=editeditem)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteditem = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant_inf = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #print restaurant_inf
    #print "ok restaurant"
    #print deleteditem
    #print "OK deleted"
    #print deleteditem.name
    if request.method == 'POST':
        session.delete(deleteditem)
        session.commit()
        flash("the item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        #print restaurant_inf.name
        #print deleteditem.name
        return render_template('deleteditem.html', restaurant=restaurant_id, menu=menu_id, rest_name=restaurant_inf.name, deleted_item=deleteditem.name)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print restaurant.name
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    print (items)
    return render_template('menu.html', restaurant=restaurant, items=items)

if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
