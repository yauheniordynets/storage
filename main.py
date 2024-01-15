from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_vue import Vue
from app import create_app
from app.models import Product, Position
from app.database import *

app = Flask(__name__)
Vue(app)
app = create_app()


class Data():
    def __init__(self, searchResultRow = None, searchResultCol = None):
        self.searchResultRow = searchResultRow
        self.searchResultCol = searchResultCol


@app.route('/')
def index():
    t = 0
    return render_template('index.html')


@app.route('/api/search', methods=['GET','POST'])
def api_search():
    data = request.args.get('searchInput')
    search_result = session.query(Product, Position).join(Position, Product.id == Position.product_id).filter(Product.name.like(f"%{data}%")).first()

    if search_result:
        product, position = search_result
        search_result_data = {
            'searchResultRow': position.row_number,
            'searchResultCol': position.column_number,
            'productName': product.name,
            'productAlternativeName': product.alternative_name
        }
        return jsonify(search_result_data)

    return jsonify({'error': 'No results found for the given search term'}), 404


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':

        name = request.form['name']
        alternative_name = request.form['alternative_name']
        quantity = float(request.form['quantity'])
        quantity_in_metres = int(quantity*150)
        status = bool(int(request.form['status']))
        position_x = int(request.form['position_x'])
        position_y = int(request.form['position_y'])

        new_product = Product(name=name, alternative_name=alternative_name,
                              quantity=quantity, quantity_in_metres=quantity_in_metres,
                              status=status)
        session.add(new_product)
        session.commit()

        product_id = session.query(Product.id).filter(Product.name == name).scalar()

        new_position = Position(product_id=product_id, row_number=position_x, column_number=position_y)
        session.add(new_position)
        session.commit()

        return redirect(url_for('index'))
    return render_template('add_item.html')


@app.route('/all_items', methods=['GET', 'POST'])
def all_items():
    data = request.args.get('search')

    if data:
        items = session.query(Product).filter(Product.name.like(data)).all()
    else:
        items = session.query(Product).all()
    return render_template('all_items.html', items=items, data=data)


@app.route('/api/cell_page', methods=['POST'])
def cell_page_api():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    redirect_url = f'/cell_page?row={row}&col={col}'

    return jsonify({'redirect_url': redirect_url})


@app.route('/cell_page', methods=['GET', 'POST'])
def cell_page():
    try:
        row = int(request.args.get('row'))
        col = int(request.args.get('col'))

        position_ids = (
            session.query(Position.product_id)
            .filter(Position.row_number == row, Position.column_number == col)
            .all()
        )

        product_ids = [item[0] for item in position_ids]

        result = (
            session.query(Product)
            .filter(Product.id.in_(product_ids))
            .all()
        )
        return render_template('cell_page.html', row=row, col=col, result=result)
    except Exception as e:

        print(f"Error: {e}")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
