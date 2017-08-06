from flask import Flask, render_template
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
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
    #return 'Restaurant has been edited'
    res=restaurants[resto_id-1]
    print res
    name_resto=res['name']
    print name_resto
    return render_template('edit_menu_item.html', resto_identif=name_resto)


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