class Basket():
    """
    A base Basket class, providing some default behaviors that
    can bem inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket = self.session['skey'] = {'number': 1231231}

        self.basket = basket

    def __add__(self):
        pass

    def add(self, product, product_qty):
        """
        adding and updating the users basket session data
        :param product_qty:
        :param product:
        :return:
        """
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

    def __len__(self):
        """
        Get the basket data and count the qty of items
        :return:
        """
        return sum(item['qty'] for item in self.basket.values())
