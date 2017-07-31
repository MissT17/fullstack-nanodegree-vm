from flask import Flask, render_template
app = Flask(__name__)

#from sqlalchemy import create_engine
#from database_setup import Base, Restaurant, MenuItem
##from sqlalchemy.orm import sessionmaker
#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()


@app.route('/')
@app.route('/restos/')
def showallrestaurants():
    #return 'this is the page with all the restaurants'
    return render_template('allrestos.html', restos=restaurants)


@app.route('/restos/new')
def createNewResto():
    return 'Create new resto'


@app.route('/restos/<int:resto_id>/edit')
def editResto(resto_id):
    return 'Restaurant has been edited'


@app.route('/restos/<int:resto_id>/delete')
def deleteResto(resto_id):
    return 'Restaurant has been deleted'


@app.route('/restos/<int:resto_id>')
@app.route('/restos/<int:resto_id>/menu')
def restoMenu(resto_id):
    return 'Here is the menu of the restaurant'


@app.route('/restos/<int:resto_id>/menu/<int:item_id>/edit')
def showMenuItems(resto_id, item_id):
    return 'The menu item of restaurant has been edited'


@app.route('/restos/<int:resto_id>/menu/new')
def addNewMenuItem(resto_id):
    return 'Menu item has been added to the restaurant'


@app.route('/restos/<int:resto_id>/menu/<int:item_id>/delete')
def deleteMenuItem(resto_id, item_id):
    return 'The menu item from restaurant has been deleted'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)