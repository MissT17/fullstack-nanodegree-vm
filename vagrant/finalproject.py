from flask import Flask, render_template, request, redirect, url_for, jsonify
from json_format import serialize, serialize_resto, serialize_item
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1', 'resto_id': '1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2', 'resto_id': '1'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3', 'resto_id': '2'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4', 'resto_id': '2'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5', 'resto_id': '2'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'resto_id': '1'}
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


@app.route('/restos/new', methods=['GET','POST'])
def createNewResto():
    if request.method == 'POST':
        if request.form['name']:
            print 'a new restaurant is being added'
            new_resto = {}
            print len(restaurants)
            print new_resto
            new_resto['name'] = request.form['name']
            new_resto['id']=len(restaurants)+1
            restaurants.append(new_resto)
            print restaurants
            return redirect(url_for('showallrestaurants'))
    return render_template('addresto.html')
    #return 'Create new resto'


@app.route('/restos/<int:resto_id>/edit', methods=['GET', 'POST'])
def editResto(resto_id):
    #return 'Restaurant has been edited'
    res = restaurants[resto_id-1]
    print res
    name_resto = res['name']
    print name_resto
    print resto_id
    if request.method == 'POST':
        print 'POST message sent'
        if request.form['name']:
            editeditem= request.form['name']
            restaurants[resto_id-1]["name"]=editeditem
            print 'this is the edited item'
            print editeditem
            # flash("the item has been edited")
            return redirect(url_for('showallrestaurants'))
    else:
    #    #restaurant_inf = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #    return render_template('edit_menu_item.html', resto_identif=resto_id, edited_item=editeditem)
        return render_template('editresto.html', resto_identif=resto_id, name_resto=name_resto)


@app.route('/restos/<int:resto_id>/delete', methods=['GET', 'POST'])
def deleteResto(resto_id):
    #resto = restaurants[resto_id-1]
    #resto_name = resto['name']
    #print resto_name
    for res in restaurants:
        if res.get('id') == resto_id:
            resto_name=res['name']
            print resto_name
            if request.method == 'POST':
                print 'Post'
                restaurants.remove(res)
                print restaurants
                return redirect(url_for('showallrestaurants'))
    return render_template('deleteresto.html', resto=resto_id, resto_name=resto_name)
    #return 'Restaurant has been deleted'


@app.route('/restos/<int:resto_ID>', methods=['GET','POST'])
@app.route('/restos/<int:resto_ID>/menu')
def restoMenu(resto_ID):
    res = restaurants[resto_ID-1]
    name_resto = res['name']
    resto_menu = []
    for item in items:
        if int(item.get('resto_id')) == resto_ID:
            print 'Please add the menu item to the restaurant'
            resto_menu.append(item)
            print resto_menu
            #return 'Here is the menu of the restaurant'
    if len(resto_menu) == 0:
        print 'oups'
        return redirect(url_for('addNewMenuItem', resto_id=resto_ID))
    return render_template('resto_menu.html', resto_identif=resto_ID, menu=resto_menu, name_resto=name_resto)  


@app.route('/restos/<int:resto_ID>/menu/JSON')
def restoMenuJSON(resto_ID):
    resto_menu = []
    for item in items:
        if int(item.get('resto_id')) == resto_ID:
            print item
            resto_menu.append(item)
            print resto_menu
        else:
            print 'No menu items'
    return jsonify(MenuItems=[serialize(i) for i in resto_menu])


@app.route('/restos/JSON')
def listrestoJSON():
    return jsonify(Restaurants=[serialize_resto(restaurant) for restaurant in restaurants])


@app.route('/restos/<int:resto_id>/menu/<int:item_id>/JSON')
def menuItem(resto_id, item_id):
    print item_id
    for item in items:
        if int(item.get('resto_id')) == resto_id:
            print 'resto OK'
            print resto_id
            if int(item.get('id')) == item_id:
                print 'Item OK'
                print item_id
                return jsonify(MenuItem=[serialize_item(item)])
            else:
                output = "<html><body><p>This menu item does not exist</p></body></html>"
                print 'This menu item does not exist'
                return output
        else:
            output = "<html><body><p>This menu item does not exist at thos restaurant</p></body></html>"
            print 'This menu item does not exist at thos restaurant'
            return output


@app.route('/restos/<int:resto_id>/menu/<int:item_id>/edit', methods=['GET', 'POST'])
def editMenuItems(resto_id, item_id):
    item=items[item_id-1]
    item_name=item['name']
    print item_name
    if request.method=='POST':
        print 'New item delivered'
        if request.form['name']:
            print 'New name defined'
            edited_menu_item= request.form['name']
            items[item_id-1]["name"]=edited_menu_item
            print 'this is the edited item'
            print edited_menu_item
            # flash("the item has been edited")
            return redirect(url_for('restoMenu', resto_ID=resto_id))
    else:
        return render_template('edit_menu_item.html', resto=resto_id, item=item_id, item_name=item_name)
        #return 'The menu item of restaurant has been edited'


@app.route('/restos/<int:resto_id>/menu/new', methods=['GET', 'POST'])
def addNewMenuItem(resto_id):
    resto=restaurants[resto_id-1]
    resto_name=resto['name']
    if request.method=='POST':
        if request.form['name']:
            added_item={}
            added_item['name']=request.form['name']
            added_item['description']=request.form['description']
            added_item['price']=request.form['price']
            added_item['course']=request.form['course']
            added_item['id']=len(items)+1
            added_item['resto_id']=resto_id
            items.append(added_item)
            print items
            return redirect(url_for('restoMenu', resto_ID=resto_id))
    return render_template('add_menu_item.html', resto=resto_id, resto_name=resto_name) 
    #return 'Menu item has been added to the restaurant'


@app.route('/restos/<int:resto_id>/menu/<int:item_id>/delete', methods=['GET','POST'])
def deleteMenuItem(resto_id, item_id):
    print resto_id
    print 'the resto id'
    for res in restaurants:
        if res.get('id')==resto_id:
            resto_name=res['name']
            print resto_name
            print 'the resto name'
    for item in items:
        if item['id']==item_id:
            item_name=item['name']
            print item_name
            print items
            if request.method=='POST':
                print item_name
                items.remove(item)
                print items            
                return redirect(url_for('restoMenu',resto_ID=resto_id))
    return render_template('delete_menu_item.html',resto=resto_id, item=item_id, resto_name=resto_name, item_name=item_name)
    #return 'The menu item from restaurant has been deleted'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)